"""
tests/scraper/test_auth.py
--------------------------
Unit tests for scraper/auth.py

Coverage:
- _load_credentials: happy path, missing file, malformed file
- authenticate: end-to-end with mocked Playwright
- Playwright isolation: no other module imports playwright

AC mapping:
  AC#1  → test_playwright_flow_navigates_and_authenticates
  AC#2  → test_authenticate_returns_httpx_compatible_dict
  AC#3  → test_missing_creds_file / test_malformed_creds_file
  AC#4  → test_playwright_is_isolated_to_auth_module
"""

from __future__ import annotations

import asyncio
import importlib
import sys
import types
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch, PropertyMock

import pytest

import scraper.auth

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_creds(tmp_path: Path, content: str) -> Path:
    """Write *content* to a temporary creds.txt and return its path."""
    p = tmp_path / "creds.txt"
    p.write_text(content, encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Tests for _load_credentials (AC #3)
# ---------------------------------------------------------------------------

class TestLoadCredentials:
    """Unit tests for the credential-loading helper."""

    def test_happy_path_returns_username_and_password(self, tmp_path: Path):
        """Valid creds.txt returns (username, password) tuple."""
        from scraper.auth import _load_credentials

        creds = _write_creds(tmp_path, "user@example.com\nmysecretpass\n")
        username, password = _load_credentials(creds)

        assert username == "user@example.com"
        assert password == "mysecretpass"

    def test_strips_whitespace_from_credentials(self, tmp_path: Path):
        """Leading/trailing whitespace on credential lines is stripped."""
        from scraper.auth import _load_credentials

        creds = _write_creds(tmp_path, "  user@example.com  \n  mysecretpass  \n")
        username, password = _load_credentials(creds)

        assert username == "user@example.com"
        assert password == "mysecretpass"

    def test_extra_lines_are_ignored(self, tmp_path: Path):
        """Lines beyond line 2 are silently ignored."""
        from scraper.auth import _load_credentials

        creds = _write_creds(tmp_path, "user@example.com\nmysecretpass\nextraline\n")
        username, password = _load_credentials(creds)

        assert username == "user@example.com"
        assert password == "mysecretpass"

    def test_missing_file_raises_file_not_found(self, tmp_path: Path):
        """AC #3: missing creds.txt raises FileNotFoundError with clear message."""
        from scraper.auth import _load_credentials

        non_existent = tmp_path / "creds.txt"
        with pytest.raises(FileNotFoundError) as exc_info:
            _load_credentials(non_existent)

        assert "creds.txt" in str(exc_info.value).lower() or "credentials" in str(exc_info.value).lower()

    def test_empty_file_raises_value_error(self, tmp_path: Path):
        """AC #3: empty creds.txt raises ValueError with clear message."""
        from scraper.auth import _load_credentials

        creds = _write_creds(tmp_path, "")
        with pytest.raises(ValueError) as exc_info:
            _load_credentials(creds)

        assert "malformed" in str(exc_info.value).lower() or "2" in str(exc_info.value)

    def test_single_line_file_raises_value_error(self, tmp_path: Path):
        """AC #3: only username present (no password) raises ValueError."""
        from scraper.auth import _load_credentials

        creds = _write_creds(tmp_path, "user@example.com\n")
        with pytest.raises(ValueError):
            _load_credentials(creds)

    def test_blank_lines_only_raises_value_error(self, tmp_path: Path):
        """AC #3: file with only whitespace/blank lines raises ValueError."""
        from scraper.auth import _load_credentials

        creds = _write_creds(tmp_path, "\n\n\n")
        with pytest.raises(ValueError):
            _load_credentials(creds)


# ---------------------------------------------------------------------------
# Tests for _run_playwright_auth (AC #1, #2)
# ---------------------------------------------------------------------------

def _make_playwright_mock(
    *,
    final_url: str = "https://knowledge.intershop.com/home",
    cookies: list[dict] | None = None,
    stay_signed_in_appears: bool = True,
) -> tuple[MagicMock, MagicMock]:
    """Build a minimal Playwright async mock tree.

    Returns
    -------
    (mock_playwright_ctx, mock_page)
        ``mock_playwright_ctx`` is the object returned by ``async_playwright()``.
    """
    if cookies is None:
        cookies = [
            {"name": "session_id", "value": "abc123"},
            {"name": "auth_token", "value": "tok456"},
        ]

    # Page mock
    mock_page = AsyncMock()
    mock_page.url = final_url

    # wait_for_url: success by default
    mock_page.wait_for_url = AsyncMock()

    # wait_for_selector: returns a clickable element mock
    mock_submit = AsyncMock()
    mock_page.wait_for_selector = AsyncMock(return_value=mock_submit)

    # Context mock
    mock_context = AsyncMock()
    mock_context.new_page = AsyncMock(return_value=mock_page)
    mock_context.cookies = AsyncMock(return_value=cookies)

    # Browser mock
    mock_browser = AsyncMock()
    mock_browser.new_context = AsyncMock(return_value=mock_context)

    # Chromium mock
    mock_chromium = AsyncMock()
    mock_chromium.launch = AsyncMock(return_value=mock_browser)

    # Playwright instance (the "p" in `async with async_playwright() as p`)
    mock_p = MagicMock()
    mock_p.chromium = mock_chromium

    # async_playwright() context manager
    mock_playwright_cm = AsyncMock()
    mock_playwright_cm.__aenter__ = AsyncMock(return_value=mock_p)
    mock_playwright_cm.__aexit__ = AsyncMock(return_value=False)

    return mock_playwright_cm, mock_page


class TestRunPlaywrightAuth:
    """Unit tests for the Playwright authentication flow."""

    def test_authenticate_returns_httpx_compatible_dict(self, tmp_path: Path):
        """AC #2: returned value is a plain dict of {str: str} cookie pairs."""
        mock_cm, _ = _make_playwright_mock()
        creds = _write_creds(tmp_path, "user@example.com\nmysecretpass\n")

        with patch("scraper.auth.async_playwright", return_value=mock_cm):
            # Import here to trigger the lazy `from playwright.async_api import ...`
            import importlib, scraper.auth as auth_mod
            result = asyncio.run(auth_mod.authenticate(creds))

        assert isinstance(result, dict)
        assert all(isinstance(k, str) and isinstance(v, str) for k, v in result.items())
        assert result == {"session_id": "abc123", "auth_token": "tok456"}

    def test_playwright_flow_fills_username_and_password(self, tmp_path: Path):
        """AC #1: the flow calls page.fill() for both email and password fields."""
        mock_cm, mock_page = _make_playwright_mock()
        creds = _write_creds(tmp_path, "user@example.com\nmysecretpass\n")

        with patch("scraper.auth.async_playwright", return_value=mock_cm):
            import scraper.auth as auth_mod
            asyncio.run(auth_mod.authenticate(creds))

        fill_calls = [str(c) for c in mock_page.fill.call_args_list]
        assert any("user@example.com" in c for c in fill_calls)
        assert any("mysecretpass" in c for c in fill_calls)

    def test_authenticate_raises_runtime_error_on_wrong_redirect(self, tmp_path: Path):
        """AC #1, #3: RuntimeError is raised when final URL is not the KB domain."""
        from playwright.async_api import TimeoutError as PlaywrightTimeoutError

        mock_cm, mock_page = _make_playwright_mock(
            final_url="https://login.microsoftonline.com/error"
        )
        # Simulate wait_for_url raising because we never land on the KB domain
        mock_page.wait_for_url = AsyncMock(
            side_effect=PlaywrightTimeoutError("timed out")
        )
        creds = _write_creds(tmp_path, "user@example.com\nwrongpassword\n")

        with patch("scraper.auth.async_playwright", return_value=mock_cm):
            import scraper.auth as auth_mod
            with pytest.raises(RuntimeError) as exc_info:
                asyncio.run(auth_mod.authenticate(creds))

        assert "authentication failed" in str(exc_info.value).lower()

    def test_stay_signed_in_timeout_is_handled_gracefully(self, tmp_path: Path):
        """AC #1: TimeoutError on 'Stay signed in?' prompt is silently swallowed."""
        from playwright.async_api import TimeoutError as PlaywrightTimeoutError

        mock_cm, mock_page = _make_playwright_mock()

        call_count = [0]

        async def selective_wait_for_selector(selector, **kwargs):
            """Raise PlaywrightTimeoutError only on the 3rd call (Stay signed in?)."""
            call_count[0] += 1
            if call_count[0] == 3:  # 3rd selector wait = stay-signed-in prompt
                raise PlaywrightTimeoutError("Prompt did not appear")
            return AsyncMock()

        mock_page.wait_for_selector = selective_wait_for_selector
        creds = _write_creds(tmp_path, "user@example.com\nmysecretpass\n")

        with patch("scraper.auth.async_playwright", return_value=mock_cm):
            import scraper.auth as auth_mod
            # Should NOT raise — missing prompt is expected behaviour
            result = asyncio.run(auth_mod.authenticate(creds))

        assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# Architecture test: Playwright isolation (AC #4)
# ---------------------------------------------------------------------------

class TestPlaywrightIsolation:
    """Ensure Playwright is imported nowhere except scraper/auth.py."""

    PLAYWRIGHT_MODULES = frozenset({
        "playwright",
        "playwright.async_api",
        "playwright.sync_api",
    })

    def _get_project_python_files(self, root: Path) -> list[Path]:
        """Collect all .py files that are production code (skip tests & __pycache__)."""
        return [
            p for p in root.rglob("*.py")
            if "__pycache__" not in p.parts
            and "tests" not in p.parts
            and ".venv" not in p.parts
            and p.name != "auth.py"  # auth.py is allowed
        ]

    def test_no_other_module_imports_playwright(self):
        """AC #4: scanning source tree for any playwright import outside auth.py."""
        import ast

        project_root = Path(__file__).parents[2]  # …/IntershopRAG/
        py_files = self._get_project_python_files(project_root)

        violations: list[str] = []
        for py_file in py_files:
            try:
                source = py_file.read_text(encoding="utf-8")
                tree = ast.parse(source, filename=str(py_file))
            except (SyntaxError, UnicodeDecodeError):
                continue

            for node in ast.walk(tree):
                # Detect: import playwright / import playwright.async_api
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.startswith("playwright"):
                            violations.append(f"{py_file}: import {alias.name}")
                # Detect: from playwright... import ...
                if isinstance(node, ast.ImportFrom):
                    if node.module and node.module.startswith("playwright"):
                        violations.append(
                            f"{py_file}: from {node.module} import ..."
                        )

        assert violations == [], (
            "Playwright import found outside scraper/auth.py:\n"
            + "\n".join(violations)
        )
