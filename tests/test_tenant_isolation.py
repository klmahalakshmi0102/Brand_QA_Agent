
from types import SimpleNamespace

from app.graph import nodes


def test_tenant_isolation(monkeypatch):
    """Tenant B must not retrieve Tenant A's documents."""

    documents = {
        "tenant_a": [
            SimpleNamespace(
                page_content="Asana is a project management tool.",
                metadata={"tenant_id": "tenant_a"}
            )
        ],
        "tenant_b": [
            SimpleNamespace(
                page_content="Trello uses boards and cards.",
                metadata={"tenant_id": "tenant_b"}
            )
        ]
    }

    class FakeVectorStore:
        def __init__(self, tenant_id):
            self.tenant_id = tenant_id

        def similarity_search(self, query, k=5):
            return documents[self.tenant_id][:k]

    requested_tenants = []

    def fake_get_vector_store(tenant_id):
        requested_tenants.append(tenant_id)
        return FakeVectorStore(tenant_id)

    # Replace real Pinecone vector store with fake store
    monkeypatch.setattr(
        nodes,
        "get_vector_store",
        fake_get_vector_store
    )

    # Tenant B asks a question
    state = {
        "tenant_id": "tenant_b",
        "question": "What is Trello?",
        "search_query": "What is Trello?"
    }

    result = nodes.retrieve_node(state)
    retrieved_docs = result["retrieved_docs"]

    # Verify retrieval used Tenant B's namespace
    assert requested_tenants == ["tenant_b"]

    # Verify only Tenant B's documents were retrieved
    assert len(retrieved_docs) == 1
    assert retrieved_docs[0].metadata["tenant_id"] == "tenant_b"
    assert "Trello" in retrieved_docs[0].page_content
    assert "Asana" not in retrieved_docs[0].page_content
