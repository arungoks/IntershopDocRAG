"""
scraper/main.py
---------------
CLI Pipeline Orchestrator for IntershopRAG.
Delegates to modular scraping components while displaying real-time progress.
"""

import asyncio
import os
import signal
import sys
from typing import Optional

# Ensure that 'scraper' can be imported when running `python scraper/main.py`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rich.console import Console
from rich.progress import (
    BarColumn, 
    Progress, 
    SpinnerColumn, 
    TaskProgressColumn, 
    TextColumn, 
    TimeElapsedColumn
)
from rich.table import Table

from scraper.auth import authenticate
from scraper.fetcher import AsyncFetcher
from scraper.sitemap import fetch_sitemap_urls
from scraper.state import StateManager

err_console = Console(stderr=True)
console = Console()

async def run_pipeline() -> None:
    state_manager = StateManager("scrape_state.json")
    
    # Task 3: Graceful Teardown and Signal Handling
    def handle_sigint(signum, frame):
        err_console.print("\n[bold red]Pipeline interrupted by user (Ctrl+C). Saving state and exiting...[/bold red]")
        state_manager._save()
        sys.exit(130)
        
    signal.signal(signal.SIGINT, handle_sigint)
    
    try:
        console.print("[bold blue]Starting IntershopRAG Extraction Pipeline...[/bold blue]")
        
        # 1. Authenticate
        with console.status("[bold cyan]Authenticating with Entra ID...", spinner="dots"):
            cookies = await authenticate()
        console.print("[bold green]✓ Authenticated successfully.[/bold green]")
        
        # 2. Parse Sitemap
        sitemap_url = "https://knowledge.intershop.com/sitemap.xml"
        with console.status("[bold cyan]Fetching sitemap...", spinner="dots"):
            urls = await fetch_sitemap_urls(sitemap_url, cookies)
        console.print(f"[bold green]✓ Discovered {len(urls)} URLs in the sitemap.[/bold green]")
        
        # 3. Filter URLs using State
        to_fetch = [u for u in urls if not state_manager.should_skip(u)]
        skipped = len(urls) - len(to_fetch)
        
        if skipped > 0:
            console.print(f"[dim]Skipping {skipped} already processed URLs.[/dim]")
            
        if not to_fetch:
            console.print("[bold green]All URLs are already processed! Pipeline complete.[/bold green]")
            return

        console.print(f"[bold blue]Starting fetch for {len(to_fetch)} URLs...[/bold blue]")
        
        fetcher = AsyncFetcher(cookies, state_manager, max_concurrent=5)
        
        success_count = 0
        failure_count = 0
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task_id = progress.add_task("[cyan]Scraping Pages...", total=len(to_fetch))
            
            def progress_callback(url: Optional[str], success: bool):
                nonlocal success_count, failure_count
                if success:
                    success_count += 1
                else:
                    failure_count += 1
                    if url:
                        # Print error instantly to stderr
                        from datetime import datetime
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        err_console.print(f"[red][{timestamp}] [FAILED] {url}[/red]")
                
                progress.advance(task_id, 1)

            # 4. Fetch Pages
            await fetcher.fetch_urls(to_fetch, progress_callback=progress_callback)
            
        # 5. Output Summary
        table = Table(title="Extraction Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="magenta")
        
        table.add_row("Total Discovered", str(len(urls)))
        table.add_row("Previously Skipped", str(skipped))
        table.add_row("Newly Succeeded", str(success_count))
        table.add_row("Newly Failed", str(failure_count))
        
        console.print(table)
        console.print("[bold green]Pipeline execution finished.[/bold green]")

    except Exception as e:
        import traceback
        err_console.print(f"[bold red]Pipeline encountered a fatal error: {e}[/bold red]")
        err_console.print(traceback.format_exc())
        state_manager._save()
        sys.exit(1)

def main():
    try:
        asyncio.run(run_pipeline())
    except KeyboardInterrupt:
        # Prevent stack trace spam on unhandled termination
        pass

if __name__ == "__main__":
    main()
