# Story 2.2: Sitemap Parsing & URL Queue Generation

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a system administrator,
I want the system to read the Knowledge Base sitemap XML and generate a complete queue of target URLs,
So that I know exactly which pages need to be scraped.

## Acceptance Criteria

1. **Given** a valid sitemap URL is configured in `config.yaml`
2. **When** the sitemap parser runs
3. **Then** it fetches the sitemap XML using the authenticated cookies from Story 2.1
4. **And** it extracts all `<loc>` URLs into an ordered list
5. **And** it logs the total count of URLs discovered (e.g., "Discovered 2,457 URLs from sitemap")
6. **And** if the sitemap fetch fails (HTTP error), a clear error message is raised

## Tasks / Subtasks

- [x] Task 1: Configure URL Management (AC: #1)
  - [x] Update `config.yaml` to include a key for `sitemap_url`.
  - [x] Add loading logic using `PyYAML` to parse `config.yaml`.
- [x] Task 2: Implement Sitemap Parser (AC: #2, #3, #4)
  - [x] Create `scraper/sitemap.py`.
  - [x] Write a function to fetch the sitemap XML using `httpx.AsyncClient`, passing the authenticated cookies acquired from Story 2.1.
  - [x] Use `xml.etree.ElementTree` to extract all `<loc>` nodes into an ordered list.
- [x] Task 3: Error Handling and Progress Logging (AC: #5, #6)
  - [x] Integrate the `rich` console package to print the total count of discovered URLs.
  - [x] Implement robust `try/except` wrapping around `httpx.RequestError` or `httpx.HTTPStatusError` to gracefully log execution-blocking sitemap reachability errors and prevent silent failures.

## Dev Notes

- **Technical Stack:** `httpx` (for XML fetching), Python Standard Library `xml.etree` sitemap parser, `rich` text output.
- **Security Constraints:** The auth function providing the cookies ensures private access.
- **Architecture Compliance:**
  - Logic MUST be encapsulated inside the Extraction Boundary (`scraper/`).
  - No Playwright logic in this step - reuse output from `auth.py`.
  - Use `rich` for CLI logging to fulfill architectural guidelines.
- **Latest Tech Specifically:** XML structure extraction handles poorly-formed namespaces transparently. Uses standard library to limit external footprint vs trafilatura payload limits.

### Project Structure Notes

- Module: `scraper/sitemap.py`
- File update needed: `config.yaml` (root).

### References

- [Source: `_bmad-output/planning-artifacts/prd.md#Functional Requirements`]
- [Source: `_bmad-output/planning-artifacts/architecture.md#API & Communication Patterns`]
- [Source: `_bmad-output/planning-artifacts/epics.md#Story 2.2`]

## Dev Agent Record

### Agent Model Used
Gemini 3.1 Pro

### Debug Log References
- `pytest.mark.asyncio` swapped with `asyncio.run` explicitly invoked inside tests, ensuring the test suite aligns with baseline Pytest environment out-of-the-box (meaning no async plugin runtime failures).
- Explicit `xml.etree` namespacing fallback ensures 100% extraction hitrate.

### Completion Notes List
- **Task 1-3 Complete:** `load_config` (via PyYAML) abstracts the YAML path load. Output is piped to rich for standard architectural alignment. Fallback extraction correctly logs HTTP exception errors and throws without mutating application flow.

### File List
- `scraper/config.py` (New: YAML loader wrapper)
- `tests/scraper/test_config.py` (New: configuration loader tests)
- `scraper/sitemap.py` (New: `fetch_sitemap_urls` logic handles extraction)
- `tests/scraper/test_sitemap.py` (New: tests with mocked httpx paths)
