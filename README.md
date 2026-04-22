# IntershopDocRAG

A robust, local-first RAG (Retrieval-Augmented Generation) chatbot designed to answer technical queries about the Intershop platform by leveraging local documentation.

## 🚀 Overview

IntershopDocRAG automates the process of extracting proprietary knowledge from the Intershop Knowledge Base, processing it into a searchable vector database, and providing a modern chat interface for developers to interact with the documentation—all while maintaining 100% data privacy through local execution.

## ✨ Key Features

- **Authenticated Scraper**: Automated Microsoft Entra ID authentication using headless Playwright to bypass SSO gateways.
- **Async Extraction Pipeline**: High-performance asynchronous fetching with rate-limiting and automatic re-authentication.
- **Semantic Parsing**: HTML-to-Markdown conversion using `trafilatura` to preserve tables, code blocks, and metadata.
- **Local RAG Integration**: Powered by LangChain, local Ollama models (`qwen2.5:3b`), and ChromaDB for privacy-preserving retrieval.
- **IDE-Like UI**: A sleek Streamlit-based chat interface with dark mode, conversational memory, and direct verifiable citations.

## 🛠️ Tech Stack

- **Package Manager**: [Astral `uv`](https://github.com/astral-sh/uv)
- **Scraping**: `httpx`, `Playwright`, `trafilatura`
- **AI/RAG**: `LangChain`, `ChromaDB`, `Ollama`
- **UI**: `Streamlit`, `rich`
- **Models**: `qwen2.5:3b` (Generation), `nomic-embed-text` (Embeddings)

## 🏗️ Architecture

The application follows a strictly decoupled, modular architecture to ensure separation of concerns between data acquisition, vectorization, and the user interface.

### 1. Data Acquisition (`scraper/`)
A resilient web scraping pipeline designed to bypass SSO protections using Microsoft Entra ID authentication via headless Playwright. It employs an asynchronous worker pool (`httpx` + `asyncio`) with built-in rate-limiting, exponential backoff, and automatic cookie-refresh mechanisms. Extracted HTML is semantically parsed into clean Markdown using `trafilatura` to preserve tables, code blocks, and metadata, and stored locally in `data/raw_md/`.

### 2. Knowledge Ingestion (`ingestion/`)
This module is responsible for building the Knowledge Base index. It uses LangChain's `RecursiveCharacterTextSplitter` to intelligently chunk the raw Markdown files with overlap, preventing context loss. The chunks are then passed through `nomic-embed-text` (running locally via Ollama) to generate vector embeddings. These embeddings are persisted to a local `ChromaDB` instance (`data/vectordb/`), forming the searchable vector space.

### 3. Conversational RAG & UI (`ui/`)
The interactive layer is built with **Streamlit** and relies on a two-phase LangChain Expression Language (LCEL) architecture:
- **History-Aware Retrieval:** When a user asks a question, the system uses the conversation history to rephrase the query into a standalone search term, ensuring contextual continuity.
- **Grounded Generation:** The rephrased query fetches the most relevant context chunks from ChromaDB. The local `qwen2.5:3b` LLM then synthesizes an answer using *only* the provided context.
- **Citations:** Every streamed response includes a dedicated footer with verifiable, deduplicated source links mapping directly back to the original Intershop documentation.

Data flows sequentially: `Knowledge Base` ➔ `scraper/` ➔ `data/raw_md/` ➔ `ingestion/` ➔ `data/vectordb/` ➔ `ui/`.

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/) installed and running locally.
- A `creds.txt` file in the root with your MS Entra ID credentials (Line 1: Username, Line 2: Password).

### Installation
1.  Clone the repository.
2.  Install dependencies and sync environment:
    ```bash
    uv sync
    ```
3.  Install browsers for Playwright:
    ```bash
    uv run playwright install chromium
    ```
4.  Pull required models in Ollama:
    ```bash
    ollama run qwen2.5:3b
    ollama pull nomic-embed-text
    ```

## 🏃 Running the Application

### 1. Scrape the Knowledge Base
```bash
uv run python scraper/main.py
```

### 2. Run the Ingestion Pipeline
```bash
uv run python ingestion/main.py
```

### 3. Launch the Chat UI
```bash
uv run streamlit run ui/app.py
```

## 📝 License
Proprietary / Internal Use.

---
*Built with ❤️ for Intershop developers.*
