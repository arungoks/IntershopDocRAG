---
title: "Product Brief Distillate: IntershopRAG"
type: llm-distillate
source: "product-brief-IntershopRAG.md"
created: "2026-03-28"
purpose: "Token-efficient context for downstream PRD creation and implementation"
---

# IntershopRAG — Detail Pack

## Technical Architecture Decisions (from brainstorming)
- **Language:** Python — richest scraping ecosystem
- **Auth:** Playwright headless → MS Entra ID OAuth 2.0 (tenant: `13a9f4be-a9d5-4987-bdf2-f31cc074034f`, client: `97ef1ba5-5545-4264-a1c0-52813528bc60`)
- **Auth flow:** 2-step MS login (email page → password page), followed by redirect to `knowledge.intershop.com/oauth.php`
- **Scraping:** Playwright for auth only → export cookies → httpx AsyncClient for all page fetches
- **Parser:** BeautifulSoup4 with CSS selector fallback chain (primary content div → `<article>` → `<main>` → `<body>`)
- **HTML→MD:** markdownify (preserves tables, actively maintained)
- **Concurrency:** asyncio with semaphore (3-5 concurrent workers)
- **Rate limiting:** Adaptive — start at 1s delay, back off on errors/429s, respect Retry-After headers
- **File naming:** `{page_id}.md` (e.g., `2C9117.md`) — unique, filesystem-safe, matches sitemap
- **Output:** Flat folder with YAML frontmatter per file
- **State:** JSON checkpoint file (`scrape_state.json`) for resume support
- **Progress:** `rich` console library for live progress + file logging
- **Config:** `config.yaml` for all configurable values
- **Phase 2 UI:** Streamlit web app for browser-based chat

## Key Technical Discoveries
- Login page at `knowledge.intershop.com/kb/index.php/Account?qdo=LogOn` redirects to `login.microsoftonline.com` (Microsoft Entra ID)
- OAuth uses PKCE (`code_challenge_method=S256`)
- `fKMSIEnabled: false` — no "Keep me signed in", sessions are time-bounded (~1 hour)
- Content pages have ~70% navigation chrome; only ~30% is article content
- Pages contain structured tables (Topic → Documentation mapping) that must be preserved
- Intershop is a German company — expect umlauts and multilingual content, enforce UTF-8

## Sitemap Facts
- File: `Intershop_sitemap.xml` (331KB)
- Total URLs: 2,457
- URL pattern: `https://knowledge.intershop.com/kb/index.php/Display/{ID}`
- Each URL has `lastmod` timestamp — use as metadata
- Dates range from 2025 to March 2026

## Resilience Patterns (from chaos engineering)
- **Auth failure recovery:** Detect redirect to `login.microsoftonline.com` in response → re-run Playwright login → get fresh cookies → resume
- **MFA detection:** If MFA screen appears, pause + alert user (not auto-recoverable)
- **Circuit breaker:** Stop after 10 consecutive failures — systemic issue likely
- **Content validation:** Check markdown length > 50 chars; flag empty/stub pages
- **Fallback selectors:** Multiple CSS selectors for different page templates
- **Deduplication:** SHA256 content hash to detect duplicate pages in sitemap
- **Encoding:** Force UTF-8 everywhere, handle UnicodeDecodeError with `errors='replace'`
- **URL handling:** Convert all relative URLs to absolute during conversion

## YAML Frontmatter Schema
```yaml
---
title: "Page Title"
url: "https://knowledge.intershop.com/kb/index.php/Display/{ID}"
page_id: "{ID}"
last_modified: "2026-03-23T11:17:31+01:00"  # from sitemap
scraped_at: "2026-03-28T12:35:00"
breadcrumb: ["Category", "Subcategory"]
word_count: 450
---
```

## Proposed Project Structure
```
IntershopRAG/
├── config.yaml
├── creds.txt                 # gitignored
├── Intershop_sitemap.xml
├── scraper/
│   ├── __init__.py
│   ├── main.py               # entry point
│   ├── auth.py               # Playwright OAuth login
│   ├── fetcher.py            # httpx async fetcher
│   ├── parser.py             # BS4 content extraction
│   ├── converter.py          # HTML → Markdown
│   ├── state.py              # JSON checkpoint
│   ├── config.py             # config loader
│   └── utils.py              # logging, rate limiting
├── output/pages/             # scraped markdown files
├── logs/
├── scrape_state.json
└── requirements.txt
```

## Scope Signals
- **In MVP:** Scraping pipeline only (sitemap-driven, authenticated, markdown output)
- **Out of MVP:** Embedding, ChromaDB, Ollama, chatbot UI
- **Future expansion:** User Manuals (`/oh/`) and Product Releases (`/prd/`) portals (same domain, same auth)
- **Phase 2 confirmed:** Streamlit web UI, not CLI

## Open Questions
- Exact CSS selector for main content div (needs one-time inspection of actual page HTML with dev tools)
- Whether any pages are JS-rendered (may need Playwright fallback for some pages)
- Optimal chunk size for RAG embeddings (Phase 2 concern)
- Which Ollama model to use (Phase 2 concern)
