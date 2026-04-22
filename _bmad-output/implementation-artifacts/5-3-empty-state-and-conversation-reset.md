# Story 5.3: Empty State & Conversation Reset

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a developer,
I want to see helpful system prompts when I first load the app, and I want an easy way to clear my session context,
so that I know exactly how to query the system and can avoid "context bleed" between different problems.

## Acceptance Criteria

1. **Given** a user opens the app (or clicks the "Clear History" button)
2. **When** the chat history is empty
3. **Then** a visually distinct Empty State component renders in the center of the screen
4. **And** it displays 2-3 clickable example prompts that auto-populate the input box when clicked
5. **And** a full-width "Clear Chat History" button exists persistently in the left `st.sidebar`
6. **And** clicking the "Clear History" button wipes `st.session_state` and triggers `st.rerun()`

## Tasks / Subtasks

- [x] Task 1: Create Sidebar Reset Functionality
  - [x] `st.sidebar` added to `ui/app.py` with a title, caption, and dividers.
  - [x] `st.button("\U0001f5d1\ufe0f Clear Chat History", use_container_width=True)` added.
  - [x] Button clears `st.session_state.messages` and `st.session_state.pending_query`, then calls `st.rerun()`.
- [x] Task 2: Implement Empty State Layout
  - [x] `if not st.session_state.messages:` guard renders the empty state.
  - [x] Welcome header `### \U0001f44b Welcome to IntershopRAG` rendered.
  - [x] Introductory markdown explains the tool purpose and grounded sourcing.
- [x] Task 3: Implement Clickable Example Prompts
  - [x] Three example prompts defined: Pipeline Framework, REST API errors, cartridge extension.
  - [x] Buttons rendered in equal-width columns; clicking sets `st.session_state.pending_query` and calls `st.rerun()`.
  - [x] Main processing loop resolves `user_query = st.session_state.pending_query or chat_input_query`, consuming both input sources identically.

## Dev Notes

- **Streamlit Constraint - Auto-populating Input:** Streamlit's `st.chat_input` component *cannot* be programmatically populated with text (as of current versions). To achieve the "clickable example prompts" requirement, the buttons should completely bypass the input box. When an example button is clicked, immediately append that string to the session state as a "user" message and process it just as if they had typed it.
- **Rerun Logic:** Clearing the history requires a full `st.rerun()` to cleanly wipe the rendered chat bubbles from the DOM. 
- **Layout:** The empty state should ideally be centered vertically, but Streamlit's top-down flow means placing it where the chat bubbles usually go is sufficient.

### Project Structure Notes

- All changes are contained within `ui/app.py`.

### References

- [Source: epics.md#Story 5.3: Empty State & Conversation Reset]
- [Source: ux-design-specification.md#3. Component Strategy]

## Dev Agent Record

### Agent Model Used

Claude Sonnet 4.6 (Thinking)

### Debug Log References

### Completion Notes List

- Added `st.session_state.pending_query` to bridge the gap between example-prompt button clicks and the main query processing loop — since `st.chat_input` cannot be programmatically populated (per dev notes).
- Example buttons call `st.rerun()` after setting `pending_query`; on the next rerun `pending_query` takes priority over `chat_input`, then is cleared immediately after consumption.
- Sidebar contains the Clear History button with `use_container_width=True`, branding text, and a usage caption.
- Empty state is hidden once messages exist, so it never competes visually with active conversation.

### File List

- `ui/app.py` (rewritten)
