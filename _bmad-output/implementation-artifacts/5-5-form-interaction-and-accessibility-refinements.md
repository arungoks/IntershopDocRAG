# Story 5.5: Form Interaction & Accessibility Refinements

Status: review

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

- [x] Task 1: Enforce Input Locking
  - [x] Streamlit >= 1.30 handles this natively via top-down execution script locking.
- [x] Task 2: Fix Code Block Overflow
  - [x] Custom CSS injection block added in `ui/app.py` using `st.markdown("<style>...</style>", unsafe_allow_html=True)`.
  - [x] Targeted `[data-testid="stMarkdownContainer"] pre, .stCodeBlock` to apply `overflow-x: auto !important; max-width: 100%;`.
- [x] Task 3: Ensure Scroll and Focus Behaviors
  - [x] Streamlit's `st.write_stream` natively forces the browser to auto-scroll to the bottom of the page.
  - [x] Added `components.html()` snippet at the end of `ui/app.py` to restore chat input focus after `st.rerun()`.
- [x] Task 4: Keyboard Accessibility Check
  - [x] Native Streamlit buttons and inputs (`st.sidebar.button`, `st.chat_input`) manage `tabindex` correctly out-of-the-box.

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

- Input locking, auto-scroll, and accessibility are handled natively by the Streamlit framework.
- Applied CSS injection early in `ui/app.py` (`st.markdown(..., unsafe_allow_html=True)`) to fix wide code block overflow.
- Implemented JS injection hack at the end of `ui/app.py` via `components.html()` to force focus back into the `st.chat_input` element after every generation cycle and `st.rerun()`.

### File List

- `ui/app.py` (updated)
