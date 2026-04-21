# IntershopDocRAG

A robust, local-first RAG (Retrieval-Augmented Generation) chatbot designed to answer technical queries about the Intershop platform by leveraging local documentation.

## 🚀 Overview

IntershopDocRAG automates the process of extracting proprietary knowledge from the Intershop Knowledge Base, processing it into a searchable vector database, and providing a modern chat interface for developers to interact with the documentation—all while maintaining 100% data privacy through local execution.

## ✨ Key Features

- **Authenticated Scraper**: Automated Microsoft Entra ID authentication using headless Playwright to bypass SSO gateways.
- **Async Extraction Pipeline**: High-performance asynchronous fetching with rate-limiting and automatic re-authentication.
- **Semantic Parsing**: HTML-to-Markdown conversion using `trafilatura` to preserve tables, code blocks, and metadata.
- **Local RAG Integration**: Powered by LangChain, local Ollama models (`qwen2.5:7b`), and ChromaDB for privacy-preserving retrieval.
- **IDE-Like UI**: A sleek Streamlit-based chat interface with dark mode, conversational memory, and direct verifiable citations.

## 🛠️ Tech Stack

- **Package Manager**: [Astral `uv`](https://github.com/astral-sh/uv)
- **Scraping**: `httpx`, `Playwright`, `trafilatura`
- **AI/RAG**: `LangChain`, `ChromaDB`, `Ollama`
- **UI**: `Streamlit`, `rich`
- **Models**: `qwen2.5:7b` (Generation), `nomic-embed-text` (Embeddings)

## 🏗️ Architecture

The project is strictly decoupled into three primary boundaries to ensure maintainability:

1.  **Scraper (`scraper/`)**: Acquisition of raw HTML/Markdown data. Isolated Playwright logic.
2.  **Ingestion (`ingestion/`)**: Processing, chunking, and embedding document data into the vector store.
3.  **UI (`ui/`)**: The LangChain LCEL retrieval chain and the Streamlit frontend.

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
    ollama run qwen2.5:7b
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
