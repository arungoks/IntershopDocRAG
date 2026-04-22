"""
ingestion/main.py
------------------
CLI Orchestrator for the IntershopRAG Vector Ingestion Pipeline.

Orchestrates the full ingestion flow:
  1. Load scraped markdown files from data/raw_md/
  2. Split documents into semantic chunks
  3. Embed chunks via local Ollama (nomic-embed-text)
  4. Upsert vectors into local ChromaDB (data/vectordb/)

Run with:
    uv run python ingestion/main.py
"""

import logging
import os
import sys
from pathlib import Path

# Allow running as a top-level script: `python ingestion/main.py`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Plain prints before any heavy imports so the terminal is never silent
print("[ingestion] Loading dependencies...", flush=True)

import yaml
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

print("[ingestion] Rich loaded.", flush=True)

from ingestion.splitter import split_documents
from ingestion.embedder import build_vector_store, embed_and_store

print("[ingestion] Ingestion modules loaded. Entering main...", flush=True)

# ---------------------------------------------------------------------------
# Logging setup — route library logs to console at WARNING level
# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

console = Console()
err_console = Console(stderr=True)

CONFIG_PATH = "config.yaml"
DEFAULT_RAW_MD_PATH = "data/raw_md"


def _load_raw_md_path() -> str:
    """Read raw_md_path from config.yaml, falling back to default."""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
            cfg = yaml.safe_load(fh) or {}
        return str(cfg.get("raw_md_path", DEFAULT_RAW_MD_PATH))
    except (FileNotFoundError, yaml.YAMLError):
        return DEFAULT_RAW_MD_PATH


def _check_ollama(port: int = 11434) -> None:
    """Probe Ollama with a 3-second TCP timeout. Exits cleanly if unreachable."""
    import socket  # noqa: PLC0415
    try:
        with socket.create_connection(("localhost", port), timeout=3):
            pass
        console.print(f"[bold green]✓[/bold green] Ollama is reachable on port {port}.")
    except OSError:
        err_console.print(
            Panel(
                f"[bold red]Cannot reach Ollama on localhost:{port}[/bold red]\n\n"
                "Start Ollama in a separate terminal:\n"
                "  [bold cyan]ollama serve[/bold cyan]\n\n"
                "Then pull the embedding model if not already done:\n"
                "  [bold cyan]ollama pull nomic-embed-text[/bold cyan]",
                title="❌  Ollama Not Running",
                border_style="red",
            )
        )
        sys.exit(1)


def _preflight_check(raw_md_path: str) -> None:
    """Verify the markdown source directory exists and has files.

    Raises:
        SystemExit: With a clear, friendly error message if checks fail.
    """
    p = Path(raw_md_path)
    if not p.exists() or not p.is_dir():
        err_console.print(
            Panel(
                f"[bold red]Source directory not found:[/bold red] [yellow]{raw_md_path}[/yellow]\n\n"
                "The scraper pipeline must be run first to populate this directory.\n"
                "Run:  [bold cyan]uv run python scraper/main.py[/bold cyan]",
                title="❌  Pre-flight Check Failed",
                border_style="red",
            )
        )
        sys.exit(1)

    md_files = list(p.glob("*.md"))
    if not md_files:
        err_console.print(
            Panel(
                f"[bold red]No markdown files found in:[/bold red] [yellow]{raw_md_path}[/yellow]\n\n"
                "The scraper has not produced any output yet.\n"
                "Run:  [bold cyan]uv run python scraper/main.py[/bold cyan]",
                title="❌  Pre-flight Check Failed",
                border_style="red",
            )
        )
        sys.exit(1)


def _iter_md_files(raw_md_path: str):
    """Yield (path, Document) for each valid .md file in *raw_md_path*.

    Files with missing frontmatter keys are skipped with a warning so the
    streaming loop never stalls on a corrupt file.
    """
    from langchain_core.documents import Document  # noqa: PLC0415
    from ingestion.loader import _parse_frontmatter, REQUIRED_META_KEYS  # noqa: PLC0415

    directory = Path(raw_md_path)
    for md_file in sorted(directory.glob("*.md")):
        try:
            content = md_file.read_text(encoding="utf-8")
        except OSError as exc:
            logger.warning("Cannot read %s: %s", md_file, exc)
            continue

        metadata, body = _parse_frontmatter(content)
        missing = REQUIRED_META_KEYS - metadata.keys()
        if missing:
            logger.warning("Skipping %s — missing frontmatter keys: %s", md_file.name, missing)
            continue

        str_metadata = {k: str(v) for k, v in metadata.items()}
        yield md_file, Document(page_content=body, metadata=str_metadata)


def main() -> None:
    """Run the full ingestion pipeline with rich progress output.

    Uses a **streaming per-file loop** so that only one file's chunks live
    in memory at a time — eliminates OOM errors on large corpora.
    ChromaDB and Ollama are initialised ONCE before the loop and reused.
    """

    console.print(
        Panel(
            "[bold blue]IntershopRAG — Vector Ingestion Pipeline[/bold blue]",
            subtitle="Powered by Ollama + ChromaDB  ·  streaming mode",
            border_style="blue",
        )
    )

    raw_md_path = _load_raw_md_path()

    # ------------------------------------------------------------------ #
    # Pre-flight: ensure source data exists
    # ------------------------------------------------------------------ #
    _preflight_check(raw_md_path)

    # Count files for the progress bar without loading content
    md_files = sorted(Path(raw_md_path).glob("*.md"))
    total_files = len(md_files)
    console.print(
        f"[bold green]✓[/bold green] Found [bold]{total_files}[/bold] markdown files in "
        f"[dim]{raw_md_path}[/dim]\n"
    )

    # ------------------------------------------------------------------ #
    # Fast Ollama reachability check — fails in 3 s instead of 60 s
    # ------------------------------------------------------------------ #
    _check_ollama()

    # ------------------------------------------------------------------ #
    # Initialise ChromaDB + Ollama ONCE — reused for every file
    # ------------------------------------------------------------------ #
    console.print("[bold cyan]Initialising ChromaDB and Ollama embedding model...[/bold cyan]")
    try:
        vector_store = build_vector_store(config_path=CONFIG_PATH)
    except Exception as exc:
        err_console.print(
            Panel(
                f"[bold red]Failed to initialise vector store:[/bold red] {exc}\n\n"
                "Ensure Ollama is running:  [bold cyan]ollama serve[/bold cyan]\n"
                "And the model is pulled:   [bold cyan]ollama pull nomic-embed-text[/bold cyan]",
                title="❌  Initialisation Failed",
                border_style="red",
            )
        )
        sys.exit(1)

    console.print("[bold green]✓[/bold green] Vector store ready.\n")
    console.print(
        "[bold cyan]Streaming pipeline: load → split → embed per file[/bold cyan]\n"
        "[dim]  Memory stays flat regardless of corpus size.[/dim]\n"
    )

    total_docs = 0
    total_chunks = 0
    total_stored = 0
    skipped_files = 0
    chunk_offset = 0  # Tracks global chunk index for unique IDs across files

    # ------------------------------------------------------------------ #
    # Streaming loop: process one file at a time
    # ------------------------------------------------------------------ #
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[bold magenta]{task.completed}/{task.total}[/bold magenta] files"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Ingesting", total=total_files)

        for md_file, doc in _iter_md_files(raw_md_path):
            progress.update(
                task,
                description=f"[cyan]{md_file.name[:40]}[/cyan]",
            )

            # Split this single document into chunks
            try:
                chunks = split_documents([doc], config_path=CONFIG_PATH)
            except Exception as exc:
                logger.warning("Failed to split %s: %s — skipping.", md_file.name, exc)
                skipped_files += 1
                progress.advance(task)
                continue

            if not chunks:
                progress.advance(task)
                continue

            # Embed and store this file's chunks immediately, then discard
            try:
                stored = embed_and_store(
                    chunks,
                    vector_store=vector_store,
                    chunk_index_offset=chunk_offset,
                )
            except ConnectionError as exc:
                err_console.print(
                    Panel(
                        f"[bold red]Cannot reach Ollama:[/bold red] {exc}\n\n"
                        "Please ensure the Ollama service is running:\n"
                        "  [bold cyan]ollama serve[/bold cyan]\n"
                        "And that the embedding model is pulled:\n"
                        "  [bold cyan]ollama pull nomic-embed-text[/bold cyan]",
                        title="❌  Ollama Unreachable",
                        border_style="red",
                    )
                )
                sys.exit(1)
            except Exception as exc:
                logger.warning(
                    "Embedding failed for %s: %s — skipping.", md_file.name, exc
                )
                skipped_files += 1
                progress.advance(task)
                continue

            total_docs += 1
            total_chunks += len(chunks)
            total_stored += stored
            chunk_offset += len(chunks)  # Keep global offset in sync

            # chunks and doc go out of scope here — GC can reclaim memory
            progress.advance(task)

    # ------------------------------------------------------------------ #
    # Summary
    # ------------------------------------------------------------------ #
    table = Table(title="Ingestion Summary", border_style="green")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="bold magenta")

    table.add_row("Files processed", str(total_docs))
    table.add_row("Files skipped", str(skipped_files))
    table.add_row("Chunks produced", str(total_chunks))
    table.add_row("Vectors stored", str(total_stored))

    console.print(table)
    console.print(
        "\n[bold green]✅  Ingestion pipeline complete![/bold green] "
        "The vector database is ready for querying."
    )


if __name__ == "__main__":
    main()
