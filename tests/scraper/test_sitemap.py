"""
tests/scraper/test_sitemap.py
-----------------------------
Unit tests for the sitemap fetching and parsing logic.
"""

from __future__ import annotations

import httpx
import pytest
from unittest.mock import AsyncMock

from scraper.sitemap import fetch_sitemap_urls


@pytest.fixture
def mock_httpx_client():
    """Fixture providing a mocked httpx.AsyncClient."""
    from unittest.mock import patch, AsyncMock
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client_ctx = AsyncMock()
    mock_client_ctx.__aenter__.return_value = mock_client
    mock_client_ctx.__aexit__.return_value = None
    
    with patch("scraper.sitemap.httpx.AsyncClient", return_value=mock_client_ctx):
        yield mock_client

import asyncio

class TestSitemapParser:
    
    def test_successful_fetch_and_parse(self, mock_httpx_client):
        """AC: #3, #4 - Valid XML is fetched and parsed correctly."""
        xml_content = b'''<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
           <url>
              <loc>https://knowledge.intershop.com/page1</loc>
           </url>
           <url>
              <loc>https://knowledge.intershop.com/page2</loc>
           </url>
        </urlset>'''
        
        mock_response = AsyncMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.content = xml_content
        mock_response.text = xml_content.decode("utf-8")
        mock_response.raise_for_status.return_value = None
        
        mock_httpx_client.get.return_value = mock_response
        
        cookies = {"session_id": "test"}
        urls = asyncio.run(fetch_sitemap_urls("https://example.com/sitemap.xml", cookies=cookies))
        
        assert len(urls) == 2
        assert urls[0] == "https://knowledge.intershop.com/page1"
        assert urls[1] == "https://knowledge.intershop.com/page2"
        mock_httpx_client.get.assert_called_once_with("https://example.com/sitemap.xml", timeout=30.0)

    def test_parse_without_namespace(self, mock_httpx_client):
        """Handle sitemaps that incorrectly omit the namespace."""
        xml_content = b'''<?xml version="1.0" encoding="UTF-8"?>
        <urlset>
           <url><loc>https://example.com/a</loc></url>
        </urlset>'''
        
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.content = xml_content
        mock_response.text = xml_content.decode("utf-8")
        
        mock_httpx_client.get.return_value = mock_response
        
        urls = asyncio.run(fetch_sitemap_urls("https://example.com/sitemap", {}))
        assert urls == ["https://example.com/a"]

    def test_http_error_raised(self, mock_httpx_client):
        """AC: #6 - HTTPStatusError correctly raised and logged."""
        mock_response = AsyncMock(spec=httpx.Response)
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "404 Not Found", request=AsyncMock(), response=mock_response
        )
        
        mock_httpx_client.get.return_value = mock_response
        
        with pytest.raises(httpx.HTTPStatusError):
            asyncio.run(fetch_sitemap_urls("https://example.com/sitemap.xml", {}))

    def test_malformed_xml_raised(self, mock_httpx_client):
        """Malformed XML raises RuntimeError."""
        xml_content = b'''Not XML'''
        
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.content = xml_content
        mock_response.text = xml_content.decode("utf-8")
        
        mock_httpx_client.get.return_value = mock_response
        
        with pytest.raises(RuntimeError):
            asyncio.run(fetch_sitemap_urls("https://example.com/sitemap.xml", {}))
