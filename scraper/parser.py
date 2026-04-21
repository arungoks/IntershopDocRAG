"""
scraper/parser.py
-----------------
Converts raw HTML pages into Markdown artifacts with YAML frontmatter.
"""

from __future__ import annotations

import hashlib
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

import trafilatura
from rich.console import Console

console = Console()

class MarkdownParser:
    """Handles HTML to Markdown conversion, metadata injection, and persistence."""

    def __init__(self, output_dir: str | Path = "data/raw_md") -> None:
        """Initialize the Markdown parser.

        Parameters
        ----------
        output_dir:
            The directory to save generated markdown files.
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _generate_page_id(self, url: str) -> str:
        """Generate a universally unique ID from the URL."""
        # We use an md5 hash of the URL to ensure file system safety and uniqueness
        return hashlib.md5(url.encode("utf-8")).hexdigest()
        
    def _absolutize_markdown_links(self, markdown: str, base_url: str) -> str:
        """Find relative URLs in Markdown and convert them to absolute URLs.
        
        Regex matches standard Markdown format: [text](/path/to/thing)
        """
        def repl_func(match: re.Match) -> str:
            text = match.group(1)
            link = match.group(2)
            # if it's an anchor, mailto, or already http/https, ignore. 
            if link.startswith(('http://', 'https://', '#', 'mailto:')):
                return match.group(0)
            
            abs_link = urljoin(base_url, link)
            return f"[{text}]({abs_link})"
            
        return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl_func, markdown)

    def parse_and_save(self, url: str, html: str) -> Optional[str]:
        """Convert HTML to frontmatter Markdown and save to disk.

        Parameters
        ----------
        url:
            Original absolute URL.
        html:
            Raw fetched HTML payload.

        Returns
        -------
        Optional[str]
            The saved file path if successful, None if it failed.
        """
        # Attempt extraction using trafilatura
        try:
            # Trafilatura extract natively supports markdown
            content = trafilatura.extract(
                html,
                url=url,
                include_links=True,
                include_tables=True,
                output_format="markdown",
            )
            
            if not content:
                console.print(f"[bold yellow]Warning: Trafilatura extracted empty content for {url}[/bold yellow]")
                return None
                
            # Safely capture metadata like Title using Trafilatura's native meta parser
            metadata = trafilatura.extract_metadata(html)
            title = metadata.title if metadata and metadata.title else "Untitled Page"
            
        except Exception as exc:
            console.print(f"[bold red]Failed to run Trafilatura extraction on {url}: {exc}[/bold red]")
            return None

        # Resolve relative URLs to absolute Intershop URLs strictly inside the Markdown payload
        processed_content = self._absolutize_markdown_links(content, url)

        # Generate unique ID and metadata footprint
        page_id = self._generate_page_id(url)
        scraped_at = datetime.now(timezone.utc).isoformat()
        
        # Build strict YAML Frontmatter
        frontmatter = [
            "---",
            f"id: '{page_id}'",
            f"title: '{title.replace(chr(39), chr(39)+chr(39))}'", # Escape single quotes
            f"url: '{url}'",
            f"scraped_at: '{scraped_at}'",
            "---\n"
        ]
        
        final_markdown = "\n".join(frontmatter) + processed_content
        
        # Safe save output path
        output_path = self.output_dir / f"{page_id}.md"
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(final_markdown)
        except IOError as exc:
            console.print(f"[bold red]Disk Write Error for {output_path}: {exc}[/bold red]")
            return None
            
        return str(output_path)
