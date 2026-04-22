# Story 5.3: Empty State & Conversation Reset

Status: ready-for-dev

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

- [ ] Task 1: Create Sidebar Reset Functionality
  - [ ] Update `ui/app.py` to include `st.sidebar`.
  - [ ] Add a button: `st.sidebar.button("Clear Chat History", use_container_width=True)`.
  - [ ] Bind the button to a callback or inline logic that clears `st.session_state.messages` and calls `st.rerun()`.
- [ ] Task 2: Implement Empty State Layout
  - [ ] In `ui/app.py`, detect when `st.session_state.messages` is empty.
  - [ ] When empty, render a Welcome header (e.g., `st.markdown("### Welcome to IntershopRAG")`).
  - [ ] Add introductory text explaining the tool's purpose.
- [ ] Task 3: Implement Clickable Example Prompts
  - [ ] Render 2-3 example prompt buttons (e.g., "Explain the Pipeline framework", "How do I handle REST API errors?").
  - [ ] Implement logic so that clicking an example button simulates a user submission: it appends the prompt to `st.session_state.messages` and immediately triggers the query processing loop (or `st.rerun()`).

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

Gemini 3.1 Pro (High)

### Debug Log References

### Completion Notes List

- Addressed the Streamlit limitation regarding `chat_input` programmatic population.
- Defined the logic for simulated submissions via `st.button`.

### File List

- `ui/app.py` (to be updated)
