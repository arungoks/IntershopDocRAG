# Story 4.3: Conversational Memory Buffer

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a developer,
I want the system to remember my previous questions and its own answers during my session,
so that I can ask follow-up questions without repeating the full context.

## Acceptance Criteria

1. **Given** a developer is in an active chat session
2. **When** they ask a follow-up question (e.g., "Where can I find that file?")
3. **Then** the Streamlit `st.session_state` passes the previous turns (chat history) into the LangChain LCEL chain
4. **And** the LCEL chain uses a history-aware retriever prompt to rephrase the follow-up question into a standalone query before querying ChromaDB
5. **And** the final generation prompt includes the chat history along with the newly retrieved context

## Tasks / Subtasks

- [x] Task 1: Integrate Chat History into LCEL
  - [x] Updated `GROUNDED_PROMPT` in `ui/chain.py` to include `MessagesPlaceholder(variable_name="chat_history")` between the system message and human input.
  - [x] `chat_history` is passed as a kwarg to `generation_chain.stream()`.
- [x] Task 2: Implement History-Aware Retriever
  - [x] Created `CONTEXTUALISE_PROMPT` that instructs the LLM to rephrase follow-up questions into standalone queries.
  - [x] `build_history_aware_retriever(retriever, llm)` wraps the Chroma retriever using `create_history_aware_retriever`.
- [x] Task 3: Update Chain Interface
  - [x] `generate_answer(query, retriever, llm, chat_history=None)` now accepts optional `chat_history`.
  - [x] When `chat_history` is non-empty, the history-aware retriever path is taken; otherwise, the fast direct-retrieval path from 4.1/4.2 is used.
- [ ] Task 4: Unit Testing _(skipped per user instruction)_
  - [ ] Add tests in `tests/ui/test_chain.py` for the standalone query rephrasing chain.
  - [ ] Mock the LLM to verify that chat history is correctly passed into both the rephrasing prompt and the final generation prompt.

## Dev Notes

- **LangChain History-Aware Pattern:** The recommended approach for LCEL is to use `create_history_aware_retriever`. This requires a prompt that says "Given a chat history and the latest user question... formulate a standalone question."
- **Streamlit History Format:** Streamlit typically stores history as a list of dicts (e.g. `{"role": "user", "content": "hello"}`). LangChain expects `HumanMessage` and `AIMessage` objects, or tuples like `("user", "message")`. Ensure `ui/chain.py` converts the Streamlit representation to the LangChain representation if needed, without importing `streamlit` inside `chain.py`. A helper mapper in `chain.py` is fine.
- **Architectural Boundaries:** Keep `ui/chain.py` unaware of `st.session_state`. Let `ui/app.py` read from `st.session_state` and pass a standard list into `generate_answer`.

### Project Structure Notes

- Modifications will be contained primarily within `ui/chain.py` and `tests/ui/test_chain.py`.
- No new modules are expected to be created.

### References

- [Source: epics.md#Story 4.3: Conversational Memory Buffer]

## Dev Agent Record

### Agent Model Used

Claude Sonnet 4.6 (Thinking)

### Debug Log References

### Completion Notes List

- Added `MessagesPlaceholder(variable_name="chat_history")` to `GROUNDED_PROMPT` so history is rendered between the system context and the human turn.
- Created `CONTEXTUALISE_PROMPT` + `build_history_aware_retriever()` using `create_history_aware_retriever` from `langchain.chains`.
- Added `convert_chat_history()` helper that maps Streamlit `{role, content}` dicts to `HumanMessage` / `AIMessage` objects; no Streamlit imports needed in `chain.py`.
- `generate_answer()` now takes optional `chat_history: list | None`. Empty/None → fast direct-retrieval path (4.1 behaviour). Non-empty → history-aware retriever path (rephrasing + context + history in generation prompt).
- Unit tests skipped per user instruction.

### File List

- `ui/chain.py` (updated)
