---
stepsCompleted: [1, 2, 3, 4]
inputDocuments: ['Intershop_sitemap.xml', 'creds.txt']
session_topic: 'Intershop Knowledge Base Web Scraping Pipeline for RAG Chatbot'
session_goals: 'Design a robust authenticated web scraper that converts ~2,457 Intershop KB pages to individual markdown files with metadata'
selected_approach: 'ai-recommended'
techniques_used: ['constraint-mapping', 'morphological-analysis', 'chaos-engineering']
ideas_generated: 29
session_active: false
workflow_completed: true
---

## Session Overview

**Topic:** Intershop Knowledge Base Web Scraping Pipeline for RAG Chatbot
**Goals:** Design a robust authenticated web scraper that converts ~2,457 Intershop KB pages to individual markdown files with embedded metadata. This is the MVP — embedding and RAG pipeline are future phases.

### Context

- **Source:** `knowledge.intershop.com` — wiki/knowledge-base CMS with Microsoft Entra ID authentication
- **Scale:** ~2,457 pages identified via sitemap XML
- **URL pattern:** `https://knowledge.intershop.com/kb/index.php/Display/{ID}`
- **Auth:** Microsoft Entra ID OAuth 2.0 with PKCE (email/password login via `login.microsoftonline.com`)
- **Output:** Individual markdown files per page with YAML frontmatter metadata
- **Stack:** Fully local — Ollama for LLM, ChromaDB for vector store (future phases)

---

## Technique Selection

**Approach:** AI-Recommended Techniques
**Techniques:** Constraint Mapping → Morphological Analysis → Chaos Engineering

---

## Technique Execution Results

### Phase 1: Constraint Mapping (5 ideas)

**Key Discovery:** Authentication is NOT simple form login — it's Microsoft Entra ID OAuth 2.0 with PKCE, requiring browser automation.

| ID | Idea | Category |
|----|------|----------|
| Auth #1 | Browser Automation for OAuth Login (Playwright) | Auth |
| Auth #2 | Session Cookie Harvesting (Playwright → httpx) | Auth |
| Auth #3 | Token Refresh Resilience (watchdog for 401s) | Auth |
| Auth #4 | Playwright Headless MS Entra Flow (2-step email→password) | Auth |
| Auth #5 | Proactive Re-auth (schedule-based, not failure-based) | Auth |

**Key Discovery:** Content pages have heavy navigation chrome (~70% noise). Main article content must be CSS-selector-targeted.

| ID | Idea | Category |
|----|------|----------|
| Content #1 | Navigation Chrome Pollution (strip header/nav/footer) | Content |
| Content #2 | CSS Selector-Based Content Extraction | Content |
| Content #3 | Rich Metadata from Page Structure (title, URL, page ID, lastmod, breadcrumbs) | Content |
| Content #4 | Table-Heavy Content Preservation | Content |
| Content #5 | Lock-Icon Gated Content Detection | Content |

| ID | Idea | Category |
|----|------|----------|
| Scale #1 | Polite Crawling with Rate Limiting | Scale |
| Scale #2 | Checkpoint/Resume System (JSON state file) | Scale |
| Scale #3 | Batch Processing with Progress Reporting | Scale |
| Scale #4 | Concurrent Scraping with Connection Pool (3-5 workers) | Scale |

### Phase 2: Morphological Analysis (5 ideas)

**Architecture Decisions Matrix:**

| Parameter | Decision | Rationale |
|-----------|----------|-----------|
| Language | Python | Richest scraping ecosystem |
| Auth Method | Playwright headless | Handles MS Entra OAuth flow |
| Scraping Engine | Playwright auth → httpx async | Browser for login, HTTP for speed |
| HTML Parser | BeautifulSoup4 | Forgiving with messy HTML |
| HTML→Markdown | markdownify | Preserves tables, actively maintained |
| Content Selector | CSS selector with fallback chain | Cleanest extraction |
| Concurrency | Async semaphore (3-5) | Fast but polite |
| Rate Limiting | Adaptive | Self-tuning based on server response |
| State/Resume | JSON file | Simple, human-readable |
| File Naming | Page ID (e.g., `2C9117.md`) | Unique, filesystem-safe |
| Output Structure | Flat folder + manifest | Simple with organization index |
| Metadata | YAML frontmatter | Self-contained, RAG-standard |
| Error Handling | Retry 3x with exponential backoff | Resilient without infinite loops |
| Progress | `rich` console | Beautiful live progress |
| Config | config.yaml | Readable, versionable |

| ID | Idea | Description |
|----|------|-------------|
| Morph #1 | Hybrid Engine Architecture | Playwright auth → httpx async scraping |
| Morph #2 | Self-Contained Markdown with YAML Frontmatter | Each file has complete metadata |
| Morph #3 | Checkpoint-Resume with JSON State | Resumable, inspectable state file |
| Morph #4 | Adaptive Rate Limiter | Self-tuning request throttling |
| Morph #5 | Content Extraction Pipeline | 4-step modular pipeline (fetch → parse → clean → convert) |

### Phase 3: Chaos Engineering (15 ideas)

| ID | Attack Scenario | Survival Strategy |
|----|----------------|-------------------|
| Chaos #1 | MS login page layout changes | Multiple fallback selectors |
| Chaos #2 | MFA enabled mid-scrape | Detect MFA prompt, pause + alert |
| Chaos #3 | Session dies at page 2,000 | Response content validation + re-auth |
| Chaos #4 | Empty content pages | Min-length check, flag as stub |
| Chaos #5 | Different HTML templates | Fallback selector chain (4 levels) |
| Chaos #6 | JS-rendered content | Detect via httpx vs Playwright comparison |
| Chaos #7 | Access-denied pages | Distinguish auth failure vs permission |
| Chaos #8 | Network drops mid-batch | Exponential backoff + auto-resume |
| Chaos #9 | Disk full mid-scrape | Pre-flight space check |
| Chaos #10 | 429 Too Many Requests | Respect Retry-After header |
| Chaos #11 | Duplicate pages in sitemap | SHA256 content dedup |
| Chaos #12 | Unicode/encoding issues | Force UTF-8 everywhere |
| Chaos #13 | Relative links/images | Convert to absolute URLs |
| Chaos #14 | Circuit Breaker pattern | Stop after 10 consecutive failures |
| Chaos #15 | Comprehensive logging | 3-level: file log + console + state |

---

## Idea Organization and Prioritization

### Theme 1: Authentication & Session Management
_Focus: Getting and staying logged in across 2,457 pages_

- **Playwright headless OAuth flow** — core auth mechanism
- **Cookie harvesting to httpx** — decouples auth from scraping speed
- **Proactive re-auth** — prevents mid-scrape session death
- **MFA detection** — graceful handling of unexpected auth changes

### Theme 2: Content Extraction Quality
_Focus: Getting clean, useful markdown from messy HTML_

- **CSS selector targeting** — extract main content only
- **Fallback selector chain** — handle multiple page templates
- **Table preservation** — maintain structured data relationships
- **Absolute URL conversion** — self-documenting output
- **UTF-8 enforcement** — handle German/multilingual content

### Theme 3: Resilience & Error Handling
_Focus: Making the scraper survive anything_

- **Retry with exponential backoff** — handle transient failures
- **Circuit breaker** — fail fast on systemic issues
- **Checkpoint/resume** — never lose progress
- **Adaptive rate limiting** — self-tuning politeness
- **Content validation** — detect empty/auth-failed/access-denied pages

### Theme 4: Output & Metadata Design
_Focus: Producing RAG-ready output files_

- **YAML frontmatter** — title, URL, page_id, last_modified, scraped_at, breadcrumb, word_count
- **Page ID filenames** — unique, filesystem-safe, matches sitemap
- **Flat folder + manifest** — simple structure with organization index
- **Content deduplication** — SHA256 hash to detect duplicates
- **Post-scrape report** — summary of what was scraped and what needs attention

---

## Action Plan: Implementation Blueprint

### Project Structure

```
IntershopRAG/
├── config.yaml              # Scraper configuration
├── creds.txt                # Login credentials (gitignored)
├── Intershop_sitemap.xml    # Source sitemap
├── scraper/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── auth.py              # Playwright OAuth login + cookie export
│   ├── fetcher.py           # httpx async page fetcher
│   ├── parser.py            # BS4 content extraction
│   ├── converter.py         # HTML → Markdown conversion
│   ├── state.py             # JSON checkpoint manager
│   ├── config.py            # Config loader
│   └── utils.py             # Logging, rate limiting, helpers
├── output/
│   └── pages/               # Scraped markdown files
├── logs/
│   └── scrape.log
├── scrape_state.json        # Resume state
└── requirements.txt
```

### Implementation Steps

**Step 1: Project Setup** (15 min)
- Create project structure
- Create `requirements.txt`: playwright, httpx, beautifulsoup4, markdownify, rich, pyyaml, lxml
- Create `config.yaml` with all configurable values
- Install dependencies, install Playwright browsers

**Step 2: Auth Module** (30 min)
- Build `auth.py`: Playwright headless → navigate to login URL → handle MS Entra 2-step flow → export cookies
- Test with a single page fetch to verify cookies work

**Step 3: Sitemap Parser** (15 min)
- Parse `Intershop_sitemap.xml` → extract all URLs + lastmod dates
- Build URL queue with metadata

**Step 4: Content Extraction Pipeline** (45 min)
- Build `fetcher.py`: httpx async client with cookie injection
- Build `parser.py`: BS4 content selector with fallback chain
- Build `converter.py`: markdownify with YAML frontmatter generation

**Step 5: State Management** (20 min)
- Build `state.py`: JSON checkpoint load/save/update
- Resume logic: skip completed, retry failed

**Step 6: Orchestrator** (30 min)
- Build `main.py`: tie everything together
- Async semaphore concurrency (3-5 workers)
- Adaptive rate limiting
- Circuit breaker (10 consecutive failures = stop)
- Rich progress bar + logging

**Step 7: Testing & Tuning** (30 min)
- Test with 10 pages first
- Verify markdown output quality
- Tune CSS selectors based on real page variants
- Adjust concurrency/rate limits

### Timeline Estimate
- **Total development:** ~3 hours
- **Full scrape run:** ~30-60 minutes (2,457 pages at 3-5 concurrent)

---

## Session Summary

**29 ideas** generated across 3 techniques in ~15 minutes of focused brainstorming.

### Key Breakthroughs
1. **Auth is OAuth, not form login** — discovered by inspecting the actual login page, completely changed the architecture
2. **Hybrid engine** — Playwright for auth only, httpx for speed — best of both worlds
3. **Content is 70% noise** — CSS selector targeting is essential, not optional
4. **Intershop is German** — UTF-8 and multilingual handling is critical

### Creative Facilitation Narrative
The session started with what seemed like a straightforward scraping challenge but quickly revealed deep complexity through constraint mapping. The discovery that authentication uses Microsoft Entra ID OAuth 2.0 (not simple form login) was a pivotal moment that reshaped the entire architecture. Morphological analysis then systematically explored 15 design parameters to arrive at optimal combinations. Chaos engineering stress-tested the design against 15 failure scenarios, producing a resilient, self-healing scraper architecture.
