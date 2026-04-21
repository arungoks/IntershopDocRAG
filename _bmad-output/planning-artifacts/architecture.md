---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments: ['prd.md', 'product-brief-IntershopRAG.md', 'product-brief-IntershopRAG-distillate.md', 'ux-design-specification.md', 'ux-design-directions.html']
workflowType: 'architecture'
project_name: 'IntershopRAG'
user_name: 'Arun'
date: '2026-03-28'
lastStep: 8
status: 'complete'
completedAt: '2026-03-28'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**
- **Extraction Pipeline:** Automated Microsoft Entra ID authentication, async fetching/throttling, HTML-to-Markdown parsing with structure preservation, and state checkpointing. Architecturally requires decoupled scraper units (Auth, Fetch, Parse, State).
- **RAG Interaction:** Natural language querying, local vector retrieval, grounded generation with citations, and session memory. Architecturally requires vector DB integration, local LLM orchestration, and Streamlit state management.

**Non-Functional Requirements:**
- **Security:** 100% local execution (Ollama/ChromaDB). No cloud LLM APIs. Secrets strictly isolated locally.
- **Performance:** Sub-5 second generation latency; concurrent scraping (3-5 workers) with polite rate-limiting.
- **Reliability:** Autonomous expired-token recovery and exponential backoff on HTTP/429 errors.

**Scale & Complexity:**
Medium complexity greenfield developer tool.

- Primary domain: Data Extraction Pipeline & Local RAG Web App (Python)
- Complexity level: Medium (due to headless Auth & AI orchestration)
- Estimated architectural components: ~8 (Auth module, Fetcher, Parser, State Manager, ChromaDB interface, Ollama Interface, Streamlit UI, Orchestrator/CLI)

### Technical Constraints & Dependencies

- **Platform:** Fully local execution optimized for developer workstations (targeting Windows).
- **Stack:** Python 3.10+, Playwright (for MS Entra ID), `httpx`, `trafilatura`, `langchain`, `langchain-chroma`, `langchain-ollama`, `streamlit`.
- **UI Constraints:** UI must be built strictly with Streamlit native components, avoiding complex custom React frontend libraries.

### Cross-Cutting Concerns Identified

- **Resilience and State:** Checkpointing and recovery span across multiple pipeline phases.
- **Configuration Management:** Centralized handling of URLs, selectors, DB paths, and model names.
- **Security/Creds Management:** Ensuring the scraper can securely access local credentials without exposing them to version control.

## Starter Template Evaluation

### Primary Technology Domain

Full-stack Python (CLI Scraper & Streamlit Web App) based on project requirements analysis.

### Starter Options Considered

1. **Standard Cookiecutter Python CLI**: Great for the scraper portion, but often rigidly tailored only for CLI distribution, making the Streamlit integration clunky.
2. **Standard Streamlit RAG Boilerplates**: Typically tightly coupled with LangChain or LlamaIndex. The PRD explicitly specifies a leaner stack using Ollama and ChromaDB directly to maintain maximum control over the context.
3. **Astral's `uv` Project Initialization (Selected)**: The modern, lightning-fast standard for Python project scaffolding. It provides the perfect unopinionated foundation for a dual-purpose architecture while managing dependencies flawlessly.

### Selected Starter: Astral `uv` Project Initialization

**Rationale for Selection:**
The IntershopRAG project is unique because it requires both a robust headless scraping pipeline and a parallel web-based Chat UI. Initializing a modern Python project via `uv` gives us a clean `pyproject.toml` foundation. We can cleanly isolate our `scraper/` module from our `app.py` Streamlit entrypoint without fighting framework-specific bloat or opinionated folder structures. Furthermore, adopting `trafilatura` perfectly aligns with this lean philosophy, eliminating the need for separate `beautifulsoup4` and `markdownify` parsing steps.

**Initialization Command:**

```bash
uv init .
uv add httpx trafilatura playwright langchain langchain-chroma langchain-ollama streamlit rich
uv run playwright install chromium
```

**Architectural Decisions Provided by Starter:**

**Language & Runtime:**
Python 3.10+ managed via `uv`, leveraging `pyproject.toml` for standard packaging and robust virtual environment isolation.

**Styling Solution:**
Native Streamlit theming configured strictly via `.streamlit/config.toml` to mandate the Dark Mode "IDE-like" aesthetic detailed in the UX specs.

**Build Tooling:**
`uv` acts as the ultra-fast package manager and build backend (replacing pip/poetry), ensuring highly deterministic and fast installs across developer workstations.

**Testing Framework:**
Standard `pytest` integration housed in a dedicated `tests/` directory.

**Code Organization:**
```text
.
├── pyproject.toml
├── scraper/             # CLI scraping pipeline
│   ├── auth.py
│   ├── fetcher.py
│   └── main.py
├── app.py               # Streamlit UI entry point
└── .streamlit/
    └── config.toml      # Theme configuration
```

**Development Experience:**
Extremely fast dependency resolution. Developers run the pipeline via `uv run python scraper/main.py` or the chat UI via `uv run streamlit run app.py`.

**Note:** Project initialization using this command should be the first implementation story.

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
- Data Architecture: Local Inference Model (Qwen 2.5 7B)
- Data Architecture: Embedding Model (nomic-embed-text)

**Important Decisions (Shape Architecture):**
- Frontend Architecture: Custom "Footnote Scholar" citation markdown rendering in Streamlit.
- Extraction Architecture: Consolidate parsing into `trafilatura` over BS4.

**Deferred Decisions (Post-MVP):**
- Expanding the scraper beyond the primary knowledge base sitemap to Jira tickets and User Manuals.

### Data Architecture

- **Local Generation Model:** `qwen2.5:7b` (via Ollama 0.18.3). *Rationale:* Exceptional capability for processing technical API questions and outputting structural markdown without hallucination.
- **Embedding Model:** `nomic-embed-text` (via Ollama). *Rationale:* A massive 8192-token context window ensures the semantic meaning of deep Intershop technical articles is maintained, reducing fragmentation when parsing large code snippets.
- **Vector Store:** ChromaDB (v1.5.5). *Rationale:* Persistent, localized local database embedded directly into the python process via `PersistentClient`.

### Authentication & Security

- **Login Flow:** Headless Playwright script storing Microsoft Entra ID cookies. *Rationale:* Only viable mechanism to bypass complex proprietary SSO gateways.
- **Secret Storage:** Strict local `creds.txt` isolation. *Rationale:* Assures proprietary documentation isn't leaked; complies with the strictly zero-cloud mandate.

### API & Communication Patterns

- **Scraper Pipeline:** `httpx` async workers controlled by an `asyncio.Semaphore`. *Rationale:* Provides polite rate-limiting while fetching 2,400+ pages concurrently.
- **LLM Context Flow:** LangChain LCEL retrieval chain via `langchain-ollama` and `langchain-chroma`. *Rationale:* Provides battle-tested abstractions for document loading, text splitting, embedding, and retrieval while keeping the stack modular via dedicated integration packages.

### Frontend Architecture

- **Framework:** Streamlit (v1.55.0).
- **UX Strategy:** "The Footnote Scholar" layout. Chat history maintains context natively through `st.session_state`. Reference documents are cited clearly via inline `st.markdown()` injections at the base of every AI response.

### Infrastructure & Deployment

- **Execution Environment:** Windows Developer Workstations. No cloud hosting topology required.
- **Dependency Management:** Python project initialized via Astral `uv`.

### Decision Impact Analysis

**Implementation Sequence:**
1. Initialize Project System (Astral `uv` environment mapping).
2. Build Scraper Pipeline (`auth.py` -> Playwright; `fetcher.py` -> `httpx` and `trafilatura`; `state.py` -> checkpoint manager).
3. Build LangChain Ingestion Pipeline (DirectoryLoader -> RecursiveCharacterTextSplitter -> OllamaEmbeddings + Chroma).
4. Build LangChain RAG Chain + Streamlit UI (ChatOllama + Chroma retriever -> LCEL chain -> Streamlit chat).

**Cross-Component Dependencies:**
- The Streamlit UI strictly relies on the metadata extracted during the scraping phase by `trafilatura` (titles, URLs, IDs) to form its verifiable user-facing citations.

## Implementation Patterns & Consistency Rules

### Pattern Categories Defined

**Critical Conflict Points Identified:**
4 areas where AI agents could make conflicting choices (UI Organization, State Checkpointing, Markdown Formatting, Python Naming).

### Naming Patterns

**Python Naming Conventions:**
- Standard PEP-8 compliance is strictly enforced.
- Variables and functions: `snake_case` (e.g., `extract_metadata()`).
- Classes: `PascalCase` (e.g., `KnowledgeBaseScraper`).
- Constants/Config keys: `UPPER_SNAKE_CASE` (e.g., `START_URL`, `OLLAMA_PORT`).

**File Naming Conventions:**
- Python files: `snake_case.py`.
- Markdown outputs from scraper: `{page_id}.md` (e.g., `2C9117.md`) to prevent OS-level path issues with long titles.

### Structure Patterns

**Project Organization:**
- Scraper module must remain entirely functionally decoupled from the Streamlit UI. They only share the ChromaDB directory and the Markdown output directory.
- `scraper/`: Logic for HTTP, auth, and parsing.
- `ui/`: Helper logic for Streamlit renders (e.g., custom UI components) to keep `app.py` clean.
- `data/`: The isolated directory where ChromaDB local files (`data/vectordb/`) and scraped markdown (`data/raw_md/`) are stored.

### Format Patterns

**Markdown YAML Frontmatter Formats:**
Every markdown file generated by the pipeline MUST contain the exact following YAML frontmatter keys to ensure the Streamlit citation pipeline doesn't crash:
```yaml
---
id: "{unique_page_id}"
title: "{extracted_title}"
url: "https://knowledge.intershop.com/.../{id}"
scraped_at: "YYYY-MM-DDTHH:MM:SS"
---
```

**Checkpoint State Format:**
The scraper's resume file (`scrape_state.json`) MUST use a dictionary mapping to track status:
```json
{
  "https://target-url.com": {
    "status": "success|failed|skipped",
    "retries": 1,
    "last_attempt": "ISO-8601-date"
  }
}
```

### Process Patterns

**Error Handling Patterns:**
- **Scraper Pipeline:** Never fail silently on HTTP 403/401 errors. If Microsoft Entra ID invalidates a cookie, the pipeline must catch the `httpx.HTTPStatusError`, trigger the Playwright auth refresh, and retry gracefully.
- **Streamlit UI:** If Ollama or ChromaDB is offline, wrap the `st.error()` message with clear instructions (e.g., "Ollama service is unreachable. Please ensure `ollama run qwen2.5` is active.").

### Enforcement Guidelines

**All AI Agents MUST:**
- Isolate Playwright strictly to `scraper/auth.py`. `httpx` and `trafilatura` handle the rest in `scraper/fetcher.py`.
- Ensure all scraped URLs are rewritten to Absolute URLs so citation links work directly from the chat UI without relative path failures.

### Pattern Examples

**Good Examples:**
```python
# Proper Streamlit chat isolation
import streamlit as st
from ui.citations import render_citation_footer

st.chat_message("assistant").write_stream(ollama_response)
render_citation_footer(retrieved_docs)
```

**Anti-Patterns:**
```python
# Anti-Pattern: Hardcoding Playwright across the app
# DO NOT DO THIS. Playwright should ONLY be used to secure the cookie exactly once per session.
page = browser.new_page()
page.goto("https://knowledge.intershop.com/kb/...")
html = page.content()
```

## Project Structure & Boundaries

### Complete Project Directory Structure

```text
IntershopRAG/
├── README.md
├── pyproject.toml               # uv project configuration & dependencies
├── uv.lock
├── config.yaml                  # Centralized project settings (paths, model names, chunk sizes)
├── creds.txt                    # (Gitignored) MS Entra ID credentials
├── .gitignore
├── scrape_state.json            # (Gitignored) Stateful URL processing tracker
├── .streamlit/
│   └── config.toml              # Streamlit Dark Mode theme configuration
├── data/                        # (Gitignored) Local data tier
│   ├── raw_md/                  # Output destination for trafilatura pipeline
│   └── vectordb/                # Persistent ChromaDB local vector storage
├── scraper/                     # The Extraction Pipeline Boundary
│   ├── __init__.py
│   ├── main.py                  # CLI orchestrator & Async Semaphore manager
│   ├── auth.py                  # Playwright headless MS Entra ID logic
│   ├── fetcher.py               # httpx + trafilatura HTML-to-MD logic
│   └── state.py                 # Checkpoint reader/writer for scrape_state.json
├── ingestion/                   # The Vector Processing Boundary (LangChain)
│   ├── __init__.py
│   ├── loader.py                # LangChain DirectoryLoader for raw_md/
│   ├── splitter.py              # RecursiveCharacterTextSplitter config
│   └── embedder.py              # LangChain OllamaEmbeddings + Chroma pipeline
├── ui/                          # The RAG Chat Boundary (LangChain + Streamlit)
│   ├── __init__.py
│   ├── app.py                   # Main Streamlit Entry Point
│   ├── chain.py                 # LangChain LCEL retrieval chain (ChatOllama + Chroma retriever)
│   └── citations.py             # Custom markdown "Footnote Scholar" UI rendering
└── tests/
    ├── conftest.py
    ├── scraper/
    │   ├── test_auth.py
    │   └── test_fetcher.py
    ├── ingestion/
    │   └── test_embedder.py
    └── ui/
        ├── test_chain.py
        └── test_citations.py
```

### Architectural Boundaries

**The Extraction Boundary (`scraper/`):**
This module has zero knowledge of AI, LangChain, ChromaDB, or Streamlit. Its sole purpose is to securely acquire the MS Entra ID cookie, parse `knowledge.intershop.com`, and dump sanitized Markdown to `data/raw_md/`.

**The Semantic Boundary (`ingestion/`):**
This module uses LangChain abstractions to bridge raw data and the AI system. It loads markdown via `DirectoryLoader`, splits it with `RecursiveCharacterTextSplitter`, embeds via `OllamaEmbeddings` (nomic-embed-text), and persists to ChromaDB via `langchain-chroma`.

**The Interaction Boundary (`ui/`):**
This module uses a LangChain LCEL retrieval chain (`ChatOllama` + `Chroma` retriever) to query `data/vectordb/` for context, generate grounded answers, and surface citations via the custom Streamlit UI.

### Requirements to Structure Mapping

**Feature/Epic Mapping:**
- **Epic: Authentication & Session Management:** Maps to `scraper/auth.py` and `creds.txt`
- **Epic: Pipeline Orchestration & Checkpointing:** Maps to `scraper/main.py` and `scraper/state.py`
- **Epic: Content Parsing:** Maps to `scraper/fetcher.py` and `data/raw_md/`
- **Epic: Vector Ingestion:** Maps to `ingestion/loader.py`, `ingestion/splitter.py`, `ingestion/embedder.py`
- **Epic: RAG Chat Experience:** Maps to `ui/app.py`, `ui/chain.py`, and `ui/citations.py`

**Cross-Cutting Concerns:**
- **NFR Security (Local Execution):** Enforced by configuring `ChatOllama` and `OllamaEmbeddings` strictly against `localhost:11434`.
- **Configuration Management:** Centralized in `config.yaml` (model names, chunk sizes, DB paths) and `creds.txt` (secrets).

### Integration Points

**Internal Communication:**
The three boundaries communicate strictly sequentially via the File System and Local Database (`data/` directory). No direct imports between `scraper/`, `ingestion/`, and `ui/`.

**External Integrations:**
- **Microsoft Entra ID:** Only accessible via `scraper/auth.py` (Headless Chromium).
- **Ollama Engine:** Accessed via LangChain's `OllamaEmbeddings` (in `ingestion/`) and `ChatOllama` (in `ui/chain.py`), both targeting `localhost:11434`.

## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:**
All technology choices are fully compatible. LangChain's modular integration packages (`langchain-chroma`, `langchain-ollama`) seamlessly wrap the previously-decided ChromaDB vector store and Ollama inference engine. `trafilatura` outputs clean markdown that LangChain's `DirectoryLoader` natively consumes. No version conflicts detected.

**Pattern Consistency:**
PEP-8 naming conventions, the mandatory YAML frontmatter schema, and the file-system-mediated boundary communication all align consistently. The checkpoint JSON format supports the resilience requirements without conflicting with the LangChain ingestion pipeline.

**Structure Alignment:**
The three-boundary architecture (`scraper/`, `ingestion/`, `ui/`) enforces strict decoupling. The `data/` directory acts as the sole shared interface, eliminating any circular import or tight-coupling risks.

### Requirements Coverage Validation ✅

**Functional Requirements Coverage:**
| FR | Coverage | Component |
|---|---|---|
| FR1-FR3 (Auth & Session) | ✅ | `scraper/auth.py` (Playwright) |
| FR4-FR7 (Pipeline Orchestration) | ✅ | `scraper/main.py` + `rich` console |
| FR8-FR11 (Fetching & State) | ✅ | `scraper/fetcher.py` + `scraper/state.py` |
| FR12-FR14 (Content Parsing) | ✅ | `scraper/fetcher.py` (trafilatura) |
| FR15-FR19 (RAG Chat) | ✅ | `ui/app.py` + `ui/chain.py` + `ui/citations.py` (LangChain LCEL) |

**Non-Functional Requirements Coverage:**
| NFR | Coverage | Mechanism |
|---|---|---|
| NFR-P1 (Sub-5s response) | ✅ | Local Ollama inference + local ChromaDB retrieval |
| NFR-P2 (Concurrent scraping) | ✅ | `asyncio.Semaphore` in `scraper/main.py` |
| NFR-S1 (Credential isolation) | ✅ | `creds.txt` strictly `.gitignore`'d |
| NFR-S2 (100% local LLM) | ✅ | `ChatOllama` and `OllamaEmbeddings` configured against `localhost` only |
| NFR-R1 (Retry with backoff) | ✅ | `scraper/fetcher.py` error handling pattern |
| NFR-R2 (Cookie expiry recovery) | ✅ | `scraper/auth.py` re-auth flow triggered by `scraper/fetcher.py` |

### Implementation Readiness Validation ✅

**Decision Completeness:**
All critical technology decisions are documented with verified versions (Ollama 0.18.3, ChromaDB 1.5.5, Streamlit 1.55.0, trafilatura 2.0.0). LangChain integration packages are specified.

**Structure Completeness:**
Every file and directory is explicitly defined in the project tree with clear purpose annotations. No generic placeholders remain.

**Pattern Completeness:**
Naming, frontmatter format, checkpoint state format, error handling, and boundary enforcement are all documented with concrete examples and anti-patterns.

### Gap Analysis Results

**Critical Gaps:** None identified.

**Important Gaps (Non-Blocking):**
- **Chunking Strategy Details:** The exact `chunk_size` and `chunk_overlap` for `RecursiveCharacterTextSplitter` should be tuned during implementation based on the actual Intershop article lengths. Recommended starting point: `chunk_size=2000`, `chunk_overlap=200` to leverage `nomic-embed-text`'s 8192-token window.
- **System Prompt Template:** The exact LLM system prompt enforcing citation behavior and grounded-only answers should be crafted during the RAG chain implementation story.

### Architecture Completeness Checklist

**✅ Requirements Analysis**
- [x] Project context thoroughly analyzed
- [x] Scale and complexity assessed
- [x] Technical constraints identified
- [x] Cross-cutting concerns mapped

**✅ Architectural Decisions**
- [x] Critical decisions documented with versions
- [x] Technology stack fully specified
- [x] Integration patterns defined
- [x] Performance considerations addressed

**✅ Implementation Patterns**
- [x] Naming conventions established
- [x] Structure patterns defined
- [x] Communication patterns specified
- [x] Process patterns documented

**✅ Project Structure**
- [x] Complete directory structure defined
- [x] Component boundaries established
- [x] Integration points mapped
- [x] Requirements to structure mapping complete

### Architecture Readiness Assessment

**Overall Status:** READY FOR IMPLEMENTATION

**Confidence Level:** High

**Key Strengths:**
- Clean three-boundary architecture with zero coupling between scraper, ingestion, and UI.
- LangChain provides robust, maintained abstractions for the RAG chain while keeping the scraper lean and custom.
- `trafilatura` eliminates multiple parsing dependencies in favor of a single, purpose-built extraction library.
- Every file in the project tree has a clear, singular purpose.

**Areas for Future Enhancement:**
- Expanding the scraper to cover User Manuals (`/oh/`) and Product Releases (`/prd/`).
- Adding hybrid search (keyword + semantic) to the retrieval chain for improved precision.
- IDE integration (VS Code extension) for in-editor knowledge access.

### Implementation Handoff

**AI Agent Guidelines:**
- Follow all architectural decisions exactly as documented
- Use implementation patterns consistently across all components
- Respect project structure and boundaries
- Refer to this document for all architectural questions

**First Implementation Priority:**
```bash
uv init .
uv add httpx trafilatura playwright langchain langchain-chroma langchain-ollama streamlit rich
uv run playwright install chromium
```
