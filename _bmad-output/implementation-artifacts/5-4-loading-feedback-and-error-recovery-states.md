# Story 5.4: Loading Feedback & Error Recovery States

Status: ready-for-dev

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a developer,
I want clear feedback while the system is retrieving context or when an internal pipeline fails,
so that I'm never left wondering if the app froze or why I didn't get an answer.

## Acceptance Criteria

1. **Given** the user submits a query
2. **When** the LCEL chain is querying ChromaDB and initializing Ollama
3. **Then** an `st.spinner()` displays an accurate status message (e.g., "Querying Knowledge Base...")
4. **And** if Ollama is unreachable (connection refused) or ChromaDB is missing, the system catches the error and renders a descriptive `st.error()` boundary explaining the failure and how to fix it

## Tasks / Subtasks

- [ ] Task 1: Implement Loading Feedback
  - [ ] In `ui/app.py`, wrap the LangChain retrieval and generation step (`ui.chain.generate_answer`) inside a `with st.spinner("Querying Knowledge Base..."):` context manager.
- [ ] Task 2: Implement Try/Catch Error Boundary
  - [ ] In `ui/app.py`, wrap the generation block within a `try...except Exception as e:` block.
  - [ ] If an error occurs, prevent the app from crashing with a raw Streamlit stack trace.
- [ ] Task 3: Render Descriptive Error States
  - [ ] Parse or analyze the caught exception `e`.
  - [ ] If the error indicates a connection refusal (e.g., `httpx.ConnectError`, `ConnectionError`), render an actionable `st.error()` message: "Error: Could not connect to local Ollama service. Please ensure `ollama run qwen2.5:7b` is active."
  - [ ] If the error is generic, render a fallback `st.error(f"Pipeline Failed: {str(e)}")`.

## Dev Notes

- **Streamlit Spinner:** The `st.spinner` automatically resolves and disappears when the `with` block exits (which is when `generate_answer` returns the stream generator). This perfectly satisfies the "Retrieval" loading state before the LLM starts typing.
- **Error Persistence:** Because Streamlit reruns from top to bottom, an `st.error` triggered during the chat loop will disappear if the user interacts again. This is generally acceptable for transient errors (like forgetting to start Ollama), but if you want it to persist, consider appending it to `st.session_state.messages` as a special error message. For this story, an inline `st.error` is sufficient.
- **LangChain Exceptions:** `langchain_ollama` relies on `httpx` under the hood. Connection refused errors will likely bubble up as `httpx.ConnectError`.

### Project Structure Notes

- Modifies `ui/app.py`.

### References

- [Source: epics.md#Story 5.4: Loading Feedback & Error Recovery States]
- [Source: ux-design-specification.md#Error Recovery Patterns]

## Dev Agent Record

### Agent Model Used

Gemini 3.1 Pro (High)

### Debug Log References

### Completion Notes List

- Designed graceful failure handling for the primary point of failure (Ollama daemon offline).
- Leveraged Streamlit's native `st.spinner` for zero-boilerplate loading states.

### File List

- `ui/app.py` (to be updated)
