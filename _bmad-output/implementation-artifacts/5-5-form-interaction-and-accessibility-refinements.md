# Story 5.5: Form Interaction & Accessibility Refinements

Status: ready-for-dev

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a developer,
I want the chat interface to lock while processing and automatically handle scrolling and focus,
so that my interaction is frictionless, keyboard-driven, and prevents double-submissions.

## Acceptance Criteria

1. **Given** the Streamlit frontend is rendering
2. **When** the user interacts with the app
3. **Then** the `st.chat_input` text box is disabled the moment a query is submitted, and only re-enabled after the final citation footer renders
4. **And** the UI automatically scrolls the viewport to the bottom as the LLM streams its response
5. **And** the chat input box auto-focuses on initial page load and after every generation cycle
6. **And** all interactive elements (buttons, links) can be navigated to via the `Tab` key
7. **And** wide UI elements (like code blocks) utilize horizontal scrolling (`overflow-x: auto`) rather than breaking the center max-width layout container

## Tasks / Subtasks

- [ ] Task 1: Enforce Input Locking
  - [ ] Verify that `st.chat_input` natively disables during the synchronous LLM generation block. If needed, implement a `st.session_state.is_processing` flag to explicitly pass `disabled=st.session_state.is_processing` to the input.
- [ ] Task 2: Fix Code Block Overflow
  - [ ] Add a custom CSS injection block in `ui/app.py` using `st.markdown("<style>...</style>", unsafe_allow_html=True)`.
  - [ ] Target the `.stMarkdown pre` and `.stCodeBlock` elements to apply `overflow-x: auto !important; max-width: 100%;`.
- [ ] Task 3: Ensure Scroll and Focus Behaviors
  - [ ] Verify that `st.write_stream` forces the browser to auto-scroll to the bottom of the page natively.
  - [ ] Implement a lightweight JS snippet via `st.components.v1.html` if the chat input loses focus after a generation cycle, or rely on Streamlit's native input retention if using the latest version.
- [ ] Task 4: Keyboard Accessibility Check
  - [ ] Ensure any newly added UI elements (like the sidebar "Clear History" button or citation links) do not use negative `tabindex` and are reachable via standard keyboard `Tab` flow.

## Dev Notes

- **Streamlit Native Features:** Streamlit >= 1.30 handles much of this automatically. `st.chat_input` inherently locks the UI during the top-down python execution script. `st.write_stream` natively pins the scroll to the bottom.
- **CSS Injection Constraints:** When injecting CSS, use broad class selectors (like `[data-testid="stMarkdownContainer"] pre`) as Streamlit occasionally changes its internal DOM structure.
- **Focus Hack:** Streamlit does not expose an `.auto_focus()` python method. If focus is dropped after an `st.rerun()`, a common workaround is injecting `<script>window.parent.document.querySelector('input[data-testid="stChatInput"]').focus();</script>`.

### Project Structure Notes

- Modifies `ui/app.py` for CSS/JS injections.

### References

- [Source: epics.md#Story 5.5: Form Interaction & Accessibility Refinements]
- [Source: ux-design-specification.md#Responsive Strategy]

## Dev Agent Record

### Agent Model Used

Gemini 3.1 Pro (High)

### Debug Log References

### Completion Notes List

- Identified native Streamlit behaviors that satisfy ACs vs behaviors that require CSS/JS hacks.
- Provided the specific Javascript snippet needed for the focus workaround.

### File List

- `ui/app.py` (to be updated)
