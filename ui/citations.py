"""
ui/citations.py - Citation Formatting Helpers
               (Story 4.5: Raw Citation Display → Story 5.2: Enhanced Footer)

Provides pure-Python helpers that convert raw LangChain Document objects
into styled HTML citation footers.  No Streamlit imports here — the caller
(ui/app.py) handles rendering with `unsafe_allow_html=True`.
"""

from __future__ import annotations

from typing import List

from langchain_core.documents import Document


def format_citation_footer(docs: List[Document]) -> str:
    """Build a styled HTML citation footer from retrieved LangChain Documents.

    Deduplicates by URL so that multiple chunks from the same Knowledge Base
    page appear as a single citation entry.  Uses raw ``<a target="_blank">``
    tags so links reliably open in a new tab regardless of browser environment
    (standard markdown links in Streamlit do not guarantee ``target="_blank"``).

    Parameters
    ----------
    docs:
        Raw retrieved ``Document`` objects as returned by ``generate_answer``.

    Returns
    -------
    str
        A markdown+HTML string beginning with a ``---`` separator and a styled
        ``<div>`` citation list, or an empty string if *docs* is empty or every
        doc is missing both ``title`` and ``url`` metadata.

    Notes
    -----
    The caller **must** render this string with
    ``st.markdown(footer, unsafe_allow_html=True)`` — the HTML ``<a>`` tags
    will otherwise be displayed as raw text.
    Using ``unsafe_allow_html`` is safe here because URLs and titles are
    generated exclusively by the internal ingestion pipeline, not by users.

    Examples
    --------
    >>> from langchain_core.documents import Document
    >>> docs = [
    ...     Document(page_content="…", metadata={"title": "Pipeline Guide",
    ...                                           "url": "https://example.com/a"}),
    ...     Document(page_content="…", metadata={"title": "Error Handling",
    ...                                           "url": "https://example.com/b"}),
    ... ]
    >>> print(format_citation_footer(docs))
    ...  # Returns HTML citation footer block
    """
    if not docs:
        return ""

    seen_urls: set[str] = set()
    link_items: List[str] = []

    for doc in docs:
        url: str = doc.metadata.get("url", "")
        title: str = doc.metadata.get("title", "")

        # Skip docs with no useful metadata
        if not url and not title:
            continue

        # Deduplicate by URL (fall back to title as dedup key if URL missing)
        dedup_key = url if url else title
        if dedup_key in seen_urls:
            continue
        seen_urls.add(dedup_key)

        # Use explicit HTML <a> tag to enforce target="_blank" (AC 6)
        display_text = title if title else url
        if url:
            link_items.append(
                f'<a href="{url}" target="_blank" rel="noopener noreferrer">'
                f"{display_text}</a>"
            )
        else:
            link_items.append(display_text)

    if not link_items:
        return ""

    # Build the styled footer block
    links_html = "\n".join(f"<li>{item}</li>" for item in link_items)
    footer = (
        "\n\n---\n**Sources:**\n"
        '<div style="font-size: 0.8em; color: gray;">'
        f"<ul>{links_html}</ul>"
        "</div>"
    )
    return footer


# ---------------------------------------------------------------------------
# Backward-compat alias — kept so any future callers of the 4.5 function
# name still work without changes.
# ---------------------------------------------------------------------------

def format_citations(docs: List[Document]) -> str:  # noqa: D103
    """Alias for :func:`format_citation_footer` (backward compatibility)."""
    return format_citation_footer(docs)
