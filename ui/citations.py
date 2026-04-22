"""
ui/citations.py - Citation Formatting Helpers
               (Story 4.5: Raw Citation Display)

Provides a pure-Python helper that converts raw LangChain Document objects
into a markdown citation string.  No Streamlit imports here — the caller
(ui/app.py) handles rendering.
"""

from __future__ import annotations

from typing import List

from langchain_core.documents import Document


def format_citations(docs: List[Document]) -> str:
    """Build a raw markdown citation list from retrieved LangChain Documents.

    Deduplicates by URL so that multiple chunks from the same Knowledge Base
    page appear as a single citation entry.

    Parameters
    ----------
    docs:
        Raw retrieved ``Document`` objects as returned by ``generate_answer``.

    Returns
    -------
    str
        A markdown-formatted citation block, or an empty string if *docs* is
        empty or every doc is missing both ``title`` and ``url`` metadata.

    Examples
    --------
    >>> from langchain_core.documents import Document
    >>> docs = [
    ...     Document(page_content="…", metadata={"title": "Pipeline Concepts",
    ...                                           "url": "https://example.com/a"}),
    ...     Document(page_content="…", metadata={"title": "Pipeline Concepts",
    ...                                           "url": "https://example.com/a"}),
    ...     Document(page_content="…", metadata={"title": "Error Handling",
    ...                                           "url": "https://example.com/b"}),
    ... ]
    >>> print(format_citations(docs))
    \\n\\n**Sources:**\\n- [Pipeline Concepts](https://example.com/a)\\n- [Error Handling](https://example.com/b)
    """
    if not docs:
        return ""

    seen_urls: set[str] = set()
    entries: List[str] = []

    for doc in docs:
        url: str = doc.metadata.get("url", "")
        title: str = doc.metadata.get("title", "")

        # Skip docs with no useful metadata
        if not url and not title:
            continue

        # Deduplicate by URL (fall back to title if URL is missing)
        dedup_key = url if url else title
        if dedup_key in seen_urls:
            continue
        seen_urls.add(dedup_key)

        # Build the markdown link (or plain title if no URL)
        if url:
            entries.append(f"- [{title or url}]({url})")
        else:
            entries.append(f"- {title}")

    if not entries:
        return ""

    return "\n\n**Sources:**\n" + "\n".join(entries)
