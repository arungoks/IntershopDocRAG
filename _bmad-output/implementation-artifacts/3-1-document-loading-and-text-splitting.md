# Story 3.1: Document Loading & Text Splitting

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a system administrator,
I want the system to load all scraped markdown files from disk and split them into semantic chunks,
so that large documentation pages can be intelligently embedded into the vector database.

## Acceptance Criteria

1. **Given** the scraper has populated `data/raw_md/` with Markdown files
2. **When** the `ingestion/loader.py` and `ingestion/splitter.py` modules are executed
3. **Then** LangChain's `DirectoryLoader` (or custom metadata-aware loader) successfully loads all `.md` files
4. **And** LangChain's `RecursiveCharacterTextSplitter` splits the text using `chunk_size` and `chunk_overlap` configured in `config.yaml` (defaulting to 2000 and 200, respectively)
5. **And** the original YAML frontmatter metadata (`id`, `title`, `url`, `scraped_at`) is successfully preserved and associated with each resulting document chunk's `metadata` dictionary

## Tasks / Subtasks

- [x] Task 1: Implement `ingestion/loader.py` (AC: 1, 3, 5)
  - [x] Implement a function or class to load `.md` files from `data/raw_md/` using LangChain's Document structure.
  - [x] Ensure that YAML frontmatter is explicitly parsed and assigned to the LangChain Document `metadata` property (e.g. using `python-frontmatter` or `yaml` modules, since default `TextLoader` does not extract YAML frontmatter).
- [x] Task 2: Implement `ingestion/splitter.py` (AC: 2, 4, 5)
  - [x] Read `chunk_size` and `chunk_overlap` properties from the centralized `config.yaml` using a YAML parser. Fallback to 2000 and 200 if not present.
  - [x] Instantiate `RecursiveCharacterTextSplitter` from LangChain.
  - [x] Implement a function to take a list of loaded `Document` objects and return a list of split `Document` objects.
  - [x] Verify that metadata (`id`, `title`, `url`, `scraped_at`) is correctly propagated to all resulting document chunks.
- [x] Task 3: Unit Testing
  - [x] Stub test file created at `tests/ingestion/test_loader.py` — user opted to skip detailed unit tests.

## Dev Notes

- **Metadata Parsing**: LangChain's base `TextLoader` or `DirectoryLoader` may not parse YAML frontmatter natively into the `metadata` dictionary. You must ensure the frontmatter is accurately parsed and attached to the `metadata` payload so that down-stream citation logic (in the UI) has access to `id`, `url`, `title`, etc.
- **Config Reading**: Rely on `yaml.safe_load` to read `config.yaml` or use an existing config loader if one was created in Epic 1.
- **Dependencies**: Use `PyYAML` or `python-frontmatter` if needed. Remember to add it to `pyproject.toml` via `uv add` if it isn't already present.
- **Error Handling**: Log a warning and skip any markdown file that is malformed or missing the required YAML metadata.
- **Cross-story Dependencies**: The output from `ingestion/splitter.py` will directly feed into `ingestion/embedder.py` (Story 3.2), so ensure the signature returns standard LangChain `Document` chunks.

### Project Structure Notes

- `ingestion/` is the Semantic Boundary. This module has no knowledge of Streamlit or the scraper's Playwright components. It relies purely on the output placed in `data/raw_md/` and data from `config.yaml`.
- Respect `PEP-8`: use `snake_case` for files and functions (e.g. `ingestion/loader.py`, `ingestion/splitter.py`).
- Maintain isolation logic: loading and splitting should remain uncoupled from ChromaDB embedding logic (for now), allowing modular testing.

### References

- [Source: epics.md#Epic 3: Vector Ingestion Pipeline]
- [Source: epics.md#Story 3.1: Document Loading & Text Splitting]
- [Source: architecture.md#The Semantic Boundary (ingestion/)]
- [Source: architecture.md#Format Patterns - Markdown YAML Frontmatter]

## Dev Agent Record

### Agent Model Used

Claude Sonnet 4.6 (Thinking)

### Debug Log References

### Completion Notes List

- Implemented `ingestion/loader.py` with custom YAML frontmatter parsing using `PyYAML` (already in `pyproject.toml`). Skips files missing any of `id`, `title`, `url`, `scraped_at`. Coerces metadata values to `str` for ChromaDB compatibility.
- Implemented `ingestion/splitter.py` using `RecursiveCharacterTextSplitter`. Reads `chunk_size` / `chunk_overlap` from `config.yaml` with automatic fallback to 2000/200. Metadata fully propagated to all chunks via LangChain's `split_documents()`.
- No custom config loader abstraction required — `yaml.safe_load` used directly, consistent with scraper patterns.
- Unit test stub created; detailed tests skipped per user instruction.

### File List
- `ingestion/loader.py` (created)
- `ingestion/splitter.py` (created)
- `tests/ingestion/test_loader.py` (created — stub)
