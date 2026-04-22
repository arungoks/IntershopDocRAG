"""
ingestion/embedder.py
----------------------
Embeds LangChain Document chunks using a local Ollama model and persists
the resulting vectors to a local ChromaDB instance.

Key design decisions:
- Uses langchain_ollama.OllamaEmbeddings (not the deprecated langchain.embeddings)
- Uses langchain_chroma.Chroma with a persist_directory for local storage
- build_vector_store() initialises Chroma + Ollama ONCE per run (not per file)
- embed_and_store() accepts a pre-built vector_store to avoid reconnect overhead
- Generates deterministic chunk IDs to support idempotent reruns (upsert semantics)
- Reads all config from config.yaml; falls back to safe defaults on any failure
- 100% local — no cloud API keys, Ollama must be running at localhost
"""

import logging
import hashlib
from pathlib import Path
from typing import Any

import yaml
from langchain_core.documents import Document

logger = logging.getLogger(__name__)

# Fallback configuration values (mirror NFR requirements)
_DEFAULTS: dict[str, Any] = {
    "embedding_model": "nomic-embed-text",
    "ollama_port": 11434,
    "chroma_db_path": "data/vectordb",
}

# ChromaDB collection name — stable across runs
COLLECTION_NAME = "intershop_kb"


def _load_config(config_path: str = "config.yaml") -> dict[str, Any]:
    """Load project config.yaml, returning defaults on failure."""
    path = Path(config_path)
    if not path.exists():
        logger.warning("config.yaml not found at %s — using defaults.", config_path)
        return {}
    try:
        with path.open("r", encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    except yaml.YAMLError as exc:
        logger.warning("Failed to parse config.yaml: %s — using defaults.", exc)
        return {}


def _get(config: dict, key: str) -> Any:
    """Retrieve key from config, falling back to _DEFAULTS."""
    return config.get(key, _DEFAULTS.get(key))


def _make_chunk_id(chunk: Document, index: int) -> str:
    """Generate a deterministic, unique ID for a chunk.

    Format: {page_id}-chunk-{index}
    If the metadata 'id' field is missing, falls back to a hash of the content.
    This ensures re-running ingestion overwrites existing vectors rather than
    duplicating them in ChromaDB.
    """
    page_id = chunk.metadata.get("id")
    if page_id:
        return f"{page_id}-chunk-{index}"
    # Fallback: hash of content + index
    content_hash = hashlib.sha256(chunk.page_content.encode()).hexdigest()[:12]
    return f"hash-{content_hash}-chunk-{index}"


def build_vector_store(config_path: str = "config.yaml") -> Chroma:
    """Initialise and return a Chroma vector store backed by Ollama embeddings.

    Call this ONCE per ingestion run and pass the returned object to
    embed_and_store() for every batch. Avoids the cost of creating a new
    ChromaDB client and Ollama connection for every file.

    Args:
        config_path: Path to the centralized config.yaml.

    Returns:
        A ready-to-use langchain_chroma.Chroma instance.

    Raises:
        ConnectionError: If the Ollama server cannot be reached on first embed.
        RuntimeError:    If ChromaDB cannot be initialised.
    """
    # Lazy imports — kept here so importing this module never blocks at startup
    from langchain_chroma import Chroma  # noqa: PLC0415
    from langchain_ollama import OllamaEmbeddings  # noqa: PLC0415

    config = _load_config(config_path)

    embedding_model = str(_get(config, "embedding_model"))
    ollama_port = int(_get(config, "ollama_port"))
    chroma_db_path = str(_get(config, "chroma_db_path"))
    ollama_base_url = f"http://localhost:{ollama_port}"

    logger.info(
        "Initializing OllamaEmbeddings — model=%s, base_url=%s",
        embedding_model, ollama_base_url,
    )
    embeddings = OllamaEmbeddings(
        model=embedding_model,
        base_url=ollama_base_url,
    )

    # Ensure persist directory exists
    Path(chroma_db_path).mkdir(parents=True, exist_ok=True)

    logger.info(
        "Connecting to ChromaDB at %s (collection=%s)", chroma_db_path, COLLECTION_NAME
    )
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=chroma_db_path,
    )

    return vector_store


def embed_and_store(
    chunks: list[Document],
    vector_store: Chroma,
    batch_size: int = 100,
    chunk_index_offset: int = 0,
) -> int:
    """Embed document chunks and upsert them into the provided ChromaDB instance.

    Args:
        chunks:             List of split Document objects from ingestion/splitter.py.
        vector_store:       Pre-initialised Chroma instance from build_vector_store().
        batch_size:         Chunks per Ollama HTTP request (avoids large payloads).
        chunk_index_offset: Added to chunk indices for globally unique IDs when
                            calling this function multiple times in a run.

    Returns:
        Total number of chunks successfully stored.
    """
    if not chunks:
        logger.info("No chunks to embed — skipping.")
        return 0

    # Generate deterministic IDs for all chunks in this call
    ids = [_make_chunk_id(chunk, chunk_index_offset + i) for i, chunk in enumerate(chunks)]

    total_stored = 0

    # Process in batches to keep Ollama HTTP payloads manageable
    for batch_start in range(0, len(chunks), batch_size):
        batch_chunks = chunks[batch_start: batch_start + batch_size]
        batch_ids = ids[batch_start: batch_start + batch_size]

        logger.info(
            "Embedding batch %d–%d of %d chunks...",
            batch_start + 1,
            batch_start + len(batch_chunks),
            len(chunks),
        )

        # add_documents with explicit ids gives upsert-like behaviour —
        # duplicate ids overwrite the existing vector instead of creating dupes.
        vector_store.add_documents(documents=batch_chunks, ids=batch_ids)
        total_stored += len(batch_chunks)

    logger.info("Stored %d chunks.", total_stored)
    return total_stored
