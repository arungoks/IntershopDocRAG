"""
ingestion/splitter.py
----------------------
Splits LangChain Document objects into semantic chunks using
RecursiveCharacterTextSplitter, with chunk_size and chunk_overlap
driven by config.yaml. All original YAML frontmatter metadata is
propagated to every resulting chunk.
"""

import logging
from pathlib import Path
from typing import Any

import yaml
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

# Defaults if config.yaml keys are absent
DEFAULT_CHUNK_SIZE = 2000
DEFAULT_CHUNK_OVERLAP = 200


def _load_config(config_path: str = "config.yaml") -> dict[str, Any]:
    """Load the centralized YAML config file.

    Args:
        config_path: Path to config.yaml (defaults to project root).

    Returns:
        Parsed config dictionary; empty dict on any read/parse error.
    """
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


def split_documents(
    documents: list[Document],
    config_path: str = "config.yaml",
) -> list[Document]:
    """Split a list of LangChain Documents into smaller chunks.

    Reads chunk_size and chunk_overlap from config.yaml (falling back to
    2000 / 200). All metadata from the source Document is propagated to
    every resulting chunk so that citation pipeline always has id, title,
    url, and scraped_at.

    Args:
        documents:   List of Documents produced by ingestion/loader.py.
        config_path: Path to the project's config.yaml.

    Returns:
        Flat list of chunk Documents ready for embedding.
    """
    if not documents:
        logger.info("No documents to split — returning empty list.")
        return []

    config = _load_config(config_path)
    chunk_size = int(config.get("chunk_size", DEFAULT_CHUNK_SIZE))
    chunk_overlap = int(config.get("chunk_overlap", DEFAULT_CHUNK_OVERLAP))

    logger.info(
        "Splitting %d documents — chunk_size=%d, chunk_overlap=%d",
        len(documents),
        chunk_size,
        chunk_overlap,
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = splitter.split_documents(documents)

    logger.info("Produced %d chunks from %d source documents.", len(chunks), len(documents))
    return chunks
