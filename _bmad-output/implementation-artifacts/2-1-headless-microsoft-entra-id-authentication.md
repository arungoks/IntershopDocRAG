# Story 2.1: Headless Microsoft Entra ID Authentication

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a system administrator,
I want the system to programmatically authenticate through the Microsoft Entra ID portal using a headless browser and persist the session cookies locally,
So that the scraping pipeline can access the protected Knowledge Base without manual login.

## Acceptance Criteria

1. **Given** valid credentials exist in a local `creds.txt` file (username on line 1, password on line 2) **When** the `scraper/auth.py` module is executed **Then** a headless Playwright Chromium browser navigates the MS Entra ID OAuth flow and successfully authenticates
2. **And** the extracted session cookies are returned as a dictionary usable by `httpx`
3. **And** if `creds.txt` is missing or credentials are invalid, a clear error message is raised
4. **And** Playwright logic is strictly isolated to `scraper/auth.py` — no other module imports Playwright

## Tasks / Subtasks

- [x] Task 1: Create `scraper/auth.py` module (AC: #4)
  - [x] Isolate all Playwright imports and functions in this module exclusively.
- [x] Task 2: Implement credential loading (AC: #3)
  - [x] Read `creds.txt` from the project root.
  - [x] Add exception handling for missing file or malformed credentials.
- [x] Task 3: Implement Headless Playwright flow (AC: #1, #2)
  - [x] Spin up `async_playwright` (Chromium).
  - [x] Navigate to the Microsoft Entra ID login portal for Intershop Knowledge Base.
  - [x] Input username (line 1), wait for next step.
  - [x] Input password (line 2), submit and handle any "Stay Signed In?" prompts.
  - [x] Wait for the redirect to complete to the protected Knowledge Base page.
  - [x] Extract the persistent auth cookies.
  - [x] Return the cookies as a dictionary formatted for `httpx`.

## Dev Notes

- **Technical Stack:** Playwright in Python (specifically `playwright.async_api`).
- **Security Constraints:** `creds.txt` MUST never be tracked in version control (this was handled in `.gitignore` during Story 1.2).
- **Architecture Strategy:** The auth script must be completely independent of the scraping engine. It is just a utility that breaches OAuth and hands off cookies to `httpx.AsyncClient`.

### Project Structure Notes

- Module: `scraper/auth.py`

### References

- [Source: `_bmad-output/planning-artifacts/prd.md#Authentication & Session Management`]
- [Source: `_bmad-output/planning-artifacts/prd.md#Risk Mitigation Strategy`]
- [Source: `_bmad-output/planning-artifacts/epics.md#Story 2.1`]

## Dev Agent Record

### Agent Model Used
Gemini 3.1 Pro

### Debug Log References
- `sys.path` manipulated in `pytest` to locate dependencies via `[tool.pytest.ini_options]` in `pyproject.toml`
- Test dependencies isolated to avoid `ImportError` on missing locally-configured modules. Mock objects explicitly initialized. 

### Completion Notes List
- **Task 1-3:** Successfully implemented `scraper/auth.py` and `tests/scraper/test_auth.py` spanning 12 comprehensive unit + architectural constraints tests. Headless navigation explicitly structured to extract Entra ID cookies. All paths simulated via async mock instances. Tests are green.

### File List
- `pyproject.toml` (Modified: pytest configuration)
- `tests/conftest.py` (Modified: updated testing environment hooks)
- `tests/__init__.py` (New: enabled robust testing architecture)
- `scraper/auth.py` (New: Playwright async authenticator)
- `tests/scraper/test_auth.py` (New: unit tests suite)
