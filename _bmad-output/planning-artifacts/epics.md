---
stepsCompleted: ['step-01-validate-prerequisites', 'step-02-design-epics', 'step-03-create-stories', 'step-04-final-validation']
inputDocuments:
  - '_bmad-output/planning-artifacts/prd.md'
  - '_bmad-output/planning-artifacts/architecture.md'
  - '_bmad-output/planning-artifacts/ux-design-specification.md'
---

# IntershopRAG - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for IntershopRAG, decomposing the requirements from the PRD, UX Design, and Architecture into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: The system can programmatically authenticate through a Microsoft Entra ID portal.
FR2: The system can extract and persist valid authentication session cookies.
FR3: The system can detect expired or invalid auth states and re-authenticate autonomously without human intervention.
FR4: The system administrator can initiate the extraction pipeline via a command-line interface.
FR5: The system can read a target sitemap XML to generate a comprehensive queue of target URLs.
FR6: The system can output real-time processing progress and error logs to the administrator during execution.
FR7: The system can gracefully shut down operations when complete or critically interrupted.
FR8: The system can download multiple web payloads concurrently (asynchronously).
FR9: The system can throttle its own request rate to respond gracefully to target server limits or timeouts.
FR10: The system can record the exact success/failure status of every individual URL processed.
FR11: The system can use persisted state records to skip already-downloaded pages on subsequent runs (Differential Sync).
FR12: The system can convert raw scraped HTML into structured Markdown files locally.
FR13: The system can preserve critical semantic elements during conversion, specifically tables, code blocks, and hyperlinks.
FR14: The system can inject standardized metadata (original URL, scrape timestamp, title) into the YAML frontmatter of every generated Markdown file.
FR15: The developer can interact with the system via natural language queries in a browser environment.
FR16: The system can retrieve local, proprietary domain knowledge matching the query intent.
FR17: The system can generate technical answers grounded solely in the retrieved context.
FR18: The system can surface direct, clickable citations to the exact original KB article corresponding to its answer.
FR19: The system can maintain a conversational memory buffer during a user's active session to handle follow-up queries.

### NonFunctional Requirements

NFR-P1: The Phase 2 RAG chat interface must return a generated answer and citations to a user query within 5 seconds on average developer hardware.
NFR-P2: The Phase 1 extraction pipeline must process multiple web pages concurrently (e.g., 3-5 workers) while automatically respecting implicit connection limits to prevent DDoSing the internal Knowledge Base.
NFR-S1: All Microsoft Entra ID login credentials must be read from local environment files (creds.txt) that are strictly excluded from version control.
NFR-S2: The LLM integration (Phase 2) must execute 100% locally via Ollama; proprietary Intershop documentation must never be transmitted to external, cloud-hosted AI APIs for generation or embedding.
NFR-R1: The asynchronous fetching engine must automatically retry failed HTTP requests up to 3 times with exponential backoff before marking a target URL as permanently failed.
NFR-R2: If the Playwright session cookie expires mid-scrape, the system must pause HTTP requests, automatically re-trigger the headless login flow, and seamlessly resume fetching without losing queue state.

### Additional Requirements

- **Starter Template:** Astral `uv` project initialization is the first implementation story (`uv init .` → `uv add httpx trafilatura playwright langchain langchain-chroma langchain-ollama streamlit rich` → `uv run playwright install chromium`).
- **HTML-to-Markdown Engine:** The architecture mandates `trafilatura` as the single extraction library, replacing the PRD's original BS4+markdownify approach.
- **RAG Orchestration:** LangChain LCEL retrieval chain via dedicated integration packages (`langchain-ollama`, `langchain-chroma`).
- **Local Generation Model:** `qwen2.5:7b` via Ollama 0.18.3.
- **Embedding Model:** `nomic-embed-text` via Ollama with 8192-token context window.
- **Vector Store:** ChromaDB v1.5.5 using `PersistentClient` for local persistence in `data/vectordb/`.
- **Centralized Configuration:** All project settings (paths, model names, chunk sizes) managed via a root `config.yaml`.
- **Architectural Boundaries:** Three strictly decoupled modules — `scraper/` (extraction), `ingestion/` (vector processing), `ui/` (RAG chat) — communicating only via the `data/` directory.
- **Mandatory YAML Frontmatter:** Every scraped markdown file must contain `id`, `title`, `url`, and `scraped_at` keys.
- **Checkpoint State Format:** `scrape_state.json` must use a dictionary mapping URLs to `{status, retries, last_attempt}`.
- **PEP-8 Naming:** Strictly enforced (`snake_case` functions/vars, `PascalCase` classes, `UPPER_SNAKE_CASE` constants).
- **Absolute URL Rewriting:** All scraped URLs must be rewritten to absolute URLs for citation link integrity.
- **Streamlit Theme:** Dark Mode configured via `.streamlit/config.toml`.
- **Chunking Strategy:** Recommended starting point `chunk_size=2000`, `chunk_overlap=200` for `RecursiveCharacterTextSplitter`.

### UX Design Requirements

UX-DR1: Implement Dark Mode theme configuration via `.streamlit/config.toml` enforcing IDE-like aesthetic (Background `#0E1117`, Primary Text `#FAFAFA`, Accent `#569CD6`, Citation Badge BG `#262730` with border `#4b4b4b`, Code Block BG `#000000`/`#151515`).
UX-DR2: Implement typography system using system sans-serif stack (Inter, Segoe UI, Roboto) for UI text and monospace stack (Fira Code, JetBrains Mono, Consolas) for code blocks, with increased line-height (1.6) for dense technical text readability.
UX-DR3: Build the Citation Footer custom component — a Python helper function that takes ChromaDB source metadata and renders a markdown separator (`---`) followed by sub-text styled (`font-size:0.8em; color:gray`) bulleted list of descriptive KB source links (opening in `target="_blank"`) below each assistant response.
UX-DR4: Build the Empty State component — a visually distinct centered block with brief onboarding text and 2-3 clickable example prompts (e.g., "Explain ICM vs IOM", "How do I create a new Pipeline?") that auto-populate or submit the query on click. Displayed on initial load and after clearing history.
UX-DR5: Implement retrieval-phase feedback using `st.spinner()` with specific, trust-building action text (e.g., "Querying ChromaDB for relevant articles...", "Initializing local Ollama model...") that disappears exactly when the first token streams.
UX-DR6: Implement error recovery patterns using `st.error()` with developer-friendly diagnostic messages and actionable fix instructions when Ollama or ChromaDB is offline (e.g., "Ollama service is unreachable. Please ensure `ollama run qwen2.5` is active.").
UX-DR7: Implement session state management for chat history using `st.session_state`, with a full-width "Clear Chat History" button in the left `st.sidebar` that wipes session state and triggers `st.rerun()` to reset to the Empty State.
UX-DR8: Implement the Input Lockout pattern — disable `st.chat_input` immediately upon submission and re-enable only after the full LLM response and Citation Footer have been completely rendered, preventing double-submissions.
UX-DR9: Implement the Scroll Pinning pattern — automatically scroll the user to the bottom of the chat as the LLM streams its response token-by-token.
UX-DR10: Implement keyboard-first interaction — `Enter` to submit queries, auto-focus the chat input on page load and after each response cycle, ensure all interactive elements (copy buttons, citation links) are reachable via `Tab` navigation.
UX-DR11: Implement responsive layout — center chat content with a max-width (~800px), use horizontal scrolling (`overflow-x: auto`) for wide code blocks, and rely on Streamlit's native sidebar collapse for viewports < 992px.
UX-DR12: Implement WCAG 2.1 Level AA accessibility — enforce minimum 4.5:1 contrast ratio (targeting AAA 7:1 for body text), ensure visible focus rings on the chat input, and use descriptive link text for all citation links (e.g., "Pipeline Concepts" not "Click Here").

### FR Coverage Map

FR1: Epic 2 - Programmatic MS Entra ID authentication
FR2: Epic 2 - Extract & persist session cookies
FR3: Epic 2 - Auto-detect expired auth & re-authenticate
FR4: Epic 2 - CLI-initiated extraction pipeline
FR5: Epic 2 - Sitemap XML parsing for URL queue
FR6: Epic 2 - Real-time progress & error logging
FR7: Epic 2 - Graceful shutdown on completion/interruption
FR8: Epic 2 - Concurrent async downloading
FR9: Epic 2 - Request rate throttling
FR10: Epic 2 - Per-URL success/failure status recording
FR11: Epic 2 - Differential sync (skip already-downloaded)
FR12: Epic 2 - HTML-to-Markdown conversion
FR13: Epic 2 - Table, code block, hyperlink preservation
FR14: Epic 2 - YAML frontmatter metadata injection
FR15: Epic 4 - Browser-based natural language queries
FR16: Epic 3 + Epic 4 - Local knowledge retrieval (ingestion + query)
FR17: Epic 4 - Grounded answer generation
FR18: Epic 4 - Clickable source citations
FR19: Epic 4 - Conversational memory buffer

## Epic List

### Epic 1: Project Foundation & Environment Setup
A developer can clone the repository, install all dependencies, and have a fully scaffolded, runnable project skeleton with correct architectural boundaries, configuration, and tooling — ready for feature development.
**FRs covered:** _(Foundation — enables all subsequent epics)_
**NFRs addressed:** NFR-S1 (credential isolation via .gitignore)
**Key Requirements:** Starter template (Astral `uv`), `pyproject.toml`, project directory structure (`scraper/`, `ingestion/`, `ui/`, `data/`, `tests/`), `config.yaml`, `.gitignore`, `.streamlit/config.toml`, PEP-8 enforcement, Playwright browser install.

### Epic 2: Authenticated Knowledge Base Extraction
A DevOps admin can run the CLI pipeline to autonomously authenticate through Microsoft Entra ID, scrape all 2,457 Knowledge Base pages concurrently, convert them to structured markdown with metadata, and resume interrupted runs — all without manual intervention.
**FRs covered:** FR1, FR2, FR3, FR4, FR5, FR6, FR7, FR8, FR9, FR10, FR11, FR12, FR13, FR14
**NFRs addressed:** NFR-P2, NFR-S1, NFR-R1, NFR-R2
**Key Requirements:** `trafilatura`, mandatory YAML frontmatter, `scrape_state.json` checkpoint format, absolute URL rewriting, `rich` console progress, `asyncio.Semaphore`.

### Epic 3: Vector Ingestion Pipeline
An admin can run the ingestion pipeline to process all scraped markdown files into a searchable local vector database, making the full Intershop Knowledge Base ready for AI-powered retrieval.
**FRs covered:** FR16 (partially — creates the retrieval foundation)
**NFRs addressed:** NFR-S2
**Key Requirements:** LangChain `DirectoryLoader`, `RecursiveCharacterTextSplitter` (chunk_size=2000, chunk_overlap=200), `OllamaEmbeddings` with `nomic-embed-text`, ChromaDB `PersistentClient` in `data/vectordb/`.

### Epic 4: RAG Chat Experience
A developer can open a browser, type a natural-language question about Intershop, and instantly receive an accurate, grounded answer with direct citations to the original Knowledge Base articles — all running 100% locally with conversation memory for follow-ups.
**FRs covered:** FR15, FR16, FR17, FR18, FR19
**NFRs addressed:** NFR-P1, NFR-S2
**Key Requirements:** LangChain LCEL retrieval chain, `ChatOllama` with `qwen2.5:7b`, Chroma retriever, `st.chat_message`/`st.chat_input`, `st.session_state` memory, Citation Footer, basic Streamlit UI.

### Epic 5: Chat UI Polish & Accessibility
Developers experience a professional, IDE-like chat interface with prominent citation footers, helpful empty states, clear error messages, keyboard-first interaction, and full accessibility compliance — building deep trust and flow-state productivity.
**FRs covered:** _(Enhances FR15, FR18, FR19 with UX polish)_
**NFRs addressed:** NFR-P1 (perceived performance)
**Key Requirements:** UX-DR1 through UX-DR12 — dark theme, typography, Citation Footer refinement, Empty State component, spinner feedback, error recovery, clear history, input lockout, scroll pinning, keyboard-first, responsive layout, WCAG AA accessibility.

## Epic 1: Project Foundation & Environment Setup

A developer can clone the repository, install all dependencies, and have a fully scaffolded, runnable project skeleton with correct architectural boundaries, configuration, and tooling — ready for feature development.

### Story 1.1: Initialize Python Project with Astral `uv`

As a developer,
I want the project initialized via Astral `uv` with all dependencies declared in `pyproject.toml`,
So that I can install the complete development environment with a single `uv sync` command.

**Acceptance Criteria:**

**Given** a fresh clone of the repository
**When** the developer runs `uv sync`
**Then** all dependencies are installed (`httpx`, `trafilatura`, `playwright`, `langchain`, `langchain-chroma`, `langchain-ollama`, `streamlit`, `rich`)
**And** a `pyproject.toml` exists at the project root with Python 3.10+ specified
**And** `uv run playwright install chromium` successfully installs the headless browser

### Story 1.2: Scaffold Project Directory Structure & Configuration

As a developer,
I want the canonical project directory structure and centralized configuration files created,
So that all future code is organized into the correct architectural boundaries from the start.

**Acceptance Criteria:**

**Given** the initialized `uv` project from Story 1.1
**When** the developer inspects the project structure
**Then** the following directories exist with `__init__.py` files: `scraper/`, `ingestion/`, `ui/`, `tests/`, `tests/scraper/`, `tests/ingestion/`, `tests/ui/`
**And** the `data/raw_md/` and `data/vectordb/` directories exist (or are created at runtime)
**And** a root `config.yaml` exists with placeholder keys for `start_url`, `sitemap_url`, `ollama_port`, `ollama_model`, `embedding_model`, `chroma_db_path`, `raw_md_path`, `chunk_size`, `chunk_overlap`
**And** a `.gitignore` exists that excludes `creds.txt`, `scrape_state.json`, `data/`, `.venv/`, `__pycache__/`
**And** a `.streamlit/config.toml` exists that configures the Dark Mode theme (background `#0E1117`, text `#FAFAFA`, accent `#569CD6`)
**And** a `tests/conftest.py` exists as an empty pytest configuration file
**And** a `README.md` exists with a project overview and setup instructions

## Epic 2: Authenticated Knowledge Base Extraction

A DevOps admin can run the CLI pipeline to autonomously authenticate through Microsoft Entra ID, scrape all 2,457 Knowledge Base pages concurrently, convert them to structured markdown with metadata, and resume interrupted runs — all without manual intervention.

### Story 2.1: Headless Microsoft Entra ID Authentication

As a system administrator,
I want the system to programmatically authenticate through the Microsoft Entra ID portal using a headless browser and persist the session cookies locally,
So that the scraping pipeline can access the protected Knowledge Base without manual login.

**Acceptance Criteria:**

**Given** valid credentials exist in a local `creds.txt` file (username on line 1, password on line 2)
**When** the `scraper/auth.py` module is executed
**Then** a headless Playwright Chromium browser navigates the MS Entra ID OAuth flow and successfully authenticates
**And** the extracted session cookies are returned as a dictionary usable by `httpx`
**And** if `creds.txt` is missing or credentials are invalid, a clear error message is raised
**And** Playwright logic is strictly isolated to `scraper/auth.py` — no other module imports Playwright

### Story 2.2: Sitemap Parsing & URL Queue Generation

As a system administrator,
I want the system to read the Knowledge Base sitemap XML and generate a complete queue of target URLs,
So that I know exactly which pages need to be scraped.

**Acceptance Criteria:**

**Given** a valid sitemap URL is configured in `config.yaml`
**When** the sitemap parser runs
**Then** it fetches the sitemap XML using the authenticated cookies from Story 2.1
**And** it extracts all `<loc>` URLs into an ordered list
**And** it logs the total count of URLs discovered (e.g., "Discovered 2,457 URLs from sitemap")
**And** if the sitemap fetch fails (HTTP error), a clear error message is raised

### Story 2.3: State Checkpoint Manager

As a system administrator,
I want the system to persist the processing status of every URL to a local `scrape_state.json` file,
So that interrupted scrapes can resume without re-downloading already-completed pages.

**Acceptance Criteria:**

**Given** the `scraper/state.py` module is initialized
**When** a URL is processed (success or failure)
**Then** its status is recorded in `scrape_state.json` with the format: `{"url": {"status": "success|failed|skipped", "retries": N, "last_attempt": "ISO-8601"}}`
**And** on subsequent pipeline runs, URLs with `"status": "success"` are automatically skipped
**And** if `scrape_state.json` does not exist, a new empty state file is created
**And** the state file is read/written atomically to prevent corruption from interrupted writes

### Story 2.4: Async HTTP Fetcher with Rate Limiting & Retries

As a system administrator,
I want the system to download multiple web pages concurrently with automatic rate limiting and retry logic,
So that the full Knowledge Base can be fetched efficiently without overwhelming the target server.

**Acceptance Criteria:**

**Given** a list of target URLs and valid session cookies
**When** the `scraper/fetcher.py` async engine processes the queue
**Then** it downloads pages concurrently using `httpx.AsyncClient` with an `asyncio.Semaphore` limiting to 3-5 workers
**And** HTTP 429/503 responses trigger automatic backoff before retrying
**And** failed requests are retried up to 3 times with exponential backoff before being marked as `"failed"` in the state file
**And** each URL's result (success/failure) is recorded via the State Checkpoint Manager (Story 2.3)

### Story 2.5: HTML-to-Markdown Conversion with Metadata

As a system administrator,
I want each fetched HTML page to be converted into a clean Markdown file with YAML frontmatter metadata,
So that the local documentation repository is structured, searchable, and preserves critical content.

**Acceptance Criteria:**

**Given** a raw HTML payload fetched by the async engine
**When** `trafilatura` processes the HTML
**Then** the output is a clean Markdown file preserving tables, code blocks, and hyperlinks
**And** all internal URLs are rewritten to absolute URLs (e.g., `https://knowledge.intershop.com/...`)
**And** a YAML frontmatter header is injected containing: `id` (unique page ID), `title` (extracted page title), `url` (original absolute URL), `scraped_at` (ISO-8601 timestamp)
**And** the Markdown file is saved to `data/raw_md/{page_id}.md`
**And** if `trafilatura` fails to extract content, the URL is marked as `"failed"` in the state file with an error log

### Story 2.6: Cookie Expiry Detection & Auto-Reauthentication

As a system administrator,
I want the system to detect expired authentication cookies mid-scrape and automatically re-authenticate without losing progress,
So that long-running scrapes of 2,457 pages complete autonomously even when tokens expire.

**Acceptance Criteria:**

**Given** the async fetcher encounters an HTTP 401 or 403 response during a scrape run
**When** the fetcher detects this authentication failure
**Then** it pauses all in-flight HTTP requests
**And** it triggers the `scraper/auth.py` module to perform a fresh headless Playwright login
**And** it updates the session cookies in the `httpx.AsyncClient`
**And** it resumes fetching from where it left off without losing queue state or re-downloading successful pages
**And** if reauthentication fails after 2 attempts, the pipeline shuts down gracefully with a clear error

### Story 2.7: CLI Pipeline Orchestrator with Real-Time Progress

As a system administrator,
I want to initiate the entire extraction pipeline via a single CLI command and see real-time progress,
So that I have full visibility into the scraping operation and can run it hands-free.

**Acceptance Criteria:**

**Given** the system administrator runs `uv run python scraper/main.py`
**When** the pipeline executes
**Then** it orchestrates the full flow: authenticate → parse sitemap → load state → fetch pages → convert to markdown → save state
**And** a `rich` console displays real-time progress (e.g., progress bar, pages completed/total, errors encountered)
**And** error logs are printed to stderr with timestamps and the failing URL
**And** when all URLs are processed (or all retries exhausted), the pipeline outputs a summary (total success, failed, skipped counts) and exits cleanly
**And** if the pipeline is interrupted (e.g., Ctrl+C), it saves the current state to `scrape_state.json` before exiting

## Epic 3: Vector Ingestion Pipeline

An admin can run the ingestion pipeline to process all scraped markdown files into a searchable local vector database, making the full Intershop Knowledge Base ready for AI-powered retrieval.

### Story 3.1: Document Loading & Text Splitting

As a system administrator,
I want the system to load all scraped markdown files from disk and split them into semantic chunks,
So that large documentation pages can be intelligently embedded into the vector database.

**Acceptance Criteria:**

**Given** the scraper has populated `data/raw_md/` with Markdown files
**When** the `ingestion/loader.py` and `ingestion/splitter.py` modules are executed
**Then** LangChain's `DirectoryLoader` successfully loads all `.md` files
**And** LangChain's `RecursiveCharacterTextSplitter` splits the text using `chunk_size` and `chunk_overlap` configured in `config.yaml` (defaulting to 2000 and 200, respectively)
**And** the original YAML frontmatter metadata (`id`, `title`, `url`, `scraped_at`) is successfully preserved and associated with each resulting document chunk

### Story 3.2: Vector Embedding & ChromaDB Storage

As a system administrator,
I want the document chunks to be converted to vector embeddings and stored locally in ChromaDB,
So that semantic search can be performed against the dataset locally.

**Acceptance Criteria:**

**Given** a list of split document chunks from Story 3.1
**When** the `ingestion/embedder.py` module processes the chunks
**Then** it uses `OllamaEmbeddings` configured to point to `localhost:11434` with the `nomic-embed-text` model
**And** the embeddings and associated metadata are stored in a local ChromaDB instance utilizing `PersistentClient` pointing to `data/vectordb/`
**And** running the ingestion process multiple times updates existing documents or skips duplicates rather than blindly duplicating the entire database

### Story 3.3: Ingestion CLI Orchestrator

As a system administrator,
I want a single command-line interface to orchestrate the entire ingestion pipeline,
So that I can easily update the vector database after a scraper run completes.

**Acceptance Criteria:**

**Given** the system administrator runs an ingestion script (e.g. `uv run python ingestion/main.py`)
**When** the pipeline executes
**Then** it orchestrates the full flow: load markdown → split text → generate embeddings → write to ChromaDB
**And** a `rich` console displays progress (e.g., "Loaded 2,457 files", "Generated 12,000 chunks", "Embedding vectors (ETA: 10m)...")
**And** when complete, it outputs a summary (total chunks embedded, DB size)

## Epic 4: RAG Chat Experience

A developer can open a browser, type a natural-language question about Intershop, and instantly receive an accurate, grounded answer with direct citations to the original Knowledge Base articles — all running 100% locally with conversation memory for follow-ups.

### Story 4.1: Vector Retrieval & Context Gathering

As a developer,
I want my natural language query to retrieve the most relevant Knowledge Base articles from the local vector database,
So that the LLM has accurate, proprietary context to answer my question.

**Acceptance Criteria:**

**Given** the local ChromaDB database is populated from Epic 3
**When** the `ui/chain.py` module receives a user query string
**Then** it uses a LangChain `Chroma` retriever with the local `OllamaEmbeddings` to fetch the top-k most relevant document chunks
**And** it extracts both the `.page_content` and the `.metadata` (specifically `title` and `url`) from the retrieved chunks
**And** it packages this context as a string to be injected into an LLM prompt
**And** if no relevant context can be found, the system explicitly returns a structured "No context found" indicator

### Story 4.2: Grounded Answer Generation (LCEL Chain)

As a developer,
I want the system to generate a technical answer strictly based on the retrieved Intershop documentation,
So that I don't receive hallucinated APIs or generic advice.

**Acceptance Criteria:**

**Given** the extracted context string from Story 4.1
**When** the LangChain LCEL chain executes
**Then** it passes the query and context to a `ChatOllama` model (configured for `qwen2.5:7b` on `localhost:11434`)
**And** a strict System Prompt enforces that the model MUST answer solely based on the provided context
**And** the generation response is returned as an iterable stream (for real-time typing UI)
**And** the chain output includes both the generated text and the list of raw retrieved LangChain `Document` objects (for citation rendering)

### Story 4.3: Conversational Memory Buffer

As a developer,
I want the system to remember my previous questions and its own answers during my session,
So that I can ask follow-up questions without repeating the full context.

**Acceptance Criteria:**

**Given** a developer is in an active chat session
**When** they ask a follow-up question (e.g., "Where can I find that file?")
**Then** the Streamlit `st.session_state` passes the previous turns (chat history) into the LangChain LCEL chain
**And** the LCEL chain uses a history-aware retriever prompt to rephrase the follow-up question into a standalone query before querying ChromaDB
**And** the final generation prompt includes the chat history along with the newly retrieved context

### Story 4.4: Basic Streamlit Chat UI

As a developer,
I want to interact with the RAG pipeline through a clean, browser-based chat interface,
So that I don't have to use a command-line terminal to query the knowledge base.

**Acceptance Criteria:**

**Given** the developer runs `uv run streamlit run ui/app.py`
**When** the browser opens to `localhost:8501`
**Then** a basic Streamlit interface renders with a fixed bottom `st.chat_input` text box
**And** the user can submit a query and see their message appear as an `st.chat_message("user")`
**And** the app calls the LCEL chain (from Story 4.2/4.3) and streams the output directly into an `st.chat_message("assistant")` using `st.write_stream`
**And** the UI successfully renders standard markdown and code block formatting returned by the LLM
**And** the conversation seamlessly persists on the screen as `st.session_state` memory grows

### Story 4.5: Raw Citation Display

As a developer,
I want the chat interface to explicitly list the source documents it used to generate the answer,
So that I can verify the information or read the full article context.

**Acceptance Criteria:**

**Given** the LCEL chain returns a generated response and the raw retrieved LangChain `Document` source objects
**When** the `st.chat_message("assistant")` finishes streaming the LLM text
**Then** the UI extracts the `url` and `title` metadata from the source objects
**And** it appends a raw text list of these sources to the bottom of the chat bubble (e.g., "Sources: Article 1 (URL), Article 2 (URL)")

## Epic 5: Chat UI Polish & Accessibility

Developers experience a professional, IDE-like chat interface with prominent citation footers, helpful empty states, clear error messages, keyboard-first interaction, and full accessibility compliance — building deep trust and flow-state productivity.

### Story 5.1: Theming & Typography Adjustments

As a generic user,
I want the chat interface to use a specific dark theme and legible fonts,
So that the application feels like a modern IDE and minimizes eye strain.

**Acceptance Criteria:**

**Given** the Streamlit app is running
**When** a user views the application
**Then** the UI strictly uses the Dark Mode palette (Background `#0E1117`, Primary Text `#FAFAFA`, Accent `#569CD6`) configured via `.streamlit/config.toml`
**And** system sans-serif fonts are applied to standard text, while monospace fonts are applied to code blocks
**And** text contrast ratios meet or exceed WCAG AA standards (4.5:1 minimum)

### Story 5.2: Enhanced Citation Footer Component

As a developer,
I want the raw source metadata from the LLM response to be beautifully formatted as a dedicated footer block,
So that I can easily scan and click the exact "proof" links verifying the AI's answer.

**Acceptance Criteria:**

**Given** the raw citation list output from Story 4.5
**When** the `ui/citations.py` helper function is called
**Then** it renders a visual markdown separator (`---`) at the bottom of the chat bubble
**And** it renders a bulleted list of citation links using sub-text styling (`font-size:0.8em; color:gray;`)
**And** the links are descriptive (e.g., using the `title` metadata rather than raw URLs)
**And** clicking a link opens the target in a new browser tab (`target="_blank"`)

### Story 5.3: Empty State & Conversation Reset

As a developer,
I want to see helpful system prompts when I first load the app, and I want an easy way to clear my session context,
So that I know exactly how to query the system and can avoid "context bleed" between different problems.

**Acceptance Criteria:**

**Given** a user opens the app (or clicks the "Clear History" button)
**When** the chat history is empty
**Then** a visually distinct Empty State component renders in the center of the screen
**And** it displays 2-3 clickable example prompts that auto-populate the input box when clicked
**And** a full-width "Clear Chat History" button exists persistently in the left `st.sidebar`
**And** clicking the "Clear History" button wipes `st.session_state` and triggers `st.rerun()`

### Story 5.4: Loading Feedback & Error Recovery States

As a developer,
I want clear feedback while the system is retrieving context or when an internal pipeline fails,
So that I'm never left wondering if the app froze or why I didn't get an answer.

**Acceptance Criteria:**

**Given** the user submits a query
**When** the LCEL chain is querying ChromaDB and initializing Ollama
**Then** an `st.spinner()` displays an accurate status message (e.g., "Querying Knowledge Base...")
**And** the spinner disappears exactly when the first LLM token streams
**And** if Ollama is unreachable (connection refused) or ChromaDB is missing, the system catches the error and renders a descriptive `st.error()` boundary explaining the failure and how to fix it

### Story 5.5: Form Interaction & Accessibility Refinements

As a developer,
I want the chat interface to lock while processing and automatically handle scrolling and focus,
So that my interaction is frictionless, keyboard-driven, and prevents double-submissions.

**Acceptance Criteria:**

**Given** the Streamlit frontend is rendering
**When** the user interacts with the app
**Then** the `st.chat_input` text box is disabled the moment a query is submitted, and only re-enabled after the final citation footer renders
**And** the UI automatically scrolls the viewport to the bottom as the LLM streams its response
**And** the chat input box auto-focuses on initial page load and after every generation cycle
**And** all interactive elements (buttons, links) can be navigated to via the `Tab` key
**And** wide UI elements (like code blocks) utilize horizontal scrolling (`overflow-x: auto`) rather than breaking the center max-width layout container
