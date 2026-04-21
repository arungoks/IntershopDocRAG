"""
tests/scraper/test_fetcher_auth.py
----------------------------------
Tests for the AsyncFetcher's re-authentication logic.
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from scraper.fetcher import AsyncFetcher
from scraper.state import StateManager


class TestAsyncFetcherAuth:

    @pytest.fixture
    def mock_state(self):
        state = AsyncMock(spec=StateManager)
        state.should_skip.return_value = False
        return state

    @patch("scraper.fetcher.authenticate", new_callable=AsyncMock)
    @patch("scraper.fetcher.MarkdownParser")
    def test_reauthenticates_on_401_and_retries(self, mock_parser_cls, mock_authenticate, mock_state):
        """AC: #1, #2, #4, #5, #6 - On 401, re-authenticate, update cookies, and retry."""
        # Arrange
        mock_parser = mock_parser_cls.return_value
        mock_parser.parse_and_save.return_value = "data/raw_md/success.md"
        
        initial_cookies = {"session": "expired"}
        new_cookies = {"session": "valid"}
        mock_authenticate.return_value = new_cookies
        
        fetcher = AsyncFetcher(initial_cookies, mock_state)
        fetcher.parser = mock_parser

        # First response is 401, second is 200
        response_401 = AsyncMock(spec=httpx.Response)
        response_401.status_code = 401
        response_200 = AsyncMock(spec=httpx.Response)
        response_200.status_code = 200
        response_200.text = "<html>content</html>"
        
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_client.get.side_effect = [response_401, response_200]

        # Act
        url, content = asyncio.run(fetcher.fetch_url(mock_client, "http://test.com"))

        # Assert
        assert content == "data/raw_md/success.md"
        assert mock_client.get.call_count == 2
        mock_authenticate.assert_called_once()
        assert fetcher.cookies == new_cookies
        assert mock_client.cookies == new_cookies
        mock_state.update_status.assert_called_once_with("http://test.com", "success", 0)

    @patch("scraper.fetcher.authenticate", new_callable=AsyncMock)
    @patch("scraper.fetcher.MarkdownParser")
    def test_fails_after_max_reauth_attempts(self, mock_parser_cls, mock_authenticate, mock_state):
        """AC: #7 - If re-authentication fails repeatedly, the pipeline fails."""
        # Arrange
        mock_parser = mock_parser_cls.return_value
        
        initial_cookies = {"session": "expired"}
        mock_authenticate.side_effect = RuntimeError("Auth failed")
        
        fetcher = AsyncFetcher(initial_cookies, mock_state)
        fetcher.parser = mock_parser

        response_401 = AsyncMock(spec=httpx.Response)
        response_401.status_code = 401
        
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_client.get.return_value = response_401

        # Act & Assert
        with pytest.raises(RuntimeError, match="Critical Pipeline Halt: Authentication failed completely"):
            asyncio.run(fetcher.fetch_url(mock_client, "http://test.com"))

        assert mock_authenticate.call_count == 2
        mock_state.save.assert_called_once()

    @patch("scraper.fetcher.authenticate", new_callable=AsyncMock)
    @patch("scraper.fetcher.MarkdownParser")
    def test_auth_lock_prevents_concurrent_reauth(self, mock_parser_cls, mock_authenticate, mock_state):
        """AC: #3 - An asyncio.Lock prevents multiple concurrent re-authentication calls."""
        # Arrange
        mock_parser = mock_parser_cls.return_value
        mock_parser.parse_and_save.return_value = "data/raw_md/success.md"

        initial_cookies = {"session": "expired"}
        new_cookies = {"session": "valid"}
        
        async def slow_authenticate():
            await asyncio.sleep(0.1)
            return new_cookies
        
        mock_authenticate.side_effect = slow_authenticate
        
        fetcher = AsyncFetcher(initial_cookies, mock_state, max_concurrent=2)
        fetcher.parser = mock_parser

        response_401 = AsyncMock(spec=httpx.Response)
        response_401.status_code = 401
        
        response_200 = AsyncMock(spec=httpx.Response)
        response_200.status_code = 200
        response_200.raise_for_status.return_value = None
        
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        
        get_call_count = 0
        async def side_effect(*args, **kwargs):
            nonlocal get_call_count
            get_call_count += 1
            if get_call_count <= 2:
                # First two requests (concurrently) return 401
                return response_401
            # Subsequent retries return 200
            return response_200

        mock_client.get.side_effect = side_effect

        # Act
        async def run_concurrent_fetches():
            tasks = [
                fetcher.fetch_url(mock_client, "http://test.com/1"),
                fetcher.fetch_url(mock_client, "http://test.com/2")
            ]
            await asyncio.gather(*tasks)

        asyncio.run(run_concurrent_fetches())

        # Assert
        # Even though two URLs failed with 401, only one re-authentication call should have been made.
        assert mock_authenticate.call_count == 1
