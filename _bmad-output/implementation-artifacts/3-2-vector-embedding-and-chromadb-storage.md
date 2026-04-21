# Story 3.2: Vector Embedding & ChromaDB Storage

Status: ready-for-dev

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a system administrator,
I want the document chunks to be converted to vector embeddings and stored locally in ChromaDB,
so that semantic search can be performed against the dataset locally.

## Acceptance Criteria

1. **Given** a list of split document chunks from Story 3.1
2. **When** the `ingestion/embedder.py` module processes the chunks
3. **Then** it uses `OllamaEmbeddings` configured to point to `localhost:11434` with the `nomic-embed-text` model
4. **And** the embeddings and associated metadata are stored in a local ChromaDB instance utilizing `PersistentClient` pointing to `data/vectordb/`
5. **And** running the ingestion process multiple times updates existing documents or skips duplicates rather than blindly duplicating the entire database

## Tasks / Subtasks

- [ ] Task 1: Setup Local Ollama Embeddings
  - [ ] Initialize `OllamaEmbeddings` using `langchain-ollama`.
  - [ ] Read URL/Port (e.g. `localhost:11434`) and model name (`nomic-embed-text`) dynamically from `config.yaml`.
- [ ] Task 2: Configure ChromaDB Local Instance
  - [ ] Initialize ChromaDB using `langchain_chroma.Chroma` integration combined with a `PersistentClient` from the official `chromadb` package.
  - [ ] Set the persist directory to `data/vectordb/` (driven by `config.yaml`).
- [ ] Task 3: Implement Upsert Logic in `ingestion/embedder.py`
  - [ ] Implement a function to embed and store chunks provided by Story 3.1's splitter.
  - [ ] Generate deterministic IDs for each document chunk (e.g., using the `id` from YAML frontmatter concatenated with a chunk index or hash).
  - [ ] Use `add_documents()` or an explicit `upsert` mechanism leveraging the deterministic IDs to prevent database duplication on subsequent ingestion runs.
- [ ] Task 4: Unit Testing
  - [ ] Add pytest tests in `tests/ingestion/test_embedder.py`.
  - [ ] Mock the Chroma `PersistentClient` and the Ollama embedding API to test the logic without a live running database or Ollama server.

## Dev Notes

- **Avoiding Duplication**: The LangChain `Chroma.add_documents` method will blindly add duplicate vectors unless you explicitly pass a list of unique `ids`. To ensure updates overwrite instead of duplicating, generate a unique ID for each chunk. The chunk ID can be formed like `f"{chunk.metadata['id']}-chunk-{index}"` so that reruns seamlessly overwrite existing vectors.
- **Library Integrations**: Use `langchain_ollama.OllamaEmbeddings` and `langchain_chroma.Chroma`. Do not use older, deprecated `langchain.vectorstores`.
- **Security Constraint**: Verify that Ollama points explicitly to `localhost` and no cloud API keys are initialized. This strictly adheres to the offline execution requirement.
- **Config Reading**: Use the same configuration loader module established in previous steps. Make sure fallback values explicitly match the NFRs (`nomic-embed-text`).

### Project Structure Notes

- `ingestion/embedder.py` resides inside the Semantic Boundary.
- `data/vectordb/` should only be created if it does not already exist; ChromaDB's persistent client usually handles this internally.
- Follow `PEP-8` naming conventions: `snake_case` functions, `PascalCase` classes.

### References

- [Source: epics.md#Epic 3: Vector Ingestion Pipeline]
- [Source: epics.md#Story 3.2: Vector Embedding & ChromaDB Storage]
- [Source: architecture.md#Data Architecture]
- [Source: architecture.md#The Semantic Boundary (ingestion/)]

## Dev Agent Record

### Agent Model Used

Gemini 3.1 Pro (High)

### Debug Log References

### Completion Notes List

- Addressed potential duplicate document issue via explicit deterministic IDs.
- Highlighted the need for updated `langchain_chroma` and `langchain_ollama` integrations instead of legacy imports.

### File List
- `ingestion/embedder.py` (to be created/updated)
- `tests/ingestion/test_embedder.py` (to be created)
---
