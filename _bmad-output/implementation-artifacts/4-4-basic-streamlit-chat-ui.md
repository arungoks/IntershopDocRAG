# Story 4.4: Basic Streamlit Chat UI

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a developer,
I want to interact with the RAG pipeline through a clean, browser-based chat interface,
so that I don't have to use a command-line terminal to query the knowledge base.

## Acceptance Criteria

1. **Given** the developer runs `uv run streamlit run ui/app.py`
2. **When** the browser opens to `localhost:8501`
3. **Then** a basic Streamlit interface renders with a fixed bottom `st.chat_input` text box
4. **And** the user can submit a query and see their message appear as an `st.chat_message("user")`
5. **And** the app calls the LCEL chain (from Story 4.2/4.3) and streams the output directly into an `st.chat_message("assistant")` using `st.write_stream`
6. **And** the UI successfully renders standard markdown and code block formatting returned by the LLM
7. **And** the conversation seamlessly persists on the screen as `st.session_state` memory grows

## Tasks / Subtasks

- [x] Task 1: Setup Streamlit Entrypoint
  - [x] `ui/app.py` initialised with `st.set_page_config` (title: "IntershopRAG", icon: 📚, layout: centered).
  - [x] App title and caption rendered at the top of the page.
- [x] Task 2: Implement Session State Memory
  - [x] `st.session_state.messages` initialised to `[]` on first load.
  - [x] History-render loop iterates over all messages and renders each via `st.chat_message(role)` + `st.markdown(content)`.
- [x] Task 3: Implement Chat Input & Processing Loop
  - [x] `st.chat_input("Ask about Intershop…")` captures the user query.
  - [x] User message rendered immediately in a user bubble and appended to session state.
  - [x] `generate_answer(query, retriever, llm, chat_history=history_for_chain)` called with full conversation history.
  - [x] `st.write_stream(stream)` renders the typing effect; return value is the full concatenated string.
  - [x] Full assistant response appended to `st.session_state.messages`.
- [x] Task 4: UI / Backend Decoupling
  - [x] `ui/app.py` contains all Streamlit (`st.*`) logic. `ui/chain.py` contains zero `st.*` calls. Boundary enforced.

## Dev Notes

- **Streamlit Streaming:** `st.write_stream` is the modern, preferred way to handle streaming LLM outputs in Streamlit (v1.30+). It automatically handles the typing effect and returns the full string when complete, which makes saving to session state trivial: `full_response = st.write_stream(stream_generator)`.
- **Handling Documents/Citations:** The chain function currently returns `(stream_generator, source_documents)`. For this basic story, you can capture the documents but you don't need to perfectly style them yet (Story 4.5 focuses on the raw citation display, and 5.2 enhances it). Just ensure the chain executes and the text streams.
- **Performance:** Ensure the retriever/LLM initialization in `ui/chain.py` is cached (e.g., using `@st.cache_resource` on a setup function) so it isn't rebuilt on every chat interaction.

### Project Structure Notes

- Creates `ui/app.py` as the main entry point for the frontend.
- Integrates with the existing `ui/chain.py`.

### References

- [Source: epics.md#Story 4.4: Basic Streamlit Chat UI]
- [Source: ux-design-specification.md#2.5 Experience Mechanics]

## Dev Agent Record

### Agent Model Used

Claude Sonnet 4.6 (Thinking)

### Debug Log References

### Completion Notes List

- Created `ui/app.py` with `st.set_page_config`, cached resource init (`@st.cache_resource` for both retriever and LLM), session-state history loop, and the full chat input/processing loop.
- `history_for_chain = st.session_state.messages[:-1]` passes all previous turns (excluding the current user query) to `generate_answer` as `chat_history`, enabling 4.3 conversational memory.
- Error handling: `try/except` around both the resource initialisation (DB/Ollama not ready) and the generation call (connectivity failures during inference).
- `st.write_stream` both renders the typing effect and returns the full string for session state persistence.
- Architectural boundary enforced: zero LangChain imports in `app.py`; zero `st.*` calls in `chain.py`.

### File List

- `ui/app.py` (created)
