"""
scraper/fetcher.py
------------------
Asynchronous HTTP fetcher with rate limiting and exponential backoff.
"""

from __future__ import annotations

import asyncio
from typing import Dict, List, Optional, Tuple

import httpx
from rich.console import Console

from scraper.auth import authenticate
from scraper.state import StateManager
from scraper.parser import MarkdownParser

console = Console()


class AsyncFetcher:
    """Fetches URLs concurrently using rate limits, retries, and checkpointing."""

    def __init__(
        self,
        cookies: Dict[str, str],
        state_manager: StateManager,
        max_concurrent: int = 5,
        max_retries: int = 3,
        base_backoff: float = 2.0
    ) -> None:
        """Initialize the fetching engine.

        Parameters
        ----------
        cookies:
            Authenticated cookies from the Entra ID flow.
        state_manager:
            Instance tracking scraped states.
        max_concurrent:
            Maximum concurrent requests (semaphore limit).
        max_retries:
            Maximum attempts for 429/50x errors before hard failure.
        base_backoff:
            Base exponential backoff time in seconds.
        """
        self.cookies = cookies
        self.state = state_manager
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.max_retries = max_retries
        self.base_backoff = base_backoff
        self.parser = MarkdownParser()
        self._auth_lock = asyncio.Lock()
        self._auth_generation = 0
        self._failed_auth_consecutive = 0



    async def fetch_url(self, client: httpx.AsyncClient, url: str) -> Tuple[str, Optional[str]]:
        """Fetch a single URL with exponential backoff retry logic.

        Parameters
        ----------
        client:
            The shared HTTP client.
        url:
            Target to fetch.

        Returns
        -------
        Tuple[str, Optional[str]]
            Tuple of (URL, Saved Markdown Path or None if failed).
        """
        if self.state.should_skip(url):
            console.print(f"[dim]Skipping (already complete): {url}[/dim]")
            return url, None

        retries = 0
        while retries <= self.max_retries:
            current_auth_gen = self._auth_generation
            async with self.semaphore:
                try:
                    response = await client.get(url, timeout=30.0)
                    
                    if response.status_code in (401, 403):
                        console.print(f"[bold red]Authentication error ({response.status_code}) on {url}[/bold red]")
                        
                        async with self._auth_lock:
                            if self._auth_generation > current_auth_gen:
                                # Another task successfully re-authenticated
                                client.cookies = self.cookies
                            else:
                                if self._failed_auth_consecutive >= 2:
                                    self.state.save()
                                    raise RuntimeError("Critical Pipeline Halt: Authentication failed completely after 2 retries.")
                                    
                                console.print("[bold yellow]Attempting re-authentication...[/bold yellow]")
                                try:
                                    self.cookies = await authenticate()
                                    client.cookies = self.cookies
                                    self._auth_generation += 1
                                    self._failed_auth_consecutive += 1
                                    console.print("[bold green]Re-authentication successful. Resuming fetch.[/bold green]")
                                except Exception as e:
                                    console.print(f"[bold red]Re-authentication failed: {e}[/bold red]")
                                    self._failed_auth_consecutive += 1
                                    if self._failed_auth_consecutive >= 2:
                                        self.state.save()
                                        raise RuntimeError(f"Critical Pipeline Halt: Authentication failed completely after 2 retries. ({e})")
                        continue

                    # Trigger retries for rate limits or server errors
                    if response.status_code in (429, 502, 503, 504):
                        retries += 1
                        if retries > self.max_retries:
                            console.print(f"[bold red]Max retries exceeded on {url}[/bold red]")
                            self.state.update_status(url, "failed", retries)
                            response.raise_for_status()
                            
                        # Respect Retry-After header if present on 429
                        retry_after = response.headers.get("Retry-After")
                        if retry_after and retry_after.isdigit():
                            sleep_time = float(retry_after)
                        else:
                            sleep_time = self.base_backoff * (2 ** (retries - 1))
                            
                        console.print(f"[yellow]Rate/Server limit ({response.status_code}) hit on {url}. Retrying in {sleep_time}s ([{retries}/{self.max_retries}])...[/yellow]")
                        await asyncio.sleep(sleep_time)
                        continue
                    
                    # Raise on other HTTP errors automatically
                    response.raise_for_status()
                    self._failed_auth_consecutive = 0
                    
                    # Instead of immediately marking as success, parse to markdown
                    md_path = self.parser.parse_and_save(url, response.text)
                    if md_path:
                        self.state.update_status(url, "success", retries)
                        return url, md_path
                    else:
                        self.state.update_status(url, "failed", retries)
                        return url, None
                    
                except httpx.RequestError as exc:
                    retries += 1
                    if retries > self.max_retries:
                        console.print(f"[bold red]Network failure on {exc.request.url!r}. Giving up.[/bold red]")
                        self.state.update_status(url, "failed", retries)
                        return url, None
                        
                    sleep_time = self.base_backoff * (2 ** (retries - 1))
                    console.print(f"[yellow]Network timeout/error on {url}. Retrying in {sleep_time}s...[/yellow]")
                    await asyncio.sleep(sleep_time)
                except httpx.HTTPStatusError as exc:
                    if exc.response.status_code not in (429, 502, 503, 504, 401, 403):
                        console.print(f"[bold red]Client error {exc.response.status_code} on {url}. Failed.[/bold red]")
                        self.state.update_status(url, "failed", retries)
                        return url, None
                    # For 401/403, we let the logic at the top of the loop handle it.
                    # For other retryable errors, we just continue the loop.
                    if exc.response.status_code in (401, 403):
                        # This is already handled above, but as a fallback, we continue the loop
                        continue
                    raise

        self.state.update_status(url, "failed", retries)
        return url, None

    async def fetch_urls(self, urls: List[str], progress_callback=None) -> Dict[str, str]:
        """Fetch a list of URLs concurrently within bounds of the semaphore.

        Parameters
        ----------
        urls:
            Queue of target URLs.
        progress_callback:
            Optional callback invoked with the result of each fetch.

        Returns
        -------
        Dict[str, str]
            Dictionary connecting URLs to their raw downloaded HTML.
        """
        results: Dict[str, str] = {}
        
        async with httpx.AsyncClient(cookies=self.cookies) as client:
            tasks = [asyncio.create_task(self.fetch_url(client, url)) for url in urls]
            
            for coro in asyncio.as_completed(tasks):
                try:
                    res = await coro
                    if isinstance(res, tuple):
                        url, content = res
                        if content is not None:
                            results[url] = content
                        if progress_callback:
                            progress_callback(url, True if content else False)
                except Exception as e:
                    console.print(f"[bold red]Unexpected failure in worker task: {e}[/bold red]")
                    if progress_callback:
                        progress_callback(None, False)
                    
        return results
