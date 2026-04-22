"""
ui/app.py - IntershopRAG Streamlit Chat Application
             (Stories 4.4, 4.5, 5.2, 5.3, 5.4 & 5.5: Chat UI + Citations + UX Polish)

Entry point: uv run streamlit run ui/app.py

Architecture boundaries:
  - ALL Streamlit logic lives here.
  - ALL LangChain / Ollama logic lives in ui/chain.py.
  - This file never touches LangChain internals directly.
"""

import sys
from pathlib import Path

# Ensure the project root is on sys.path so that `from ui.chain import …`
# resolves correctly when Streamlit runs this file as a script rather than
# as part of an installed package.
_PROJECT_ROOT = Path(__file__).parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import streamlit as st
import streamlit.components.v1 as components

from ui.chain import build_llm, build_retriever, generate_answer
from ui.citations import format_citation_footer

# ---------------------------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="IntershopRAG",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="auto",
)

# ---------------------------------------------------------------------------
# Global CSS Injection  (Story 5.5: Task 2)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Allow wide code blocks to scroll horizontally instead of breaking layout */
    [data-testid="stMarkdownContainer"] pre, .stCodeBlock {
        overflow-x: auto !important;
        max-width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Cached Resource Initialisation  (Performance)
# ---------------------------------------------------------------------------

@st.cache_resource(show_spinner="Loading Knowledge Base index…")
def _get_retriever():
    """Build and cache the Chroma retriever for the lifetime of the server."""
    return build_retriever()


@st.cache_resource(show_spinner="Connecting to Ollama…")
def _get_llm():
    """Build and cache the ChatOllama LLM for the lifetime of the server."""
    return build_llm()


# ---------------------------------------------------------------------------
# Session State Initialisation
# ---------------------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# pending_query holds a query submitted via an example-prompt button.
# Processed at the end of the script alongside chat_input submissions.
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

# ---------------------------------------------------------------------------
# Sidebar — Story 5.3: Conversation Reset  (Task 1)
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("## 📚 IntershopRAG")
    st.caption("Local RAG over Intershop Knowledge Base")
    st.divider()

    if st.button("🗑️ Clear Chat History", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.session_state.pending_query = None
        st.rerun()

    st.divider()
    st.caption(
        "Answers are grounded in official Intershop documentation "
        "and generated 100 % locally via Ollama."
    )

# ---------------------------------------------------------------------------
# App Header
# ---------------------------------------------------------------------------

st.title("📚 IntershopRAG")
st.caption(
    "Ask anything about the Intershop Knowledge Base — "
    "answers are grounded in official documentation and run 100 % locally."
)

# ---------------------------------------------------------------------------
# Render Existing Chat History
# ---------------------------------------------------------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        # unsafe_allow_html required to correctly render citation HTML anchors
        st.markdown(msg["content"], unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Story 5.3: Empty State  (Task 2 & 3)
# ---------------------------------------------------------------------------

_EXAMPLE_PROMPTS = [
    "What is the Intershop Pipeline Framework?",
    "How do I handle REST API errors in Intershop?",
    "How do I extend a cartridge in Intershop Commerce Management?",
]

if not st.session_state.messages:
    st.markdown("### 👋 Welcome to IntershopRAG")
    st.markdown(
        "Ask me anything about the **Intershop Knowledge Base**. "
        "I'll retrieve relevant documentation and generate a grounded answer — "
        "no hallucinations, every answer is backed by a source link.\n\n"
        "**Try one of these example questions:**"
    )

    # Render example prompt buttons. Clicking one sets pending_query and
    # reruns — the query is then processed in the main chat loop below.
    cols = st.columns(len(_EXAMPLE_PROMPTS))
    for col, prompt in zip(cols, _EXAMPLE_PROMPTS):
        with col:
            if st.button(prompt, use_container_width=True, key=f"ex_{prompt[:20]}"):
                st.session_state.pending_query = prompt
                st.rerun()

# ---------------------------------------------------------------------------
# Chat Input & Processing Loop
# ---------------------------------------------------------------------------

# Resolve the active query: prefer a pending example-prompt click over
# a newly-typed chat_input (only one can be active per rerun).
chat_input_query = st.chat_input("Ask about Intershop…")
user_query = st.session_state.pending_query or chat_input_query

# Clear the pending query now that we've consumed it
if st.session_state.pending_query:
    st.session_state.pending_query = None

if user_query:

    # Immediately render the user's message
    with st.chat_message("user"):
        st.markdown(user_query)

    # Append to session state so it persists on reruns
    st.session_state.messages.append(
        {"role": "user", "content": user_query}
    )

    # Initialise cached resources (built once, reused on every turn)
    try:
        retriever = _get_retriever()
        llm = _get_llm()
    except Exception as exc:
        st.error(
            f"⚠️ **Initialisation failed:** {exc}\n\n"
            "Please ensure Ollama is running (`ollama serve`) and that "
            "the vector database has been populated by running the "
            "ingestion pipeline first."
        )
        st.stop()

    # Generate and stream the assistant response
    with st.chat_message("assistant"):
        try:
            # Pass the full history *excluding* the current user message
            history_for_chain = st.session_state.messages[:-1]

            # Story 5.4: Task 1 — spinner is shown while retrieval + LLM
            # initialisation happens (before streaming begins).
            with st.spinner("Querying Knowledge Base…"):
                stream, source_docs = generate_answer(
                    query=user_query,
                    retriever=retriever,
                    llm=llm,
                    chat_history=history_for_chain,
                )

            # Stream the LLM response; st.write_stream returns the full string.
            # The spinner has already resolved by the time streaming starts.
            full_response: str = st.write_stream(stream)

            # Story 5.2: Render styled HTML citation footer in the same bubble.
            # unsafe_allow_html=True is required for <a target="_blank"> links.
            citation_block = format_citation_footer(source_docs)
            if citation_block:
                st.markdown(citation_block, unsafe_allow_html=True)

        except Exception as exc:
            # Story 5.4: Task 2 & 3 — descriptive error boundaries.
            error_type = type(exc).__name__
            error_msg = str(exc)

            # Detect Ollama / network connectivity failures:
            # langchain_ollama uses httpx; connection refused surfaces as
            # httpx.ConnectError or contains "connect" in the message.
            is_connection_error = (
                "ConnectError" in error_type
                or "connect" in error_msg.lower()
                or "connection" in error_msg.lower()
            )

            if is_connection_error:
                friendly = (
                    "⚠️ **Ollama Unreachable** — Could not connect to the local Ollama service.\n\n"
                    "**Fix:** Start Ollama in a terminal and ensure the model is available:\n"
                    "```\nollama run qwen2.5:3b\n```"
                )
                st.error(friendly)
                full_response = friendly
            else:
                friendly = f"⚠️ **Pipeline Error:** `{error_type}: {error_msg}`"
                st.error(friendly)
                full_response = friendly

            citation_block = ""  # No citations on error

    # Persist the full response + citations as one string in session state
    # so the combined content re-renders correctly in the history loop.
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response + citation_block}
    )

# ---------------------------------------------------------------------------
# Post-Generation Focus Hack  (Story 5.5: Task 3)
# ---------------------------------------------------------------------------
# Streamlit does not provide a native .focus() method for chat_input.
# Injecting a small invisible JS snippet at the end of the script ensures
# focus returns to the input box after every rerun / generation cycle.
components.html(
    """
    <script>
    const el = window.parent.document.querySelector('[data-testid="stChatInput"] textarea') 
               || window.parent.document.querySelector('textarea[aria-label="Ask about Intershop…"]') 
               || window.parent.document.querySelector('input[data-testid="stChatInput"]');
    if (el) {
        el.focus();
    }
    </script>
    """,
    height=0,
    width=0,
)
