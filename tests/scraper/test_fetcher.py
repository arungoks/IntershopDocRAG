"""
tests/scraper/test_fetcher.py
-----------------------------
Unit tests for the AsyncFetcher engine.
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from scraper.fetcher import AsyncFetcher
from scraper.state import StateManager


class TestAsyncFetcher:

    @pytest.fixture
    def mock_state(self):
        state = AsyncMock(spec=StateManager)
        state.should_skip.return_value = False
        return state

    @pytest.fixture
    def mock_httpx_client(self):
        with patch("scraper.fetcher.httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock(spec=httpx.AsyncClient)
            mock_client_ctx = AsyncMock()
            mock_client_ctx.__aenter__.return_value = mock_client
            mock_client_ctx.__aexit__.return_value = None
            mock_client_cls.return_value = mock_client_ctx
            yield mock_client

    @patch("scraper.fetcher.MarkdownParser")
    def test_fetches_valid_url(self, mock_parser_cls, mock_state):
        """AC: #3 - Standard 200 GET triggers parser and stores 'success' state."""
        mock_parser = mock_parser_cls.return_value
        mock_parser.parse_and_save.return_value = "data/raw_md/something.md"
        
        fetcher = AsyncFetcher({"cookie": "x"}, mock_state)
        # Ensure instances bind properly testing isolated logic
        fetcher.parser = mock_parser
        
        mock_response = AsyncMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.text = "<html>content</html>"
        mock_response.raise_for_status.return_value = None
        
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_client.get.return_value = mock_response

        url, content = asyncio.run(fetcher.fetch_url(mock_client, "http://test.com"))
        
        assert content == "data/raw_md/something.md"
        mock_parser.parse_and_save.assert_called_once_with("http://test.com", "<html>content</html>")
        mock_state.update_status.assert_called_once_with("http://test.com", "success", 0)

    @patch("scraper.fetcher.MarkdownParser")
    def test_parser_failure_marks_failed(self, mock_parser_cls, mock_state):
        """AC: #7 (from Story 2.5) - Parser failure logs failure in state."""
        mock_parser = mock_parser_cls.return_value
        mock_parser.parse_and_save.return_value = None
        
        fetcher = AsyncFetcher({"cookie": "x"}, mock_state)
        fetcher.parser = mock_parser
        
        mock_response = AsyncMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.text = "<html>fail me</html>"
        
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        url, content = asyncio.run(fetcher.fetch_url(mock_client, "http://test.com"))
        
        assert content is None
        mock_state.update_status.assert_called_once_with("http://test.com", "failed", 0)

    def test_skips_processed_url(self, mock_state):
        """AC: #6 - Skip already-checked state keys."""
        mock_state.should_skip.return_value = True
        fetcher = AsyncFetcher({"cookie": "x"}, mock_state)
        
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        url, content = asyncio.run(fetcher.fetch_url(mock_client, "http://test.com"))
        
        assert content is None
        mock_client.get.assert_not_called()

    @patch("scraper.fetcher.asyncio.sleep", new_callable=AsyncMock)
    def test_retries_on_rate_limit(self, mock_sleep, mock_state):
        """AC: #4, #5 - Retries 429 and updates state to 'failed' on max out."""
        fetcher = AsyncFetcher({"cookie": "x"}, mock_state, max_retries=2)
        
        mock_response = AsyncMock(spec=httpx.Response)
        mock_response.status_code = 429
        mock_response.headers = {}
        # mock HTTPStatusError on raise_for_status
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError("Limit", request=AsyncMock(), response=mock_response)
        
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        with pytest.raises(httpx.HTTPStatusError):
            asyncio.run(fetcher.fetch_url(mock_client, "http://test.com"))
            
        assert mock_client.get.call_count == 3  # initial + 2 retries
        assert mock_sleep.call_count == 2
        mock_state.update_status.assert_called_with("http://test.com", "failed", 3)

    def test_aborts_on_404_instantly(self, mock_state):
        """Standard errors (404, 500 without retry backoff) fail immediately."""
        fetcher = AsyncFetcher({"cookie": "x"}, mock_state)
        
        mock_response = AsyncMock(spec=httpx.Response)
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError("Not Found", request=AsyncMock(), response=mock_response)
        
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        url, content = asyncio.run(fetcher.fetch_url(mock_client, "http://test.com"))
        
        assert content is None
        assert mock_client.get.call_count == 1
        mock_state.update_status.assert_called_once_with("http://test.com", "failed", 0)

