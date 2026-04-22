# Story 5.1: Theming & Typography Adjustments

Status: ready-for-dev

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a generic user,
I want the chat interface to use a specific dark theme and legible fonts,
so that the application feels like a modern IDE and minimizes eye strain.

## Acceptance Criteria

1. **Given** the Streamlit app is running
2. **When** a user views the application
3. **Then** the UI strictly uses the Dark Mode palette (Background `#0E1117`, Primary Text `#FAFAFA`, Accent `#569CD6`) configured via `.streamlit/config.toml`
4. **And** system sans-serif fonts are applied to standard text, while monospace fonts are applied to code blocks
5. **And** text contrast ratios meet or exceed WCAG AA standards (4.5:1 minimum)

## Tasks / Subtasks

- [ ] Task 1: Configure Streamlit Theme
  - [ ] Locate or create `.streamlit/config.toml` in the project root.
  - [ ] Add the `[theme]` section block.
  - [ ] Set `base="dark"`.
  - [ ] Set `primaryColor="#569CD6"` (IDE Accent Blue).
  - [ ] Set `backgroundColor="#0E1117"` (Deep Dark Background).
  - [ ] Set `secondaryBackgroundColor="#262730"` (for sidebars/chat inputs).
  - [ ] Set `textColor="#FAFAFA"` (High Contrast Off-White).
- [ ] Task 2: Typography Configuration
  - [ ] Set `font="sans serif"` in the `[theme]` block.
- [ ] Task 3: Visual Verification
  - [ ] Ensure that code blocks natively rendered by Streamlit (`st.markdown`) use a distinct monospace font compared to the standard sans-serif body text.

## Dev Notes

- **Implementation Location:** This story is purely configuration-driven. No changes to `ui/app.py` or Python logic are required. All work should happen in `.streamlit/config.toml`.
- **Contrast Compliance:** The requested palette inherently passes the WCAG AA 4.5:1 ratio constraint on the specified dark background.
- **Code Block Fonts:** Streamlit's markdown parser automatically wraps triple backticks in `<pre><code>` blocks styled with monospace fonts. Your `font="sans serif"` config will only apply to the main UI body, fulfilling the typography requirement seamlessly.

### Project Structure Notes

- Modifies/creates `.streamlit/config.toml`.

### References

- [Source: epics.md#Story 5.1: Theming & Typography Adjustments]
- [Source: ux-design-specification.md#Visual Design Foundation]

## Dev Agent Record

### Agent Model Used

Gemini 3.1 Pro (High)

### Debug Log References

### Completion Notes List

- Translated UX specifications directly into Streamlit TOML config values.
- Noted that Streamlit natively handles the monospace code block rendering.

### File List

- `.streamlit/config.toml` (to be created/updated)
