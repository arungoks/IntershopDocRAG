"""
ui/chain.py - Vector Retrieval, Context Gathering, Answer Generation
               & Conversational Memory  (Stories 4.1, 4.2 & 4.3)

This module implements the full LangChain retrieval + generation backend for
the IntershopRAG Streamlit UI.  It is strictly decoupled from Streamlit itself
— no `st.*` calls appear here.

Public API
----------
build_retriever()      -> VectorStoreRetriever   (cache with @st.cache_resource)
build_llm()            -> ChatOllama              (cache with @st.cache_resource)
retrieve_context()     -> (context_str, docs)
generate_answer()      -> (stream_generator, docs)
                          Accepts optional chat_history for follow-up questions.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Tuple

import yaml
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama, OllamaEmbeddings

# ---------------------------------------------------------------------------
# Configuration Loader
# ---------------------------------------------------------------------------

def _load_config() -> dict:
    """Load and return the centralised project config.yaml.

    Searches from the repo root (two levels up from this file by default,
    but falls back to a CONFIG_PATH env-var override for testing).
    """
    config_path_override = os.environ.get("INTERSHOP_CONFIG_PATH")
    if config_path_override:
        config_path = Path(config_path_override)
    else:
        # ui/chain.py → ui/ → project root
        config_path = Path(__file__).parent.parent / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"config.yaml not found at {config_path}. "
            "Set INTERSHOP_CONFIG_PATH env var to override."
        )

    with open(config_path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


# ---------------------------------------------------------------------------
# Retriever Factory
# ---------------------------------------------------------------------------

def build_retriever():
    """Build and return a configured LangChain Chroma retriever.

    This function is designed to be wrapped with ``@st.cache_resource`` in
    ``ui/app.py`` so it is called only once per Streamlit server process.

    Returns
    -------
    langchain_core.vectorstores.VectorStoreRetriever
        A retriever configured for similarity search against the local
        ChromaDB vector store.

    Raises
    ------
    FileNotFoundError
        If config.yaml cannot be located.
    Exception
        Any ChromaDB / Ollama initialisation errors propagate to the caller
        so that ``ui/app.py`` can display an actionable ``st.error`` message.
    """
    config = _load_config()

    ollama_port: int = config.get("ollama_port", 11434)
    embedding_model: str = config.get("embedding_model", "nomic-embed-text")
    chroma_db_path: str = config.get("chroma_db_path", "data/vectordb")
    retrieval_k: int = config.get("retrieval_k", 5)

    # Resolve db path relative to repo root
    db_path = Path(__file__).parent.parent / chroma_db_path

    embeddings = OllamaEmbeddings(
        model=embedding_model,
        base_url=f"http://localhost:{ollama_port}",
    )

    vector_store = Chroma(
        collection_name="intershop_kb",
        persist_directory=str(db_path),
        embedding_function=embeddings,
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": retrieval_k},
    )

    return retriever


# ---------------------------------------------------------------------------
# Context Formatting
# ---------------------------------------------------------------------------

# Sentinel returned when the retriever finds nothing relevant
NO_CONTEXT_SENTINEL = "__NO_CONTEXT_FOUND__"


def format_docs(docs: List[Document]) -> str:
    """Convert a list of retrieved LangChain Documents into a single context
    string suitable for injection into an LLM prompt.

    Each chunk is prefixed with its source metadata (title + URL) so the LLM
    can attribute claims to specific Knowledge Base articles.

    Parameters
    ----------
    docs:
        A list of ``langchain_core.documents.Document`` objects returned by
        the Chroma retriever.

    Returns
    -------
    str
        A formatted context string, or ``NO_CONTEXT_SENTINEL`` when *docs* is
        empty.
    """
    if not docs:
        return NO_CONTEXT_SENTINEL

    parts: List[str] = []
    for doc in docs:
        title = doc.metadata.get("title", "Unknown Article")
        url = doc.metadata.get("url", "")
        header = f"[Source: {title}]"
        if url:
            header += f" ({url})"
        parts.append(f"{header}\n{doc.page_content}")

    return "\n\n---\n\n".join(parts)


# ---------------------------------------------------------------------------
# Public Retrieval Entry-Point
# ---------------------------------------------------------------------------

def retrieve_context(query: str, retriever) -> Tuple[str, List[Document]]:
    """Retrieve the most relevant document chunks for *query* and format them.

    Parameters
    ----------
    query:
        The user's natural-language question.
    retriever:
        A LangChain retriever object (as returned by ``build_retriever()``).

    Returns
    -------
    context_str : str
        A formatted string containing the retrieved content ready for LLM
        injection, or ``NO_CONTEXT_SENTINEL`` if nothing was retrieved.
    source_docs : list[Document]
        The raw retrieved ``Document`` objects (used later for citation
        rendering).
    """
    try:
        docs: List[Document] = retriever.invoke(query)
    except Exception:
        # Surface an empty context rather than crashing — caller decides
        # how to handle (display st.error, etc.)
        return NO_CONTEXT_SENTINEL, []

    context_str = format_docs(docs)
    return context_str, docs


# ---------------------------------------------------------------------------
# LLM Factory  (Story 4.2)
# ---------------------------------------------------------------------------

def build_llm():
    """Build and return a configured ``ChatOllama`` LLM.

    Like ``build_retriever()``, this is designed to be wrapped with
    ``@st.cache_resource`` in ``ui/app.py`` so the connection is established
    only once per Streamlit server process.

    Returns
    -------
    ChatOllama
        An Ollama chat model instance pointed at the locally running daemon.
    """
    config = _load_config()

    ollama_port: int = config.get("ollama_port", 11434)
    ollama_model: str = config.get("ollama_model", "qwen2.5:7b")

    return ChatOllama(
        model=ollama_model,
        base_url=f"http://localhost:{ollama_port}",
    )


# ---------------------------------------------------------------------------
# Prompt Template  (Story 4.2)
# ---------------------------------------------------------------------------

# Strict grounding prompt — the LLM MUST NOT invent facts outside the context.
_SYSTEM_PROMPT = """\
You are a precise technical assistant for Intershop developers.
Your ONLY knowledge source is the context provided below, which contains
excerpts from the official Intershop Knowledge Base.

Strict rules:
1. Answer ONLY using information present in the provided context.
2. If the context does not contain enough information to answer the question,
   say: "I could not find relevant information in the Intershop Knowledge Base
   for this query. Please refine your question or check the documentation
   directly."
3. Never guess, invent API names, configuration keys, or code that is not
   explicitly shown in the context.
4. Format your answer in clean Markdown with code blocks where appropriate.
5. Be concise and directly relevant to the developer's question.

Context:
{context}
"""

GROUNDED_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", _SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)


# ---------------------------------------------------------------------------
# History-Aware Components  (Story 4.3)
# ---------------------------------------------------------------------------

# Contextualisation prompt: rephrases a follow-up question into a standalone
# search query that can be understood without the chat history.
_CONTEXTUALISE_SYSTEM = """\
Given a chat history and the latest user question which might reference context
in the chat history, formulate a standalone question which can be understood
without the chat history.  Do NOT answer the question; just reformulate it if
needed, otherwise return it as is.
"""

CONTEXTUALISE_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", _CONTEXTUALISE_SYSTEM),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)


def build_history_aware_retriever(retriever, llm):
    """Wrap *retriever* in a history-aware layer that first rephrases a
    follow-up question into a standalone query before hitting ChromaDB.

    Uses CONTEXTUALISE_PROMPT + *llm* to reformulate the question, then
    passes the result to the base *retriever*.  Returns a RunnableLambda
    that accepts ``{"input": str, "chat_history": list}`` and returns
    ``List[Document]`` — the same interface as ``create_history_aware_retriever``.

    Parameters
    ----------
    retriever:
        The base Chroma retriever (from ``build_retriever()``).
    llm:
        A ``ChatOllama`` instance (from ``build_llm()``).

    Returns
    -------
    RunnableLambda
        A callable chain compatible with ``.invoke({"input": ..., "chat_history": ...})``.
    """
    contextualise_chain = CONTEXTUALISE_PROMPT | llm | StrOutputParser()

    def _retrieve(inputs: dict) -> List[Document]:
        query: str = inputs.get("input", "")
        history: list = inputs.get("chat_history", [])

        # Only rephrase if there is prior history to reference
        if history:
            standalone_query: str = contextualise_chain.invoke(
                {"input": query, "chat_history": history}
            )
        else:
            standalone_query = query

        return retriever.invoke(standalone_query)

    return RunnableLambda(_retrieve)


# ---------------------------------------------------------------------------
# Streamlit ↔ LangChain Message Format Converter  (Story 4.3)
# ---------------------------------------------------------------------------

def convert_chat_history(streamlit_history: list) -> list:
    """Convert Streamlit session_state message dicts into LangChain message
    objects.

    Streamlit stores history as::

        [{"role": "user", "content": "..."},
         {"role": "assistant", "content": "..."}]

    LangChain prompts expect ``HumanMessage`` / ``AIMessage`` objects.
    This helper lives in ``chain.py`` (not ``app.py``) so the conversion
    logic is co-located with the prompt templates that consume it.

    Parameters
    ----------
    streamlit_history:
        List of message dicts from ``st.session_state.messages``.

    Returns
    -------
    list
        List of ``HumanMessage`` / ``AIMessage`` objects.
    """
    lc_messages = []
    for msg in streamlit_history:
        role = msg.get("role", "")
        content = msg.get("content", "")
        if role == "user":
            lc_messages.append(HumanMessage(content=content))
        elif role == "assistant":
            lc_messages.append(AIMessage(content=content))
        # Ignore unknown roles silently
    return lc_messages


# ---------------------------------------------------------------------------
# Public Generation Entry-Point  (Story 4.2)
# ---------------------------------------------------------------------------

def generate_answer(query: str, retriever, llm, chat_history: list | None = None):
    """Retrieve relevant context and stream a grounded LLM answer.

    Supports both single-turn queries and multi-turn conversations:
    - When *chat_history* is empty (or ``None``), the base retriever is used
      directly (same behaviour as Story 4.2).
    - When *chat_history* contains previous turns, a history-aware retriever
      first rephrases the question into a standalone query, then retrieves
      context, then passes both the history and the new context to the
      generation prompt.

    Parameters
    ----------
    query:
        The developer's natural-language question.
    retriever:
        A LangChain retriever (as returned by ``build_retriever()``).
    llm:
        A ``ChatOllama`` instance (as returned by ``build_llm()``).
    chat_history:
        Optional list of Streamlit message dicts
        (``[{"role": ..., "content": ...}]``).  Pass ``[]`` or ``None`` for
        a fresh conversation.

    Returns
    -------
    stream_generator : iterator
        A streaming iterator of LLM response text chunks, compatible with
        Streamlit's ``st.write_stream()``.
    source_docs : list[Document]
        Raw retrieved ``Document`` objects for citation rendering.
    """
    # Normalise history input
    lc_history = convert_chat_history(chat_history or [])
    has_history = bool(lc_history)

    # --- Phase 1: Retrieval ---
    if has_history:
        # Use history-aware retriever to rephrase follow-up into standalone query
        ha_retriever = build_history_aware_retriever(retriever, llm)
        try:
            source_docs: List[Document] = ha_retriever.invoke(
                {"input": query, "chat_history": lc_history}
            )
        except Exception:
            source_docs = []
        context_str = format_docs(source_docs)
    else:
        # Fresh query — use the fast direct retriever path from Story 4.1
        context_str, source_docs = retrieve_context(query, retriever)

    # If no context was found, return a pre-canned no-context stream immediately.
    if context_str == NO_CONTEXT_SENTINEL:
        def _no_context_stream():
            yield (
                "I could not find relevant information in the Intershop "
                "Knowledge Base for this query. Please try rephrasing your "
                "question or check the official documentation directly."
            )
        return _no_context_stream(), []

    # --- Phase 2: Streaming Generation with History ---
    generation_chain = GROUNDED_PROMPT | llm | StrOutputParser()

    stream = generation_chain.stream(
        {
            "context": context_str,
            "question": query,
            "chat_history": lc_history,
        }
    )

    return stream, source_docs
