
from typing import TypedDict, List, Any


class BrandQAState(TypedDict):
    # User input
    tenant_id: str
    question: str

    # Search and retrieval
    search_query: str
    retrieved_docs: List[Any]
    relevant_docs: List[Any]

    # Retry control
    retry_count: int

    # Final response
    answer: str
    found_in_corpus: bool
    citations: List[dict]

    # Execution history
    trace: List[str]
