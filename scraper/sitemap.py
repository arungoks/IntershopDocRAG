"""
scraper/sitemap.py
------------------
Sitemap parsing and URL queue generation logic.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Dict, List

import httpx
from rich.console import Console

console = Console()

import io

async def fetch_sitemap_urls(sitemap_url: str, cookies: Dict[str, str]) -> List[str]:
    """Fetch and parse a sitemap XML to extract all URLs under <loc>.

    Parameters
    ----------
    sitemap_url:
        URL to the sitemap XML file.
    cookies:
        Authenticated session cookies as a dictionary.

    Returns
    -------
    List[str]
        Ordered list of extracted URLs.

    Raises
    ------
    httpx.RequestError
        If a network/reachability issue occurs.
    httpx.HTTPStatusError
        If a non-success HTTP status was returned.
    RuntimeError
        If parsing the XML fails.
    """
    async with httpx.AsyncClient(cookies=cookies) as client:
        try:
            response = await client.get(sitemap_url, timeout=30.0)
            response.raise_for_status()
        except httpx.RequestError as exc:
            console.print(f"[bold red]Network error while requesting {exc.request.url!r}.[/bold red]")
            raise
        except httpx.HTTPStatusError as exc:
            console.print(
                f"[bold red]HTTP error {exc.response.status_code} while requesting {exc.request.url!r}.[/bold red]"
            )
            raise

    try:
        root = ET.fromstring(response.text)
    except ET.ParseError as exc:
        console.print("[bold red]Failed to parse sitemap XML.[/bold red]")
        raise RuntimeError(f"XML parsing failed: {exc}") from exc

    # Handle standard sitemap namespaces gracefully
    ns_map = {}
    if "xmlns=" in response.text:
        # Simple extraction of default namespace to query elements cleanly
        try:
            namespaces = dict([
                node for _, node in ET.iterparse(
                    io.BytesIO(response.content), events=["start-ns"]
                )
            ])
            if "" in namespaces:
                ns_map["ns"] = namespaces[""]
        except Exception:
            pass

    urls: List[str] = []
    
    # Check for direct sitemap <url> entries
    url_tag = "ns:url/ns:loc" if "ns" in ns_map else "url/loc"
    elements = root.findall(url_tag, ns_map)
    
    if not elements:
        # Check if root elements lack parent namespace wrap (poorly formatted XML)
        # Using string matching just in case
        for el in root.iter():
            tag_name = el.tag.split("}")[-1] if "}" in el.tag else el.tag
            if tag_name == "loc" and el.text:
                urls.append(el.text.strip())
    else:
        for loc in elements:
            if loc.text:
                urls.append(loc.text.strip())
                
    console.print(f"[bold green]Discovered {len(urls)} URLs from sitemap.[/bold green]")
    return urls
