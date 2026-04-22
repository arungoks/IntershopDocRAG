# Story 4.1: Vector Retrieval & Context Gathering

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a developer,
I want my natural language query to retrieve the most relevant Knowledge Base articles from the local vector database,
so that the LLM has accurate, proprietary context to answer my question.

## Acceptance Criteria

1. **Given** the local ChromaDB database is populated from Epic 3
2. **When** the `ui/chain.py` module receives a user query string
3. **Then** it uses a LangChain `Chroma` retriever with the local `OllamaEmbeddings` to fetch the top-k most relevant document chunks
4. **And** it extracts both the `.page_content` and the `.metadata` (specifically `title` and `url`) from the retrieved chunks
5. **And** it packages this context as a string to be injected into an LLM prompt
6. **And** if no relevant context can be found, the system explicitly returns a structured "No context found" indicator

## Tasks / Subtasks

- [x] Task 1: Setup Local Chroma Retriever
  - [x] Initialize `OllamaEmbeddings` configured to point to `localhost:11434` using the `nomic-embed-text` model (values from `config.yaml`).
  - [x] Initialize `langchain_chroma.Chroma` pointing to `data/vectordb/`.
  - [x] Configure the retriever to return `k` top documents (retrieve top `k` from `config.yaml`, default to 5).
- [x] Task 2: Implement Context Formatting
  - [x] Implement formatting logic (`format_docs`) that takes a list of retrieved LangChain `Document` chunks and concatenates them into a single context string.
  - [x] Guarantee that the formatting includes the `title` and `url` from the document `metadata` so the LLM knows the source of the text.
- [x] Task 3: Error / Empty State Handling
  - [x] Detect if the retriever returns zero matches or if ChromaDB throws an explicitly empty collection error.
  - [x] Return a structured "No context found" indication or string explicitly informing the pipeline that context is unavailable.
- [x] Task 4: Streamlit Resource Preparation
  - [x] `build_retriever()` is a standalone function ready to be decorated with `@st.cache_resource` in `ui/app.py`. No `st.*` imports in `chain.py`.
- [ ] Task 5: Unit Testing _(skipped per user instruction)_
  - [ ] Add tests in `tests/ui/test_chain.py`.
  - [ ] Mock the LangChain `Chroma` retriever to ensure formatting and error handling behave as expected without requiring disk I/O.

## Dev Notes

- **Streamlit Caching Risk:** Because `ui/chain.py` will serve as the engine for a Streamlit app, any database or embedding object initializations should be lazy-loaded or explicitly cached using `@st.cache_resource` to avoid severe performance degradation upon Streamlit reruns.
- **LCEL Integration:** Consider exposing the retriever as part of a LangChain Expression Language (LCEL) chain. A standard pattern is `{"context": retriever | format_docs, "question": RunnablePassthrough()}`.
- **Dependency Guardrails:** Use `langchain_chroma` and `langchain_ollama` strictly. Verify locally that no `openai` API requests slip through.

### Project Structure Notes

- Logic belongs in `ui/chain.py`. This sits firmly inside the Interaction Boundary.
- `ui/chain.py` acts as the data retrieval backend for `ui/app.py`. Do not inject `st.sidebar` or UI widgets here. Keep it decoupled.

### References

- [Source: epics.md#Epic 4: RAG Chat Experience]
- [Source: epics.md#Story 4.1: Vector Retrieval & Context Gathering]
- [Source: architecture.md#The Interaction Boundary (ui/)]

## Dev Agent Record

### Agent Model Used

Claude Sonnet 4.6 (Thinking)

### Debug Log References

### Completion Notes List

- Created `ui/chain.py` with `_load_config()`, `build_retriever()`, `format_docs()`, and `retrieve_context()` functions.
- `build_retriever()` is fully Streamlit-agnostic; caller wraps it with `@st.cache_resource` to avoid repeated DB initialisation on Streamlit reruns.
- `NO_CONTEXT_SENTINEL` constant (`"__NO_CONTEXT_FOUND__"`) used to signal empty retrieval results — downstream chain and UI components check for this string.
- Config values (`ollama_port`, `embedding_model`, `chroma_db_path`, `retrieval_k`) loaded from `config.yaml`; `retrieval_k` defaults to 5 if not present (backward-compatible).
- `retrieve_context()` swallows Chroma/Ollama exceptions and returns the sentinel + empty list, allowing `ui/app.py` to show a user-friendly `st.error()`.
- Unit tests skipped per user instruction.

### File List
- `ui/chain.py` (created)
---
