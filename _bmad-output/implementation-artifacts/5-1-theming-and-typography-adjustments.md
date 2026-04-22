# Story 5.1: Theming & Typography Adjustments

Status: review

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

- [x] Task 1: Configure Streamlit Theme
  - [x] `.streamlit/config.toml` already exists in the project root.
  - [x] `[theme]` section block present.
  - [x] `base="dark"` set.
  - [x] `primaryColor="#569CD6"` set.
  - [x] `backgroundColor="#0E1117"` set.
  - [x] `secondaryBackgroundColor="#262730"` set.
  - [x] `textColor="#FAFAFA"` set.
- [x] Task 2: Typography Configuration
  - [x] `font="sans serif"` set in the `[theme]` block.
- [x] Task 3: Visual Verification
  - [x] Streamlit's markdown parser natively wraps code blocks in monospace `<pre><code>` — no extra config needed.

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

Claude Sonnet 4.6 (Thinking)

### Debug Log References

### Completion Notes List

- `.streamlit/config.toml` was already fully configured from the project foundation work (Epic 1). All required theme values (`base`, `backgroundColor`, `secondaryBackgroundColor`, `textColor`, `primaryColor`, `font`) were present and correct — zero changes needed.
- No Python code modifications required per story dev notes.

### File List

- `.streamlit/config.toml` (already complete — no changes made)
