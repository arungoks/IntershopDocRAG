"""
ingestion/loader.py
--------------------
Loads scraped Markdown files from data/raw_md/ as LangChain Document objects.
Explicitly parses YAML frontmatter so that id, title, url, and scraped_at
are available in every Document's metadata dictionary for downstream citation.
"""

import logging
import os
from pathlib import Path
from typing import Optional

import yaml
from langchain_core.documents import Document

logger = logging.getLogger(__name__)

# Required frontmatter keys — any file missing these will be skipped.
REQUIRED_META_KEYS = {"id", "title", "url", "scraped_at"}


def _parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from a Markdown file.

    Returns:
        (metadata_dict, body_text) where body_text has the frontmatter block stripped.
        If no valid frontmatter is found, returns ({}, original_content).
    """
    if not content.startswith("---"):
        return {}, content

    # Find the closing '---'
    end_index = content.find("\n---", 3)
    if end_index == -1:
        return {}, content

    yaml_block = content[3:end_index].strip()
    body = content[end_index + 4:].lstrip("\n")  # skip past closing '---\n'

    try:
        metadata = yaml.safe_load(yaml_block) or {}
        if not isinstance(metadata, dict):
            return {}, content
    except yaml.YAMLError as exc:
        logger.warning("Failed to parse YAML frontmatter: %s", exc)
        return {}, content

    return metadata, body


def load_documents(raw_md_path: str) -> list[Document]:
    """Load all .md files from *raw_md_path* as LangChain Documents.

    Each Document will have its metadata populated from the YAML frontmatter.
    Files missing required frontmatter keys (id, title, url, scraped_at) are
    skipped with a warning to avoid corrupting downstream citation logic.

    Args:
        raw_md_path: Absolute or relative path to the directory containing .md files.

    Returns:
        List of LangChain Document objects ready for text splitting.

    Raises:
        FileNotFoundError: If *raw_md_path* does not exist.
        ValueError: If *raw_md_path* is not a directory.
    """
    directory = Path(raw_md_path)

    if not directory.exists():
        raise FileNotFoundError(f"raw_md directory not found: {raw_md_path}")
    if not directory.is_dir():
        raise ValueError(f"Expected a directory, got: {raw_md_path}")

    documents: list[Document] = []
    md_files = sorted(directory.glob("*.md"))

    for md_file in md_files:
        try:
            content = md_file.read_text(encoding="utf-8")
        except OSError as exc:
            logger.warning("Cannot read file %s: %s", md_file, exc)
            continue

        metadata, body = _parse_frontmatter(content)

        missing = REQUIRED_META_KEYS - metadata.keys()
        if missing:
            logger.warning(
                "Skipping %s — missing frontmatter keys: %s", md_file.name, missing
            )
            continue

        # Coerce all metadata values to strings for ChromaDB compatibility
        str_metadata = {k: str(v) for k, v in metadata.items()}

        documents.append(Document(page_content=body, metadata=str_metadata))

    logger.info("Loaded %d documents from %s", len(documents), raw_md_path)
    return documents
