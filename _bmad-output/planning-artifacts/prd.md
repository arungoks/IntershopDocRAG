stepsCompleted: 
  - 'step-01-init'
  - 'step-02-discovery'
  - 'step-02b-vision'
  - 'step-02c-executive-summary'
  - 'step-03-success'
  - 'step-04-journeys'
  - 'step-05-domain'
  - 'step-06-innovation'
  - 'step-07-project-type'
  - 'step-08-scoping'
  - 'step-09-functional'
  - 'step-10-nonfunctional'
  - 'step-11-polish'
classification:
  projectType: developer_tool
  domain: general
  complexity: low
  projectContext: greenfield
inputDocuments: 
  - 'c:\Users\Arun\Documents\Projects\IntershopRAG\_bmad-output\planning-artifacts\product-brief-IntershopRAG.md'
  - 'c:\Users\Arun\Documents\Projects\IntershopRAG\_bmad-output\planning-artifacts\product-brief-IntershopRAG-distillate.md'
  - 'c:\Users\Arun\Documents\Projects\IntershopRAG\_bmad-output\brainstorming\brainstorming-session-2026-03-28-1228.md'
workflowType: 'prd'
briefCount: 2
researchCount: 0
brainstormingCount: 1
projectDocsCount: 0
---

# Product Requirements Document - IntershopRAG

**Author:** Arun
**Date:** 2026-03-28

## Executive Summary

IntershopRAG is a fully local, AI-powered developer assistant designed to eliminate the authentication and search friction of accessing the Intershop Commerce Platform documentation. By converting all 2,457 pages of the Microsoft Entra ID-gated Knowledge Base (`knowledge.intershop.com`) into a structured, searchable markdown repository, and subsequently feeding it into a local ChromaDB/Ollama RAG pipeline, the system provides developers with instant, natural-language answers to complex technical questions. It transforms the current high-friction "context-switch, login, search, scan" workflow into an immediate, self-serve Q&A experience directly grounded in official documentation.

### What Makes This Special

Unlike general-purpose LLMs that frequently hallucinate technical API details, IntershopRAG strictly retrieves answers from verified, official source documents, maintaining complete traceability with direct source citations. By operating completely offline and on-premises, the system incurs zero recurring API costs and guarantees that proprietary engineering queries never leak to external vendors. The solution bypasses the slow, token-expiring web interface entirely, drastically improving developer "flow state" and new-hire onboarding velocity.

## Project Classification

- **Project Type:** Internal Developer Tool (Web Scraper & AI Chatbot Pipeline)
- **Domain:** Software Engineering / Technical Documentation
- **Complexity:** Low Regulatory Complexity, Medium Technical Execution (Playwright Auth + Local RAG)
- **Project Context:** Greenfield

## Success Criteria

### User Success
- **Faster Answers:** Developers receive accurate responses within 5 seconds for typical queries.
- **Workflow Adoption:** Over 80% of the development team prefers using the IntershopRAG chatbot over browsing `knowledge.intershop.com` directly for routine technical lookups.
- **Trust in Results:** Users can verify every answer immediately because 100% of responses include direct citations/links to the source documentation.

### Business Success
- **Time Reclaimed:** Significant reduction in engineering hours lost to context-switching, logging into the MS Entra ID portal, and searching for documentation.
- **Onboarding Velocity:** New hires reach productivity faster by self-serving technical queries through the AI.

### Technical Success
- **100% Documentation Coverage:** All 2,457 Knowledge Base articles in the sitemap are successfully scraped.
- **Format Integrity:** Scraped markdown files perfectly preserve complex tables, code snippets, hyperlinks, and structural hierarchy.
- **Pipeline Resilience:** The scraper completes its full run autonomously, successfully handling Microsoft Entra ID token expirations and network errors without manual intervention.
- **RAG Accuracy:** The local LLM cites the correct source document ≥90% of the time without hallucination.

## Product Scope

### MVP - Minimum Viable Product (Phase 1)
- Playwright-driven Microsoft Entra ID OAuth login to extract session cookies.
- Async HTTP scraper fetching all 2,457 pages from the sitemap.
- HTML-to-Markdown conversion with structure preservation and YAML frontmatter (metadata).
- State management for resuming interrupted scrapes and avoiding duplicate work.

### Growth Features (Phase 2)
- Markdown chunking strategy and ChromeDB local vector store population.
- Local LLM integration (Ollama).
- A simple, browser-based Streamlit Chat UI for developers to interact with the RAG system.

### Vision (Future)
- **Broader Content Parsing:** Expand scraping beyond the primary sitemap to include User Manuals (`/oh/`) and Product Releases (`/prd/`).
- **Unified Knowledge Source:** Integrate GitHub PRs, Jira tickets, and internal runbooks into the same RAG pipeline.
- **IDE Integration:** Deliver the context directly into the developer's IDE (e.g., VS Code extension).

## User Journeys

### 1. Sarah, Senior Backend Developer (Primary User - Success Path)
- **Situation:** Sarah is deep into a coding sprint, building a custom REST API integration. She suddenly hits an obscure `400 Bad Request` error from the Intershop platform that she's never seen before.
- **The Obstacle:** Normally, she would have to break her flow state, open her browser, go to `knowledge.intershop.com`, wait through the Microsoft Entra ID multi-step login redirect dance, and then fight the Knowledge Base's built-in search to find the correct API reference.
- **The Solution:** Instead, she opens the IntershopRAG Streamlit UI and pastes her error message. Within 3 seconds, the LLM retrieves the exact documentation page, summarizes the fix, and importantly, provides a direct citation link for verification.
- **Resolution:** Sarah fixes her code immediately. Her emotional transition goes from *frustrated interaction* to *relieved productivity*. She never had to leave her workflow context.

### 2. Arun, Junior Engineer Onboarding (Exploration Path)
- **Situation:** Arun just joined the team and is completely overwhelmed by Intershop's proprietary terminology. He doesn't understand the difference between the ICM (Intershop Commerce Management) and IOM (Intershop Order Management) modules.
- **The Obstacle:** In the standard Knowledge Base, searching for "ICM vs IOM" returns hundreds of disjointed, highly technical articles with no beginner-friendly, high-level summary.
- **The Solution:** Arun asks the chatbot, "Can you explain how ICM and IOM interact using simple terms?" The RAG pipeline intelligently synthesizes context from 5 different high-level architectural markdown files, presenting a cohesive, unified answer. Arun asks a follow-up question ("Which one handles payment routing?"), and the UI retains his session history to answer perfectly.
- **Resolution:** Arun avoids tapping a senior developer on the shoulder for the 5th time today. He goes from feeling *lost* to *capable and confident*.

### 3. Marcus, DevOps / System Admin (Operations Path)
- **Situation:** Intershop releases a platform update, meaning the company's local RAG vector database contains stale documentation.
- **The Obstacle:** Marcus needs to update the 2,400+ markdown files. The Microsoft Entra ID login makes standard automated scraping impossible because it requires executing a complex OAuth flow.
- **The Solution:** Marcus simply runs the Python scraping pipeline `main.py`. A headless Playwright browser spins up, automatically handles the Microsoft Entra ID 2-step login using an admin service account (pulling from `creds.txt`), harvests the valid auth cookies, and passes them to an async HTTP engine. The pipeline automatically skips unmodified pages and only scrapes/updates the new markdown files.
- **Resolution:** A task that could have been a major authentication headache runs silently and autonomously in minutes.

### Journey Requirements Summary

These narrative journeys reveal the following concrete technical capabilities needed for the system:

- **Auth Automation (Operations):** The scraper must be able to autonomously orchestrate a Microsoft Entra ID login flow without human UI interaction.
- **Citation Traceability (Primary User):** The LLM prompt architecture must force the model to append explicit source references to every answer to maintain developer trust.
- **Conversation Memory (Exploration User):** The Streamlit UI must preserve chat history per session so users can ask follow-up queries contextually.
- **Differential Scraping (Operations):** The pipeline needs state management to understand which pages have already been successfully converted to markdown so it doesn't blindly re-download 2,457 pages every run.

## Developer Tool Specific Requirements

### Project-Type Overview
IntershopRAG is an internal developer tool consisting of two primary components: an automated, Playwright-driven Python data extraction pipeline, and an interactive RAG application framework running completely locally.

### Technical Architecture Considerations
- **Core Language:** Python 3.10+ (selected for the richest ecosystem of scraping and AI tooling).
- **Authentication Bridge:** Playwright (headless) must be used specifically to navigate the Microsoft Entra ID OAuth 2.0 PKCE flow and harvest session cookies. 
- **Scraping Engine:** `httpx.AsyncClient` for high-throughput concurrency (3-5 workers), parsed via `BeautifulSoup4`, and converted to clean markup via `markdownify`.
- **State Management:** JSON checkpointing (`scrape_state.json`) is required to allow the pipeline to resume without re-authenticating or re-scraping the full 2,457 page sitemap if interrupted.
- **AI Stack:** ChromaDB (for local vector persistence) and Ollama (for local LLM execution, ensuring zero data leakage).

### Installation & Environment Setup
- The tool must run locally on developer workstations (optimizing for Windows).
- Dependencies will be managed via standard `requirements.txt`.
- Credentials (`creds.txt` containing the MS Entra ID username/password) must be strictly `.gitignore`'d and loaded dynamically at runtime.

### Pipeline Interfaces (CLI Usage)
The primary interface for Phase 1 operations is a CLI pipeline executed by a dev/admin:
- The pipeline initiates `main.py`, orchestrating the auth, fetch, and convert modules.
- It must present real-time console progress (e.g., using the `rich` library) to provide visibility into the async queue of 2,400+ requests.

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

**MVP Approach:** The "Extraction First" MVP. Our immediate goal is to prove we can reliably breach the Microsoft Entra ID authentication wall and establish a pristine local repository of the Intershop Knowledge Base. Only after the extraction pipeline is battle-tested will we move to the AI / RAG implementation.
**Resource Requirements:** 1-2 Backend/Data Engineers for Phase 1 (Python, Playwright, HTTPx), transitioning to LLM integration for Phase 2.

### MVP Feature Set (Phase 1)
**Core User Journeys Supported:**
- Marcus, DevOps / System Admin (Operations Path) - updating the knowledge base autonomously.

**Must-Have Capabilities:**
- Headless Playwright integration for automated MS Entra ID OAuth login.
- Asynchronous HTTP fetching engine with built-in rate-limiting and auto-retries.
- Intelligent HTML-to-Markdown parser utilizing BeautifulSoup4 and markdownify.
- Local JSON checkpointing (`scrape_state.json`) to skip already-downloaded pages and resume interrupted operations.

### Post-MVP Features

**Phase 2 (Growth - RAG Application):**
- Local ChromaDB vector embedding of all 2,457 markdown files.
- Ollama local inference integration.
- Streamlit browser-based Chat UI for the development team.
- Built-in source citation linking.

**Phase 3 (Expansion - System Evolution):**
- Unified Knowledge: Incorporating Jira tickets, User Manuals (`/oh/`), and Product Releases (`/prd/`) into the same vector space.
- Developer Workflow: Direct VS Code IDE extension to surface docs interactively while coding.

### Risk Mitigation Strategy

**Technical Risks:** Microsoft Entra ID may update its login UI or flow over time, potentially breaking the headless Playwright script.
- *Mitigation Approach:* Isolate the Playwright logic completely in an independent `auth.py` file with easily configurable CSS selectors. The scraping engine (`fetcher.py`) will remain totally agnostic to the auth flow, only requiring valid cookies.

**Market Risks:** Developers may resist adopting the chatbot tool due to habit, preferring the slow but familiar `knowledge.intershop.com` browser experience.
- *Validation Approach:* The new UI must be measurably faster. Crucially, the LLM must provide direct citation links to the original KB articles so developers can instantly verify answers without a loss of trust.

**Resource Risks:** Building the full RAG pipeline (Phase 2) might take longer than anticipated for a small team.
- *Contingency Approach:* By strictly bounding the MVP to the Scraping Pipeline (Phase 1), the team still massively benefits from producing a fully local, searchable markdown archive of all documentation, even before the AI chatbot is deployed.

## Functional Requirements

### Authentication & Session Management
- **FR1:** The system can programmatically authenticate through a Microsoft Entra ID portal.
- **FR2:** The system can extract and persist valid authentication session cookies.
- **FR3:** The system can detect expired or invalid auth states and re-authenticate autonomously without human intervention.

### Pipeline Orchestration & Lifecycle
- **FR4:** The system administrator can initiate the extraction pipeline via a command-line interface.
- **FR5:** The system can read a target sitemap XML to generate a comprehensive queue of target URLs.
- **FR6:** The system can output real-time processing progress and error logs to the administrator during execution.
- **FR7:** The system can gracefully shut down operations when complete or critically interrupted.

### Fetching & State Tracking
- **FR8:** The system can download multiple web payloads concurrently (asynchronously).
- **FR9:** The system can throttle its own request rate to respond gracefully to target server limits or timeouts.
- **FR10:** The system can record the exact success/failure status of every individual URL processed.
- **FR11:** The system can use persisted state records to skip already-downloaded pages on subsequent runs (Differential Sync).

### Content Parsing & Output Generation
- **FR12:** The system can convert raw scraped HTML into structured Markdown files locally.
- **FR13:** The system can preserve critical semantic elements during conversion, specifically tables, code blocks, and hyperlinks.
- **FR14:** The system can inject standardized metadata (original URL, scrape timestamp, title) into the YAML frontmatter of every generated Markdown file.

### RAG Chat Experience (Phase 2 Growth Scope)
- **FR15:** The developer can interact with the system via natural language queries in a browser environment.
- **FR16:** The system can retrieve local, proprietary domain knowledge matching the query intent.
- **FR17:** The system can generate technical answers grounded solely in the retrieved context.
- **FR18:** The system can surface direct, clickable citations to the exact original KB article corresponding to its answer.
- **FR19:** The system can maintain a conversational memory buffer during a user's active session to handle follow-up queries.

## Non-Functional Requirements

### Performance
- **NFR-P1:** The Phase 2 RAG chat interface must return an generated answer and citations to a user query within 5 seconds on average developer hardware.
- **NFR-P2:** The Phase 1 extraction pipeline must process multiple web pages concurrently (e.g., 3-5 workers) while automatically respecting implicit connection limits to prevent DDoSing the internal Knowledge Base.

### Security & Privacy
- **NFR-S1:** All Microsoft Entra ID login credentials must be read from local environment files (`creds.txt`) that are strictly excluded from version control.
- **NFR-S2:** The LLM integration (Phase 2) must execute 100% locally via Ollama; proprietary Intershop documentation must never be transmitted to external, cloud-hosted AI APIs (e.g., OpenAI, Anthropic) for generation or embedding.

### Reliability & Resilience
- **NFR-R1:** The asynchronous fetching engine must automatically retry failed HTTP requests up to 3 times with exponential backoff before marking a target URL as permanently failed.
- **NFR-R2:** If the Playwright session cookie expires mid-scrape, the system must pause HTTP requests, automatically re-trigger the headless login flow, and seamlessly resume fetching without losing queue state.
