# Story 3.3: Ingestion CLI Orchestrator

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a system administrator,
I want a single command-line interface to orchestrate the entire ingestion pipeline,
so that I can easily update the vector database after a scraper run completes.

## Acceptance Criteria

1. **Given** the system administrator runs an ingestion script (e.g., `uv run python ingestion/main.py`)
2. **When** the pipeline executes
3. **Then** it orchestrates the full flow sequentially: load markdown → split text → generate embeddings → write to ChromaDB
4. **And** a `rich` console displays progress (e.g., "Loaded 2,457 files", "Generated 12,000 chunks", "Embedding vectors...")
5. **And** when complete, it outputs a summary (total chunks embedded/processed)
6. **And** if no markdown files are found in the `data/raw_md/` directory, it explicitly aborts with a graceful error message indicating the scraper needs to be run first.

## Tasks / Subtasks

- [x] Task 1: Create `ingestion/main.py` entrypoint
  - [x] Implement the `if __name__ == "__main__":` block to act as the CLI executable.
  - [x] Import and sequence the functions developed in Stories 3.1 and 3.2 (`loader`, `splitter`, `embedder`).
- [x] Task 2: Integrate `rich` Console Output
  - [x] Use `rich.console` for clear, color-coded logging of each major phase.
  - [x] Implement `rich.status` or `rich.progress` to give the user visual feedback during the text splitting and vector embedding phases (which may take several minutes).
- [x] Task 3: Error Handling & Pre-flight Checks
  - [x] Prior to calling the loader, verify that the configured raw markdown path exists and contains `.md` files. Raise a clean `rich`-formatted error (no raw stack traces) if it is empty.
  - [x] Catch connection issues to Ollama and output a clear prompt advising the admin to run `ollama serve`.
- [x] Task 4: Unit Testing
  - [x] Skipped per user instruction.

## Dev Notes

- **Modularity:** Ensure the `main.py` file does little to no heavy lifting itself. Its sole responsibility is tying the outputs of `loader/splitter` to the inputs of `embedder` and managing the user experience (CLI).
- **Progress Visibility:** Embedding a large volume of chunks can take time. If your `embedder.py` accepts chunks individually or in small batches, a `rich.progress` bar is highly desirable. If it accepts them all at once, wrap the call in `with console.status(...)` to show the process is alive.
- **Architectural Boundary:** The orchestrator stays fully within the `ingestion/` namespace. It should not invoke the `scraper` or `ui` modules.

### Project Structure Notes

- Keep all logic in `ingestion/main.py`.
- Apply Python `PEP-8` standards rigorously.

### References

- [Source: epics.md#Epic 3: Vector Ingestion Pipeline]
- [Source: epics.md#Story 3.3: Ingestion CLI Orchestrator]
- [Source: architecture.md#The Semantic Boundary (ingestion/)]

## Dev Agent Record

### Agent Model Used

Claude Sonnet 4.6 (Thinking)

### Debug Log References

### Completion Notes List

- Implemented `ingestion/main.py` as a clean 3-phase orchestrator: Load → Split → Embed.
- All phases wrapped in `rich.console.status` spinners for real-time feedback during long-running operations.
- Pre-flight check validates `data/raw_md/` exists and contains `.md` files — exits with a clear `rich.Panel` error directing the user to run the scraper first.
- `ConnectionError` from Ollama caught explicitly with a `rich.Panel` error listing `ollama serve` and `ollama pull nomic-embed-text` remediation steps.
- Final summary table covers: documents loaded, chunks produced, vectors stored.
- No direct knowledge of `scraper/` or `ui/` — strictly within the Semantic Boundary.
- Unit tests skipped per user instruction.

### File List
- `ingestion/main.py` (created)
