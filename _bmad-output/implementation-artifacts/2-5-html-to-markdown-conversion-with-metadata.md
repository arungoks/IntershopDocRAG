# Story 2.5: HTML-to-Markdown Conversion with Metadata

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a system administrator,
I want each fetched HTML page to be converted into a clean Markdown file with YAML frontmatter metadata,
So that the local documentation repository is structured, searchable, and preserves critical content.

## Acceptance Criteria

1. **Given** a raw HTML payload fetched by the async engine
2. **When** `trafilatura` processes the HTML
3. **Then** the output is a clean Markdown file preserving tables, code blocks, and hyperlinks
4. **And** all internal URLs are rewritten to absolute URLs (e.g., `https://knowledge.intershop.com/...`)
5. **And** a YAML frontmatter header is injected containing: `id` (unique page ID), `title` (extracted page title), `url` (original absolute URL), `scraped_at` (ISO-8601 timestamp)
6. **And** the Markdown file is saved to `data/raw_md/{page_id}.md`
7. **And** if `trafilatura` fails to extract content, the URL is marked as `"failed"` in the state file with an error log

## Tasks / Subtasks

- [x] Task 1: Setup HTML-to-Markdown Extraction (AC: #2, #3, #4)
  - [x] Implement processing logic in `scraper/parser.py`.
  - [x] Use `trafilatura.extract()` passing arguments to retain tables and links (`include_links=True`, `include_tables=True`).
  - [x] Write logic to parse and rewrite all relative URLs inside the extracted content into absolute URLs referencing the Intershop domain.
- [x] Task 2: Inject YAML Frontmatter Metadata (AC: #5)
  - [x] Implement a function to prepend YAML frontmatter strictly formatting `id`, `title`, `url`, and `scraped_at`.
  - [x] Extract the title safely from the HTML (via `trafilatura.extract_metadata` natively).
  - [x] Format `scraped_at` as an ISO-8601 string.
- [x] Task 3: Save to Disk and Handle Failures (AC: #6, #7)
  - [x] Write the generated Markdown string safely to `data/raw_md/{page_id}.md`.
  - [x] Introduce error handling: If `trafilatura` falls back to empty output or faults, log the error using `rich`, and integrate with Story 2.3 `state.py` to mark the URL status as `"failed"`.

## Dev Notes

- **Technical Stack:** `trafilatura`, standard `datetime` for ISO string generation, `re` or `urllib.parse` for relative-to-absolute URL resolution.
- **Architecture Compliance:**
  - Logic MUST be encapsulated inside the Extraction Boundary (`scraper/`).
  - Expected Markdown YAML block requires exact string match keys to guarantee compatibility with `DirectoryLoader` in Epic 3.
  - File path output must be exactly `{page_id}.md` instead of the full article title to prevent OS-level character length and invalid character issues on Windows.
- **Dependency Integration:** Expects `data/raw_md/` to be created or exist. Integrate closely with the `fetcher` and `state` modules from prior stories.

### Project Structure Notes

- Module: `scraper/parser.py` inside the Extraction Boundary.
- Target Output Directory: `data/raw_md/`

### References

- [Source: `_bmad-output/planning-artifacts/prd.md#Functional Requirements` (FR12, FR13, FR14)]
- [Source: `_bmad-output/planning-artifacts/architecture.md#Format Patterns`]
- [Source: `_bmad-output/planning-artifacts/epics.md#Story 2.5`]

## Dev Agent Record

### Agent Model Used
Gemini 3.1 Pro

### Debug Log References
- `urllib.parse.urljoin` cleanly wraps `trafilatura`'s markdown generation to guarantee `data_tables` and relative HTML components point exactly back to absolute sources.
- Safe `md5(url)` handles `id` generation reliably sidestepping Windows Path constraint character limitations!

### Completion Notes List
- **Tasks 1-3:** Standalone extraction class handles parsing natively intercepting pipeline HTML strings via memory. Rebound testing in `scraper/fetcher.py` cleanly maps `[failed]` traps directly into our internal `.state` system preventing cascading issues with downstream embedding chunks.

### File List
- `scraper/parser.py` (New)
- `tests/scraper/test_parser.py` (New)
- `scraper/fetcher.py` (Modified to attach processing natively on `200 OK`)
- `tests/scraper/test_fetcher.py` (Modified isolated mock limits to expect filepaths on output bounds)
