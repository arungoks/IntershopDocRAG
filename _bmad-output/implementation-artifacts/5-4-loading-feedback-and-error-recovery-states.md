# Story 5.4: Loading Feedback & Error Recovery States

Status: review

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

- [x] Task 1: Implement Loading Feedback
  - [x] `generate_answer()` call wrapped in `with st.spinner("Querying Knowledge Base\u2026"):` inside the assistant bubble. Spinner auto-resolves before streaming begins.
- [x] Task 2: Implement Try/Catch Error Boundary
  - [x] Existing `try...except Exception as exc:` block retained and upgraded.
  - [x] Raw Streamlit stack traces are suppressed; all errors route to `st.error()`.
- [x] Task 3: Render Descriptive Error States
  - [x] `error_type = type(exc).__name__` captured for class-name-based detection.
  - [x] Connection errors detected via `"ConnectError" in error_type` (catches `httpx.ConnectError`) OR `"connect"` in message string.
  - [x] Connection error: `st.error()` with actionable fix including `ollama run qwen2.5:3b` code block.
  - [x] Generic error: `st.error(f"\u26a0\ufe0f **Pipeline Error:** `{error_type}: {error_msg}`")`.

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

Claude Sonnet 4.6 (Thinking)

### Debug Log References

### Completion Notes List

- Wrapped `generate_answer()` in `with st.spinner("Querying Knowledge Base\u2026"):`. The spinner resolves automatically when the context exits (i.e., when the stream generator is returned but before streaming begins), giving accurate feedback for the retrieval phase.
- Upgraded exception handler: captures `type(exc).__name__` for class-based detection of `httpx.ConnectError` in addition to message-string matching.
- Connection errors display `st.error()` with markdown formatting and a `ollama run` code block fix instruction.
- Generic errors display `st.error()` with the exception class name and message for easier debugging.
- Both error types append the friendly message to `st.session_state.messages` so the error persists on the next rerun.

### File List

- `ui/app.py` (updated)
