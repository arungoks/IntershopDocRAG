# Story 4.1: Vector Retrieval & Context Gathering

Status: ready-for-dev

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

- [ ] Task 1: Setup Local Chroma Retriever
  - [ ] Initialize `OllamaEmbeddings` configured to point to `localhost:11434` using the `nomic-embed-text` model (values from `config.yaml`).
  - [ ] Initialize `langchain_chroma.Chroma` pointing to `data/vectordb/`.
  - [ ] Configure the retriever to return `k` top documents (retrieve top `k` from `config.yaml`, default to 5).
- [ ] Task 2: Implement Context Formatting
  - [ ] Implement formatting logic (`format_docs`) that takes a list of retrieved LangChain `Document` chunks and concatenates them into a single context string.
  - [ ] Guarantee that the formatting includes the `title` and `url` from the document `metadata` so the LLM knows the source of the text.
- [ ] Task 3: Error / Empty State Handling
  - [ ] Detect if the retriever returns zero matches or if ChromaDB throws an explicitly empty collection error.
  - [ ] Return a structured "No context found" indication or string explicitly informing the pipeline that context is unavailable.
- [ ] Task 4: Streamlit Resource Preparation
  - [ ] Wrap the retriever/DB initialization in a caching mechanism (e.g., preparing it to be wrapped with `@st.cache_resource` in the main app file) so Streamlit does not reload the massive db index on every query.
- [ ] Task 5: Unit Testing
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

Gemini 3.1 Pro (High)

### Debug Log References

### Completion Notes List

- Addressed critical Streamlit caching constraint for database connection efficiency.
- Re-enforced architectural boundary rules preventing UI components leaking into the backend chain logic.

### File List
- `ui/chain.py` (to be created)
- `tests/ui/test_chain.py` (to be created)
---
