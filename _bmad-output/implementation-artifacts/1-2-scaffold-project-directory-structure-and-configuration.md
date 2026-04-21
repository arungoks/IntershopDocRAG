# Story 1.2: Scaffold Project Directory Structure & Configuration

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a developer,
I want the canonical project directory structure and centralized configuration files created,
So that all future code is organized into the correct architectural boundaries from the start.

## Acceptance Criteria

1. **Given** the initialized `uv` project from Story 1.1 **When** the developer inspects the project structure **Then** the following directories exist with `__init__.py` files: `scraper/`, `ingestion/`, `ui/`, `tests/`, `tests/scraper/`, `tests/ingestion/`, `tests/ui/`
2. **And** the `data/raw_md/` and `data/vectordb/` directories exist (or are created at runtime)
3. **And** a root `config.yaml` exists with placeholder keys for `start_url`, `sitemap_url`, `ollama_port`, `ollama_model`, `embedding_model`, `chroma_db_path`, `raw_md_path`, `chunk_size`, `chunk_overlap`
4. **And** a `.gitignore` exists that excludes `creds.txt`, `scrape_state.json`, `data/`, `.venv/`, `__pycache__/`
5. **And** a `.streamlit/config.toml` exists that configures the Dark Mode theme (background `#0E1117`, text `#FAFAFA`, accent `#569CD6`)
6. **And** a `tests/conftest.py` exists as an empty pytest configuration file
7. **And** a `README.md` exists with a project overview and setup instructions

## Tasks / Subtasks

- [x] Task 1: Create Python package directories (AC: #1)
  - [x] Create `scraper/`, `ingestion/`, `ui/`, `tests/`, `tests/scraper/`, `tests/ingestion/`, `tests/ui/` with empty `__init__.py` files.
- [x] Task 2: Create state and data directories (AC: #2)
  - [x] Ensure logic exists or shell structure is primed for `data/raw_md/` and `data/vectordb/`.
- [x] Task 3: Setup configuration files (AC: #3, #5, #6, #7)
  - [x] Create `config.yaml` with the necessary YAML placeholders.
  - [x] Create `.streamlit/config.toml` targeting the Dark Mode specs.
  - [x] Create `tests/conftest.py`.
  - [x] Create baseline `README.md`.
- [x] Task 4: Setup Git ignore rules (AC: #4)
  - [x] Create `.gitignore` to omit credentials, state files, databases, and venv artifacts.

## Dev Notes

- **Architecture Compliance:** Architectural boundaries dictate three explicitly decoupled modules (`scraper/`, `ingestion/`, `ui/`).
- **Data flow:** The only point of communication between these modules is via the `data/` directory (Markdown files or Vector store).

### Project Structure Notes

- Project boundaries are formalized in this story. Future code must adhere to these module lines.

### References

- [Source: `_bmad-output/planning-artifacts/prd.md#Installation & Environment Setup`]
- [Source: `_bmad-output/planning-artifacts/architecture.md#Architectural Boundaries`]
- [Source: `_bmad-output/planning-artifacts/epics.md#Story 1.2`]

## Dev Agent Record

### Agent Model Used

Claude Sonnet (Thinking)

### Debug Log References

- All directories created via PowerShell `New-Item -ItemType Directory`; `__init__.py` files created with `New-Item -ItemType File`.
- `.gitignore` extended (not replaced) from uv-generated baseline to add all required IntershopRAG exclusions (creds.txt, scrape_state.json, data/).
- `.gitkeep` files added to `data/raw_md/` and `data/vectordb/` so Git tracks the directories while the data itself is gitignored.

### Completion Notes List

- ✅ AC1: 7 package dirs + 6 `__init__.py` files created (scraper, ingestion, ui, tests, tests/scraper, tests/ingestion, tests/ui)
- ✅ AC2: `data/raw_md/` and `data/vectordb/` created with `.gitkeep` sentinels
- ✅ AC3: `config.yaml` with all 9 required keys (start_url, sitemap_url, ollama_port, ollama_model, embedding_model, chroma_db_path, raw_md_path, chunk_size=2000, chunk_overlap=200)
- ✅ AC4: `.gitignore` updated to exclude creds.txt, scrape_state.json, data/, .venv/, __pycache__/
- ✅ AC5: `.streamlit/config.toml` configured with Dark Mode: backgroundColor=#0E1117, textColor=#FAFAFA, primaryColor=#569CD6
- ✅ AC6: `tests/conftest.py` created
- ✅ AC7: Comprehensive `README.md` created (setup, usage, structure, tech stack documentation)
- ✅ 55 pytest tests pass (41 new + 14 from Story 1.1) — zero regressions

### File List

- `scraper/__init__.py` (created)
- `ingestion/__init__.py` (created)
- `ui/__init__.py` (created)
- `tests/__init__.py` (created — Note: tests dir already existed from Story 1.1)
- `tests/scraper/__init__.py` (created)
- `tests/ingestion/__init__.py` (created)
- `tests/ui/__init__.py` (created)
- `data/raw_md/.gitkeep` (created)
- `data/vectordb/.gitkeep` (created)
- `config.yaml` (created)
- `.streamlit/config.toml` (created)
- `tests/conftest.py` (created)
- `README.md` (created)
- `.gitignore` (updated — extended with IntershopRAG-specific rules)
- `tests/test_project_structure.py` (created)
