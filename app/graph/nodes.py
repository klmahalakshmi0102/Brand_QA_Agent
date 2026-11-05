
from app.graph.state import BrandQAState
from app.services.vector_store import get_vector_store

from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY, GROQ_MODEL
from app.graph.state import BrandQAState


llm = ChatGroq(
    model=GROQ_MODEL,
    temperature=0,
    api_key=GROQ_API_KEY
)


def retrieve_node(state: BrandQAState) -> dict:
    """
    Retrieve relevant document chunks from Pinecone
    using the tenant-specific namespace.
    """

    tenant_id = state["tenant_id"]
    search_query = state.get("search_query") or state["question"]
    #important
    vector_store = get_vector_store(tenant_id)

    retrieved_docs = vector_store.similarity_search(
        search_query,
        k=5
    )

    trace = state.get("trace", [])
    trace.append(
        f"Retrieved {len(retrieved_docs)} chunks from tenant '{tenant_id}'"
    )

    return {
        "search_query": search_query,
        "retrieved_docs": retrieved_docs,
        "trace": trace
    }


def rewrite_node(state: BrandQAState) -> dict:
    """Rewrite the question to improve document retrieval."""

    question = state["question"]

    prompt = f"""
    Rewrite this question to improve retrieval from a
    project-management knowledge base.

    Keep the original meaning. Use clear keywords.
    Return only the rewritten question.

    Question: {question}
    """

    response = llm.invoke(prompt)
    rewritten_query = response.content

    trace = list(state.get("trace", []))
    trace.append("Rewrote the search query for one retry.")

    return {
        "search_query": rewritten_query,
        "retry_count": state.get("retry_count", 0) + 1,
        "trace": trace
    }


def answer_node(state: BrandQAState) -> dict:
    """Generate an answer using relevant retrieved documents."""

    relevant_docs = state.get("relevant_docs", [])
    question = state["question"]

    context = "\n\n".join(
        doc.page_content for doc in relevant_docs
    )

    prompt = f"""
    You are a brand question-answering assistant.

    Answer the user's question using ONLY the supplied context.
    Do not use outside knowledge.
    If the context does not support a claim, do not invent it.

    Context:
    {context}

    Question:
    {question}

    Provide a clear and concise answer.
    """

    response = llm.invoke(prompt)

    citations = []
    for doc in relevant_docs:
        citations.append({
            "source": doc.metadata.get("source", "unknown"),
            "brand": doc.metadata.get("brand", "unknown"),
            "doc_id": doc.metadata.get("doc_id", ""),
            "chunk_index": doc.metadata.get("chunk_index", 0)
        })

    trace = list(state.get("trace", []))
    trace.append("Generated an answer using relevant documents.")

    return {
        "answer": response.content,
        "found_in_corpus": True,
        "citations": citations,
        "trace": trace
    }


def not_found_node(state: BrandQAState) -> dict:
    """Return a safe response when evidence is unavailable."""

    trace = list(state.get("trace", []))
    trace.append("No relevant evidence found after one retry.")

    return {
        "answer": (
            "I couldn't find sufficient information in the "
            "available knowledge base to answer this question."
        ),
        "found_in_corpus": False,
        "citations": [],
        "trace": trace
    }
