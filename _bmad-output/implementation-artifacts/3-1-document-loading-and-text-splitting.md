# Story 3.1: Document Loading & Text Splitting

Status: ready-for-dev

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

- [ ] Task 1: Implement `ingestion/loader.py` (AC: 1, 3, 5)
  - [ ] Implement a function or class to load `.md` files from `data/raw_md/` using LangChain's Document structure.
  - [ ] Ensure that YAML frontmatter is explicitly parsed and assigned to the LangChain Document `metadata` property (e.g. using `python-frontmatter` or `yaml` modules, since default `TextLoader` does not extract YAML frontmatter).
- [ ] Task 2: Implement `ingestion/splitter.py` (AC: 2, 4, 5)
  - [ ] Read `chunk_size` and `chunk_overlap` properties from the centralized `config.yaml` using a YAML parser. Fallback to 2000 and 200 if not present.
  - [ ] Instantiate `RecursiveCharacterTextSplitter` from LangChain.
  - [ ] Implement a function to take a list of loaded `Document` objects and return a list of split `Document` objects.
  - [ ] Verify that metadata (`id`, `title`, `url`, `scraped_at`) is correctly propagated to all resulting document chunks.
- [ ] Task 3: Unit Testing
  - [ ] Add pytest tests in `tests/ingestion/test_loader.py` and `tests/ingestion/test_splitter.py` using mock files and `config.yaml`.

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

Gemini 3.1 Pro (High)

### Debug Log References

### Completion Notes List

- Comprehensive dev guide created covering edge cases around frontmatter parsing and config usage.

### File List
- `ingestion/loader.py` (to be created/updated)
- `ingestion/splitter.py` (to be created/updated)
- `tests/ingestion/test_loader.py` (to be created)
- `tests/ingestion/test_splitter.py` (to be created)
---
