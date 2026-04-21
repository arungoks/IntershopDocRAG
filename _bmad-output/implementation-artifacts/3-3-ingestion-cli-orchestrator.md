# Story 3.3: Ingestion CLI Orchestrator

Status: ready-for-dev

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

- [ ] Task 1: Create `ingestion/main.py` entrypoint
  - [ ] Implement the `if __name__ == "__main__":` block to act as the CLI executable.
  - [ ] Import and sequence the functions developed in Stories 3.1 and 3.2 (`loader`, `splitter`, `embedder`).
- [ ] Task 2: Integrate `rich` Console Output
  - [ ] Use `rich.console` for clear, color-coded logging of each major phase.
  - [ ] Implement `rich.status` or `rich.progress` to give the user visual feedback during the text splitting and vector embedding phases (which may take several minutes).
- [ ] Task 3: Error Handling & Pre-flight Checks
  - [ ] Prior to calling the loader, verify that the configured raw markdown path exists and contains `.md` files. Raise a clean `rich`-formatted error (no raw stack traces) if it is empty.
  - [ ] Catch connection issues to Ollama and output a clear prompt advising the admin to run `ollama serve`.
- [ ] Task 4: Unit Testing
  - [ ] Create `tests/ingestion/test_main.py`.
  - [ ] Use `unittest.mock` to stub out the `loader`, `splitter`, and `embedder` functions to verify that `main.py` properly coordinates the flow and handles errors without requiring execution of the heavy underlying ML models.

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

Gemini 3.1 Pro (High)

### Debug Log References

### Completion Notes List

- Clarified robust error handling for missing offline Ollama services and empty source directories.
- Elaborated on `rich` implementation options for handling long-standing tasks.

### File List
- `ingestion/main.py` (to be created)
- `tests/ingestion/test_main.py` (to be created)
---
