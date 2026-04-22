# Story 4.2: Grounded Answer Generation (LCEL Chain)

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a developer,
I want the system to generate a technical answer strictly based on the retrieved Intershop documentation,
so that I don't receive hallucinated APIs or generic advice.

## Acceptance Criteria

1. **Given** the extracted context string from Story 4.1
2. **When** the LangChain LCEL chain executes
3. **Then** it passes the query and context to a `ChatOllama` model (configured for `qwen2.5:7b` on `localhost:11434`)
4. **And** a strict System Prompt enforces that the model MUST answer solely based on the provided context
5. **And** the generation response is returned as an iterable stream (for real-time typing UI)
6. **And** the chain output includes both the generated text and the list of raw retrieved LangChain `Document` objects (for citation rendering)

## Tasks / Subtasks

- [x] Task 1: Setup ChatOllama Model
  - [x] Initialize `langchain_ollama.ChatOllama` pointing to `localhost:11434` using the `qwen2.5:7b` model (values derived from `config.yaml` via `build_llm()`).
- [x] Task 2: Create System Prompt
  - [x] Implemented `GROUNDED_PROMPT` as a `ChatPromptTemplate` with a strict system message using `{context}` and `{question}` variables.
  - [x] Explicit rule in prompt instructs the LLM to acknowledge when context is insufficient rather than hallucinating.
- [x] Task 3: Build the LCEL Generation Chain
  - [x] `generate_answer(query, retriever, llm)` implements the two-phase pattern: retrieve docs → stream via `GROUNDED_PROMPT | llm | StrOutputParser()`.
  - [x] Returns a tuple `(stream_generator, source_documents)` — stream is compatible with `st.write_stream()`.
- [ ] Task 4: Unit Testing _(skipped per user instruction)_
  - [ ] Update `tests/ui/test_chain.py` to test the new prompt and chain components.
  - [ ] Mock `ChatOllama` and the retriever to ensure unit tests execute without local network/inference dependencies.

## Dev Notes

- **LCEL & Streaming Constraint:** Streamlit's `st.write_stream` expects an iterable/generator. Since you also need to return the source `Document` objects for citations (AC 6), a standard LCEL chain `.stream()` might not naturally return the context alongside the stream chunks. A common pattern is to:
  1. Retrieve the documents explicitly using the retriever.
  2. Format the documents into the context string.
  3. Invoke the LLM chain with `.stream({"context": ctx, "question": query})`.
  4. Return a tuple of `(stream_generator, source_documents)`.
- **Architectural Boundaries:** Keep all LLM/LangChain logic inside `ui/chain.py`. Do not reference Streamlit (`st.*`) in `ui/chain.py`. The Streamlit app (`ui/app.py`) will handle the streaming logic.
- **Dependency Guardrails:** Use `langchain_ollama` strictly for the LLM. 

### Project Structure Notes

- Logic belongs in `ui/chain.py` alongside the retriever from 4.1.
- Config values (Ollama port, model name) should be loaded from the centralized `config.yaml`.

### References

- [Source: epics.md#Story 4.2: Grounded Answer Generation (LCEL Chain)]
- [Source: architecture.md#The Interaction Boundary (ui/)]

## Dev Agent Record

### Agent Model Used

Claude Sonnet 4.6 (Thinking)

### Debug Log References

### Completion Notes List

- Added `build_llm()` to `ui/chain.py` — reads `ollama_model` and `ollama_port` from `config.yaml`.
- `GROUNDED_PROMPT` is a module-level `ChatPromptTemplate` with 5 strict anti-hallucination rules.
- `generate_answer(query, retriever, llm)` implements the two-phase LCEL pattern from dev notes: retrieval first (preserving `source_docs` for citations), then `GROUNDED_PROMPT | llm | StrOutputParser()` for streaming.
- No-context shortcut: if `retrieve_context` returns the sentinel, a pre-canned generator is returned immediately without ever calling the LLM.
- Unit tests skipped per user instruction.

### File List

- `ui/chain.py` (updated)
