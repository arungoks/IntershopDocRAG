"""
tests/scraper/test_parser.py
----------------------------
Unit tests for HTML to Markdown parser and metadata injector.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from scraper.parser import MarkdownParser


class TestMarkdownParser:

    @pytest.fixture
    def parser(self, tmp_path: Path):
        return MarkdownParser(output_dir=tmp_path)

    def test_parses_html_with_metadata(self, parser: MarkdownParser, tmp_path: Path):
        """AC: #2, #3, #5, #6 - HTML is parsed, metadata generated, and saved to disk."""
        target_url = "https://knowledge.intershop.com/article1"
        html = '''
        <html>
            <head><title>Intershop Article</title></head>
            <body>
                <h1>Intershop Article</h1>
                <p>This is test content.</p>
                <table><tr><td>Data</td></tr></table>
            </body>
        </html>
        '''
        
        output_file = parser.parse_and_save(target_url, html)
        assert output_file is not None
        assert os.path.exists(output_file)
        
        # Verify file contents
        content = Path(output_file).read_text(encoding="utf-8")
        
        # Verify frontmatter
        assert "---" in content
        assert "id: '" in content
        assert "title: 'Intershop Article'" in content
        assert f"url: '{target_url}'" in content
        assert "scraped_at:" in content
        
        # Verify Markdown mapping extracted standard tags
        assert "Data" in content

    def test_empty_trafilatura_extraction_returns_none(self, parser: MarkdownParser):
        """AC: #7 - Null HTML fails cleanly."""
        html = "<html><body></body></html>"
        url = "https://blank.test"
        
        assert parser.parse_and_save(url, html) is None

    def test_absolutizes_markdown_links(self, parser: MarkdownParser):
        """AC: #4 - Internal links are rewritten to absolute."""
        url = "https://knowledge.intershop.com/path/"
        
        md_content = "This is a [relative link](/some/other/page.html) and [anchor](#top)."
        
        result = parser._absolutize_markdown_links(md_content, url)
        
        assert "[relative link](https://knowledge.intershop.com/some/other/page.html)" in result
        assert "[anchor](#top)" in result # Ignored properly
