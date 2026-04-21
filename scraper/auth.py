"""
scraper/auth.py
---------------
Headless Microsoft Entra ID / OAuth authentication module.

Playwright is the ONLY module in the project that may import from
`playwright.async_api`. No other module in this codebase should touch
Playwright directly.

Usage:
    import asyncio
    from scraper.auth import authenticate

    cookies = asyncio.run(authenticate())
    # cookies is a dict suitable for httpx.AsyncClient(cookies=cookies)
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Dict

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

async def authenticate(creds_path: str | Path = "creds.txt") -> Dict[str, str]:
    """Authenticate against Microsoft Entra ID and return session cookies.

    Parameters
    ----------
    creds_path:
        Path to the plain-text credentials file. Line 1 = username/email,
        line 2 = password. Defaults to ``"creds.txt"`` in the current
        working directory.

    Returns
    -------
    dict
        A mapping of cookie name → value usable by ``httpx.AsyncClient``.

    Raises
    ------
    FileNotFoundError
        If ``creds_path`` does not exist.
    ValueError
        If the credentials file is empty or malformed (fewer than 2 lines,
        or blank username / password).
    RuntimeError
        If authentication fails (wrong credentials, unexpected redirect, etc.)
    """
    username, password = _load_credentials(creds_path)
    cookies = await _run_playwright_auth(username, password)
    return cookies


# ---------------------------------------------------------------------------
# Credential loading (Task 2)
# ---------------------------------------------------------------------------

def _load_credentials(creds_path: str | Path) -> tuple[str, str]:
    """Read and validate credentials from *creds_path*.

    Returns
    -------
    tuple[str, str]
        ``(username, password)``

    Raises
    ------
    FileNotFoundError
        If the file does not exist at *creds_path*.
    ValueError
        If the file has fewer than 2 non-empty lines.
    """
    path = Path(creds_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Credentials file not found: '{path.resolve()}'. "
            "Create a 'creds.txt' file with your username on line 1 and "
            "password on line 2."
        )

    lines = path.read_text(encoding="utf-8").splitlines()

    # Strip blank lines and surrounding whitespace
    stripped = [line.strip() for line in lines if line.strip()]

    if len(stripped) < 2:
        raise ValueError(
            f"Credentials file '{path}' is malformed. "
            "Expected at least 2 non-empty lines: line 1 = username, "
            "line 2 = password."
        )

    username, password = stripped[0], stripped[1]
    return username, password


# ---------------------------------------------------------------------------
# Playwright authentication flow (Task 3)
# ---------------------------------------------------------------------------

async def _run_playwright_auth(username: str, password: str) -> Dict[str, str]:
    """Spin up a headless Chromium browser and complete the Entra ID OAuth flow.

    Parameters
    ----------
    username:
        Microsoft account email / UPN.
    password:
        Microsoft account password.

    Returns
    -------
    dict
        Cookies extracted from the browser context after successful login,
        formatted as ``{name: value}`` for use with ``httpx``.

    Raises
    ------
    RuntimeError
        If the authentication flow does not result in landing on the
        protected Knowledge Base domain.
    """
    # ------------------------------------------------------------------ #
    # Playwright is imported HERE and ONLY here (AC #4).                  #
    # ------------------------------------------------------------------ #
    TARGET_DOMAIN = "knowledge.intershop.com"
    LOGIN_URL = "https://knowledge.intershop.com/kb/index.php/Account?qdo=LogOn"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # -- 1. Navigate to the protected resource -----------------------
            await page.goto(LOGIN_URL, wait_until="networkidle", timeout=45_000)

            # -- 2. Enter username -------------------------------------------
            # Since Microsoft forms can vary, wait for *any* text input first
            await page.wait_for_selector('input[type="email"], input[name="loginfmt"], input[type="text"]', timeout=20_000)
            
            # Now explicitly fill
            username_field = page.locator('input[type="email"], input[name="loginfmt"], input[type="text"]').first
            await username_field.fill(username)
            
            # Click next
            await page.locator('input[type="submit"], button[type="submit"], #idSIButton9').first.click()

            # -- 3. Enter password -------------------------------------------
            await page.wait_for_selector('input[name="passwd"], input[type="password"]', timeout=20_000)
            await page.locator('input[name="passwd"], input[type="password"]').first.fill(password)
            await page.locator('input[type="submit"], button[type="submit"], #idSIButton9').first.click()

            # -- 4. Handle "Stay signed in?" prompt (optional) ---------------
            try:
                stay_signed_in = await page.wait_for_selector(
                    'input[type="submit"], button[type="submit"], #idSIButton9', timeout=10_000
                )
                if stay_signed_in:
                    await stay_signed_in.click()
            except PlaywrightTimeoutError:
                # Prompt did not appear — that is fine
                pass

            # -- 5. Wait for redirect to the Knowledge Base ------------------
            try:
                await page.wait_for_url(
                    f"**{TARGET_DOMAIN}**", timeout=30_000
                )
            except PlaywrightTimeoutError as exc:
                current_url = page.url
                raise RuntimeError(
                    f"Authentication failed: expected redirect to "
                    f"'{TARGET_DOMAIN}' but landed on '{current_url}'. "
                    f"Content snippet: {(await page.content())[:200]}"
                ) from exc

            # -- 6. Extract cookies ------------------------------------------
            browser_cookies = await context.cookies()
            httpx_cookies: Dict[str, str] = {
                c["name"]: c["value"] for c in browser_cookies
            }

        except Exception as outer_exc:
            await page.screenshot(path="playwright_error_auth.png")
            with open("playwright_error_auth.html", "w", encoding="utf-8") as f:
                f.write(await page.content())
            raise outer_exc

        finally:
            await context.close()
            await browser.close()

    if not httpx_cookies:
        raise RuntimeError(
            "Authentication appeared to succeed but no cookies were extracted. "
            "The session may not have been persisted correctly."
        )

    return httpx_cookies
