# Story 2.7: CLI Pipeline Orchestrator with Real-Time Progress

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a system administrator,
I want to initiate the entire extraction pipeline via a single CLI command and see real-time progress,
So that I have full visibility into the scraping operation and can run it hands-free.

## Acceptance Criteria

1. **Given** the system administrator runs `uv run python scraper/main.py`
2. **When** the pipeline executes
3. **Then** it orchestrates the full flow: authenticate → parse sitemap → load state → fetch pages → convert to markdown → save state
4. **And** a `rich` console displays real-time progress (e.g., progress bar, pages completed/total, errors encountered)
5. **And** error logs are printed to stderr with timestamps and the failing URL
6. **And** when all URLs are processed (or all retries exhausted), the pipeline outputs a summary (total success, failed, skipped counts) and exits cleanly
7. **And** if the pipeline is interrupted (e.g., Ctrl+C), it saves the current state to `scrape_state.json` before exiting

## Tasks / Subtasks

- [x] Task 1: Pipeline Orchestration Scaffold (AC: #1, #2, #3)
  - [x] Create `scraper/main.py` if it doesn't already exist.
  - [x] Implement the `__main__` entrypoint to orchestrate the imports from `auth`, `fetcher` / `parser`, and `state`.
  - [x] Write the sequential execution flow: Trigger auth -> Get cookies -> Fetch sitemap queue -> Initialize state -> Pass queue to async fetcher loop.
- [x] Task 2: Rich Console Integration (AC: #4, #5, #6)
  - [x] Integrate `rich.progress.Progress` to show a live progress bar mapping against the total items in the sitemap queue.
  - [x] Use `rich.console.Console(stderr=True)` for logging exceptions with timestamps.
  - [x] On completion, calculate summary metrics (successes, skips, failures) from the final state object and `rich.print()` a clean summary table or block.
- [x] Task 3: Graceful Teardown and Signal Handling (AC: #7)
  - [x] Wrap the main execution block in a `try...except KeyboardInterrupt` and general `Exception` block.
  - [x] Ensure that even if interrupted, the `scraper/state.py` save function is explicitly called to persist progress up to that exact moment.

## Dev Notes

- **Technical Stack:** Python `asyncio.run()`, `rich` library (Progress, Console, Table), standard library `signal` or `try/finally` blocks.
- **Architecture Compliance:**
  - This file serves as the singular entrypoint for the Extraction loop.
  - Ensure compatibility with `uv run python scraper/main.py` structure.
  - The orchestrator should not perform HTTTP fetching or HTML parsing directly; it delegates those to the appropriate modules from prior stories.
- **Dependency Integration:** Integrates `auth.py`, `state.py`, and `fetcher.py`. If those modular boundaries have not been rigidly defined, use this story to solidify them by calling their public APIs.

### Project Structure Notes

- Module: `scraper/main.py`
- Root entry point for Epic 2.

### References

- [Source: `_bmad-output/planning-artifacts/prd.md#Functional Requirements` (FR4, FR6, FR7)]
- [Source: `_bmad-output/planning-artifacts/architecture.md#API & Communication Patterns`]
- [Source: `_bmad-output/planning-artifacts/epics.md#Story 2.7`]

## Dev Agent Record

### Agent Model Used
Gemini 3.1 Pro (Low)

### Debug Log References
- Per user instruction, ignored unit tests and proceeded to complete the development tasks for 2-7.

### Completion Notes List
- Successfully created `scraper/main.py` entrypoint.
- Added rich progress bar showing completion for the URLs mapped to `sitemap.xml`.
- Registered `signal.SIGINT` and wrapped into a try-except to ensure `state_manager._save()` commits state.
- Emits timestamped errors directly to stderr `err_console`.

### File List
- `scraper/main.py`
