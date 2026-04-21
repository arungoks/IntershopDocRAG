# Story 2.4: Async HTTP Fetcher with Rate Limiting & Retries

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a system administrator,
I want the system to download multiple web pages concurrently with automatic rate limiting and retry logic,
So that the full Knowledge Base can be fetched efficiently without overwhelming the target server.

## Acceptance Criteria

1. **Given** a list of target URLs and valid session cookies
2. **When** the `scraper/fetcher.py` async engine processes the queue
3. **Then** it downloads pages concurrently using `httpx.AsyncClient` with an `asyncio.Semaphore` limiting to 3-5 workers
4. **And** HTTP 429/503 responses trigger automatic backoff before retrying
5. **And** failed requests are retried up to 3 times with exponential backoff before being marked as `"failed"` in the state file
6. **And** each URL's result (success/failure) is recorded via the State Checkpoint Manager (Story 2.3)

## Tasks / Subtasks

- [x] Task 1: Setup httpx AsyncClient and Semaphore (AC: #3)
  - [x] Implement async generator or consumer function in `scraper/fetcher.py`.
  - [x] Initialize `httpx.AsyncClient(cookies=...)` using cookies from the Auth module.
  - [x] Create an `asyncio.Semaphore` with a limit variable (e.g., 3 to 5 concurrent workers).
- [x] Task 2: Implement Retry and Backoff Logic (AC: #4, #5)
  - [x] Wrap the `httpx.get` call in a custom retry loop or utilize a library like `tenacity`.
  - [x] Ensure specific handling for HTTP 429 and 503 errors to trigger exponential backoff.
  - [x] Allow up to 3 retry attempts before raising a final failure exception.
- [x] Task 3: State Checkpoint Integration (AC: #6)
  - [x] Import and utilize the methods from `scraper/state.py` (implemented in Story 2.3).
  - [x] Check `scrape_state.json` via the state manager *before* fetching to skip pre-processed URLs.
  - [x] Record the final status (`"success"` or `"failed"`) of the URL to the checkpoint JSON after processing.
- [x] Task 4: HTTP 401/403 Preparation (Architecture requirement prep)
  - [x] Log and raise `httpx.HTTPStatusError` specifically on auth-related status codes (401, 403), allowing the orchestrator/orchestration-loop to trigger a re-auth if needed in the future (Story 2.6).

## Dev Notes

- **Technical Stack:** `asyncio`, `httpx`, Custom backoff loop natively implemented over `tenacity` to keep external dependency count thin and ensure fine-tuned explicit control for authentication exception bubbling.
- **Architecture Compliance:**
  - Logic MUST be encapsulated inside `scraper/fetcher.py`.
  - Always respect the `asyncio.Semaphore` limit to avoid DDoSing the proprietary API.
  - Use `httpx.AsyncClient` for all outbound calls to allow for shared connection pools and cookies.
- **Dependencies:** Uses `scraper.state` from Story 2.3 for unified skip checking natively inside loop constraints.

### Project Structure Notes

- Module: `scraper/fetcher.py`

### References

- [Source: `_bmad-output/planning-artifacts/prd.md#NonFunctional Requirements` (NFR-P2, NFR-R1)]
- [Source: `_bmad-output/planning-artifacts/architecture.md#API & Communication Patterns`]
- [Source: `_bmad-output/planning-artifacts/epics.md#Story 2.4`]

## Dev Agent Record

### Agent Model Used
Gemini 3.1 Pro

### Debug Log References
- Decided to build the backoff logic directly utilizing `asyncio.sleep` with standard Python exception loops mapped dynamically to the `httpx.Response` code map instead of introducing extra imports such as `tenacity`. This enables full granular exception bubbling handling authentication traps (401/403).

### Completion Notes List
- **Task 1-4 Delivered:** Created AsyncFetcher class bridging URL traversal semantics tightly against `StateManager`. Re-raises `raise_for_status` specifically to bubble cleanly if an unrecoverable runtime authorization condition halts concurrent extraction pipelines abruptly!

### File List
- `scraper/fetcher.py` (New: async concurrent HTTP payload loop handling Semaphore + rate limits)
- `tests/scraper/test_fetcher.py` (New: async mock coverage against error trap limits)
