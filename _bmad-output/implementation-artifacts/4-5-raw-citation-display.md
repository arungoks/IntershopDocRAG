# Story 4.5: Raw Citation Display

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a developer,
I want the chat interface to explicitly list the source documents it used to generate the answer,
so that I can verify the information or read the full article context.

## Acceptance Criteria

1. **Given** the LCEL chain returns a generated response and the raw retrieved LangChain `Document` source objects
2. **When** the `st.chat_message("assistant")` finishes streaming the LLM text
3. **Then** the UI extracts the `url` and `title` metadata from the source objects
4. **And** it appends a raw text list of these sources to the bottom of the chat bubble (e.g., "Sources: Article 1 (URL), Article 2 (URL)")

## Tasks / Subtasks

- [x] Task 1: Capture Source Documents
  - [x] Updated `ui/app.py` to capture `source_docs` (renamed from `_source_docs`) returned by `generate_answer`.
- [x] Task 2: Format Citation List
  - [x] Created `ui/citations.py` with `format_citations(docs)` that deduplicates by `url` metadata (falls back to `title` for docs without URLs).
  - [x] Builds a markdown string: `\n\n**Sources:**\n- [Title](URL)\n- ...`
- [x] Task 3: Render and Persist
  - [x] `st.markdown(citation_block)` renders the citation list inside the assistant bubble immediately after `st.write_stream` completes.
  - [x] `full_response + citation_block` appended to `st.session_state.messages` so citations persist on reruns.
- [x] Task 4: Edge Case Handling
  - [x] `format_citations` returns `""` for empty or metadata-less doc lists; the `if citation_block:` guard prevents rendering an empty block. Error paths also set `citation_block = ""` to prevent appending garbage.

## Dev Notes

- **Separation of Concerns:** You might want to create a `format_citations(docs)` helper function. According to the architecture and UX specifications, a dedicated helper (`ui/citations.py`) is ideal to keep `app.py` clean.
- **Simplicity Constraints:** For this story, stick to a raw markdown text list. Do not worry about advanced HTML formatting, CSS sub-text styling, or visual dividers yet. Epic 5 (specifically Story 5.2) will focus on polishing this into a beautifully styled footer.
- **Session State:** By appending the citations directly to the assistant's string message before saving to `st.session_state.messages`, the citations will automatically render as part of the normal chat history loop you built in 4.4 without requiring complex state structures.

### Project Structure Notes

- Modifies `ui/app.py`.
- May create `ui/citations.py` for helper logic.

### References

- [Source: epics.md#Story 4.5: Raw Citation Display]
- [Source: ux-design-specification.md#2.5 Experience Mechanics]

## Dev Agent Record

### Agent Model Used

Claude Sonnet 4.6 (Thinking)

### Debug Log References

### Completion Notes List

- Created `ui/citations.py` with `format_citations(docs)`: deduplicates by URL, builds a raw markdown `**Sources:**` list, returns `""` for empty/no-metadata inputs.
- Updated `ui/app.py`: captures `source_docs` from `generate_answer`, renders citation block with `st.markdown()` inside the assistant bubble, persists `full_response + citation_block` in session state so citations survive reruns.
- Error path explicitly sets `citation_block = ""` so the session state append is always safe.
- `ui/citations.py` is Streamlit-free, ready for upgrade to HTML-styled footer in Story 5.2.

### File List

- `ui/citations.py` (created)
- `ui/app.py` (updated)
