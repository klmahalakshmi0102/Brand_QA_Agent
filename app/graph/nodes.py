
from app.graph.state import BrandQAState
from app.services.vector_store import get_vector_store


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

