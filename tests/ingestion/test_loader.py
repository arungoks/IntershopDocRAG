"""
tests/ingestion/test_loader.py
------------------------------
Unit tests for ingestion/loader.py.
Tests validate that markdown files are loaded with correct YAML frontmatter
metadata extracted into LangChain Document objects.
"""
import os
import tempfile

import pytest

from ingestion.loader import load_documents


# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #

VALID_MD_CONTENT = """\
---
id: "ABC123"
title: "Test Article"
url: "https://knowledge.intershop.com/kb/ABC123"
scraped_at: "2026-03-28T10:00:00"
---

# Test Article

Some content here.

## Section 1

More content.
"""

MISSING_FRONTMATTER_MD = """\
# No Frontmatter

This file has no YAML frontmatter block.
"""

PARTIAL_FRONTMATTER_MD = """\
---
id: "PARTIAL1"
---

# Partial Frontmatter

Only has id, missing title/url/scraped_at.
"""


@pytest.fixture
def valid_md_dir(tmp_path):
    """Creates a temp directory with one valid markdown file."""
    md_file = tmp_path / "ABC123.md"
    md_file.write_text(VALID_MD_CONTENT, encoding="utf-8")
    return tmp_path


@pytest.fixture
def multi_md_dir(tmp_path):
    """Creates a temp directory with multiple markdown files."""
    (tmp_path / "A1.md").write_text(VALID_MD_CONTENT.replace("ABC123", "A1"), encoding="utf-8")
    (tmp_path / "A2.md").write_text(VALID_MD_CONTENT.replace("ABC123", "A2"), encoding="utf-8")
    return tmp_path


@pytest.fixture
def mixed_md_dir(tmp_path):
    """Creates a temp directory with valid, missing-FM, and non-md files."""
    (tmp_path / "valid.md").write_text(VALID_MD_CONTENT, encoding="utf-8")
    (tmp_path / "no_fm.md").write_text(MISSING_FRONTMATTER_MD, encoding="utf-8")
    (tmp_path / "partial.md").write_text(PARTIAL_FRONTMATTER_MD, encoding="utf-8")
    (tmp_path / "data.csv").write_text("a,b,c", encoding="utf-8")  # non-md, should be ignored
    return tmp_path


@pytest.fixture
def empty_md_dir(tmp_path):
    """Creates an empty temp directory."""
    return tmp_path


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #


class TestLoadDocuments:
    """Tests for the load_documents() function."""

    def test_loads_single_valid_file(self, valid_md_dir):
        """Should load one Document with correct metadata from a valid .md file."""
        docs = load_documents(str(valid_md_dir))
        assert len(docs) == 1
        doc = docs[0]
        assert doc.metadata["id"] == "ABC123"
        assert doc.metadata["title"] == "Test Article"
        assert doc.metadata["url"] == "https://knowledge.intershop.com/kb/ABC123"
        assert doc.metadata["scraped_at"] == "2026-03-28T10:00:00"

    def test_page_content_excludes_frontmatter(self, valid_md_dir):
        """The page_content should not include the raw YAML frontmatter block."""
        docs = load_documents(str(valid_md_dir))
        assert "---" not in docs[0].page_content
        assert "id:" not in docs[0].page_content
        assert "Test Article" in docs[0].page_content

    def test_loads_multiple_files(self, multi_md_dir):
        """Should load all .md files from directory."""
        docs = load_documents(str(multi_md_dir))
        assert len(docs) == 2
        ids = {d.metadata["id"] for d in docs}
        assert ids == {"A1", "A2"}

    def test_skips_file_without_frontmatter(self, mixed_md_dir):
        """Files without YAML frontmatter should be skipped (warn, not crash)."""
        docs = load_documents(str(mixed_md_dir))
        # Only 'valid.md' has all required frontmatter keys
        valid_ids = [d.metadata.get("id") for d in docs if d.metadata.get("id") == "ABC123"]
        assert len(valid_ids) == 1

    def test_ignores_non_md_files(self, mixed_md_dir):
        """Non-.md files should not be loaded."""
        docs = load_documents(str(mixed_md_dir))
        for doc in docs:
            # Ensure no .csv data bleeds in
            assert "a,b,c" not in doc.page_content

    def test_empty_directory_returns_empty_list(self, empty_md_dir):
        """An empty directory should return an empty list."""
        docs = load_documents(str(empty_md_dir))
        assert docs == []

    def test_nonexistent_directory_raises(self):
        """Passing a nonexistent directory should raise an appropriate error."""
        with pytest.raises((FileNotFoundError, ValueError)):
            load_documents("/nonexistent/path/to/nothing")
