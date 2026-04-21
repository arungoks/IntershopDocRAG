# Story 2.6: Cookie Expiry Detection & Auto-Reauthentication

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a system administrator,
I want the system to detect expired authentication cookies mid-scrape and automatically re-authenticate without losing progress,
So that long-running scrapes of 2,457 pages complete autonomously even when tokens expire.

## Acceptance Criteria

1. **Given** the async fetcher encounters an HTTP 401 or 403 response during a scrape run
2. **When** the fetcher detects this authentication failure
3. **Then** it pauses all in-flight HTTP requests
4. **And** it triggers the `scraper/auth.py` module to perform a fresh headless Playwright login
5. **And** it updates the session cookies in the `httpx.AsyncClient`
6. **And** it resumes fetching from where it left off without losing queue state or re-downloading successful pages
7. **And** if reauthentication fails after 2 attempts, the pipeline shuts down gracefully with a clear error

## Tasks / Subtasks

- [x] Task 1: Auth Exception Detection (AC: #1, #2)
  - [x] Implement handling for HTTP 401 / 403 within the fetcher loop or exception block (`scraper/fetcher.py`).
  - [x] When detected, signal the pipeline to halt generating new requests (pause in-flight limits).
- [x] Task 2: Auto-Reauthentication Workflow (AC: #3, #4, #5)
  - [x] Use an `asyncio.Lock` or similar synchronization primitive to prevent multiple worker tasks from triggering the `auth.py` login concurrently.
  - [x] Invoke the authentication function from `scraper/auth.py` securely.
  - [x] Update the `httpx.AsyncClient` instance with the newly acquired cookies.
- [x] Task 3: Retry and Fast Fail Logic (AC: #6, #7)
  - [x] Ensure that URLs that failed explicitly due to authentication are automatically requeued/retried by the fetcher immediately following token refresh.
  - [x] Implement a retry counter for the *authentication* process itself. If `auth.py` is called twice consecutively without a successful HTTP payload following it, raise a critical pipeline halt error and exit cleanly (saving state first).

## Dev Notes

- **Technical Stack:** `asyncio.Lock` for concurrency control, exception trapping on `httpx.HTTPStatusError`.
- **Architecture Compliance:**
  - Logic MUST be encapsulated inside the Extraction Boundary (`scraper/`).
  - Strict synchronization is necessary so that 5 concurrent async workers getting a 401 simultaneously don't launch 5 Playwright instances.
  - Resume functionality relies on the shared state checkpoint mechanism from Story 2.3.
- **Dependency Integration:** Depends directly on `scraper/auth.py` (Story 2.1) returning a fresh dictionary of cookies, and integrates intricately into `scraper/fetcher.py` (Story 2.4).

### Project Structure Notes

- Module: `scraper/fetcher.py` and potentially updates to `scraper/auth.py` or the main orchestrator loop.

### References

- [Source: `_bmad-output/planning-artifacts/prd.md#Functional Requirements` (FR3)]
- [Source: `_bmad-output/planning-artifacts/architecture.md#Process Patterns`]
- [Source: `_bmad-output/planning-artifacts/epics.md#Story 2.6`]

## Dev Agent Record

### Agent Model Used
Gemini 3.1 Pro (Low)

### Debug Log References
- Per user instruction, ignored unit tests and proceeded to complete the development tasks.

### Completion Notes List
- Implemented robust `_auth_lock` mechanics using an `_auth_generation` counter.
- Implemented fast-fail mechanics on max sequential auth errors (2).
- Ensured state gets saved before raising `RuntimeError`.

### File List
- `scraper/fetcher.py`
- `tests/scraper/test_fetcher.py`
- `tests/scraper/test_fetcher_auth.py`
