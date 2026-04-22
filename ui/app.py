"""
ui/app.py - IntershopRAG Streamlit Chat Application
             (Stories 4.4 & 4.5: Basic Chat UI + Raw Citation Display)

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

from ui.chain import build_llm, build_retriever, generate_answer
from ui.citations import format_citations

# ---------------------------------------------------------------------------
# Page Configuration  (Task 1)
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="IntershopRAG",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="auto",
)

# ---------------------------------------------------------------------------
# Cached Resource Initialisation  (Performance — Dev Notes)
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
# Session State Initialisation  (Task 2)
# ---------------------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------------------------
# App Header  (Task 1)
# ---------------------------------------------------------------------------

st.title("📚 IntershopRAG")
st.caption(
    "Ask anything about the Intershop Knowledge Base — "
    "answers are grounded in official documentation and run 100 % locally."
)

# ---------------------------------------------------------------------------
# Render Existing Chat History  (Task 2)
# ---------------------------------------------------------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------------------------------------------
# Chat Input & Processing Loop  (Task 3)
# ---------------------------------------------------------------------------

if user_query := st.chat_input("Ask about Intershop…"):

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

            # Task 1: Capture source_docs alongside the stream
            stream, source_docs = generate_answer(
                query=user_query,
                retriever=retriever,
                llm=llm,
                chat_history=history_for_chain,
            )

            # Stream the LLM response; st.write_stream returns the full string
            full_response: str = st.write_stream(stream)

            # Task 2 & 3: Format citations and render them in the same bubble
            citation_block = format_citations(source_docs)
            if citation_block:
                st.markdown(citation_block)

        except Exception as exc:
            error_msg = str(exc)
            if "connect" in error_msg.lower() or "connection" in error_msg.lower():
                full_response = (
                    "⚠️ Could not connect to the local Ollama service. "
                    "Please ensure `ollama run qwen2.5:7b` is active and "
                    "retry your question."
                )
            else:
                full_response = f"⚠️ Pipeline error: {error_msg}"
            st.markdown(full_response)
            citation_block = ""  # No citations on error

    # Task 3: Persist the full response + citations as one string in session
    # state so the combined content re-renders correctly in the history loop.
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response + citation_block}
    )
