---
title: "Product Brief: IntershopRAG"
status: "complete"
created: "2026-03-28"
updated: "2026-03-28"
inputs:
  - "brainstorming-session-2026-03-28-1228.md"
  - "Intershop_sitemap.xml"
  - "creds.txt"
---

# Product Brief: IntershopRAG

## Executive Summary

The Intershop Knowledge Base contains 2,457 articles covering every aspect of the Intershop Commerce Platform — from API references to deployment guides to troubleshooting articles. Today, accessing this knowledge requires navigating a slow, login-gated website that frustrates developers and breaks their flow. Every lookup is a context switch.

**IntershopRAG** is a fully local, AI-powered chatbot that puts the entire Intershop Knowledge Base at the development team's fingertips. Developers ask questions in natural language and get instant, accurate answers grounded in official documentation — with source citations. No browser, no login, no waiting.

The system runs entirely on-premises: scraped documentation stored as markdown, embedded in ChromaDB, served through a local LLM via Ollama. No data leaves the organization. No API costs. No vendor lock-in.

## The Problem

Developers working with the Intershop Commerce Platform face a recurring friction: finding answers in the official documentation is slow and painful.

- **Login wall:** The Knowledge Base at `knowledge.intershop.com` requires Microsoft Entra ID authentication. Getting access takes time, and every session starts with a redirect-heavy OAuth login flow.
- **Search friction:** Once inside, finding the right article among 2,457 pages requires knowing the right keywords. The KB's built-in search returns results, but developers must open, scan, and cross-reference multiple articles to find what they need.
- **Context switching:** Every documentation lookup pulls a developer out of their IDE, into a browser, through a login flow, and into a search-click-read-repeat loop. This breaks concentration and reduces productive coding time.
- **Onboarding burden:** New team members rely heavily on senior developers to interpret Intershop documentation. There is no self-service way to ask "how does X work in Intershop?" and get a synthesized answer.

The result: developers spend more time searching for information than applying it.

## The Solution

IntershopRAG solves this in two phases:

**Phase 1 (MVP): Knowledge Extraction Pipeline**
A Python-based scraping pipeline that authenticates into the Intershop Knowledge Base via Playwright (handling the Microsoft Entra ID OAuth flow), scrapes all 2,457 pages using async HTTP requests, and converts each page into a clean markdown file with YAML metadata (title, URL, page ID, last modified date, breadcrumb path). The result is a complete, local, offline copy of the entire Knowledge Base — structured and ready for AI consumption.

**Phase 2: RAG Chatbot**
The scraped markdown files are chunked, embedded into ChromaDB, and connected to a local LLM via Ollama. A chat interface allows developers to ask questions in natural language and receive accurate, citation-backed answers drawn from the official documentation.

## What Makes This Different

- **Fully local:** No data sent to cloud APIs. No OpenAI, no Anthropic, no vendor dependency. The entire stack — LLM, vector database, documents — lives on your infrastructure.
- **Grounded in official docs:** Unlike a general-purpose LLM that might hallucinate Intershop answers, IntershopRAG retrieves its answers exclusively from the verified, official Knowledge Base. Every response can cite its source.
- **Instant access:** No login, no browser, no search UI. Ask a question, get an answer. Seconds, not minutes.
- **Always up-to-date:** The scraping pipeline can be re-run to pull the latest documentation, keeping the local knowledge base current.
- **Zero recurring cost:** After initial setup, there are no API fees or subscription costs. Ollama runs locally, ChromaDB is open-source, and the scraped data is yours.

## Who This Serves

**Primary: Intershop Development Team**
Developers working with the Intershop Commerce Platform (ICM, PWA, IOM, SPARQUE.AI, DevOps). They need quick answers about APIs, configuration, deployment, and troubleshooting — and they need them without leaving their workflow.

**Secondary: New Team Members**
Engineers onboarding to Intershop projects who need to rapidly build understanding of the platform's architecture, concepts, and best practices without constantly asking senior developers.

## Success Criteria

| Metric | Target |
|--------|--------|
| **Knowledge Base Coverage** | 100% of the 2,457 KB pages in the sitemap successfully scraped and stored as clean markdown |
| **Content Quality** | Scraped markdown preserves tables, code blocks, links, and structural hierarchy |
| **Scraper Resilience** | Full scrape completes without manual intervention (auto re-auth, error recovery) |
| **Answer Accuracy** (Phase 2) | RAG responses cite correct source documents ≥90% of the time |
| **Response Time** (Phase 2) | Chatbot responds within 5 seconds for typical queries |
| **Developer Adoption** (Phase 2) | Team members prefer chatbot over direct KB browsing for routine questions |

## Scope

### Phase 1 — MVP (In Scope)
- Sitemap-driven URL extraction (2,457 pages)
- Automated MS Entra ID login via Playwright (headless)
- Async HTTP scraping with cookie-based authentication
- HTML → Markdown conversion with metadata (YAML frontmatter)
- Checkpoint/resume for interrupted scrapes
- Error handling, retry logic, and progress reporting

### Phase 2 — RAG Chatbot (Future)
- Markdown chunking strategy for embeddings
- ChromaDB local vector store setup
- Ollama LLM integration
- Streamlit web UI for browser-based chat interface
- Source citation in responses

### Out of Scope
- Real-time sync with the Knowledge Base (batch re-scrape only)
- Multi-user access control
- Cloud deployment
- Scraping beyond the sitemap XML (User Manuals, Product Releases portals — future expansion)

## Vision

If IntershopRAG succeeds, it becomes the default way the development team interacts with Intershop documentation — a knowledgeable AI teammate that has read every article and can synthesize answers across multiple sources instantly.

In 2-3 years, this could evolve into:
- **Multi-source RAG:** Incorporating Intershop GitHub repos, Jira tickets, internal runbooks, and Slack threads alongside the KB
- **IDE integration:** A VS Code extension that surfaces relevant Intershop documentation contextually as developers write code
- **Automated knowledge updates:** Scheduled re-scrapes triggered by sitemap changes, with incremental embedding updates
- **Team-wide deployment:** A shared service accessible to the entire engineering organization, not just one developer's machine
