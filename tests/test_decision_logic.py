
from app.graph.graph import route_after_grading


def test_decision_logic():
    """Verify answer, retry, and not-found decisions."""

    # Case 1: Relevant documents found -> answer
    relevant_state = {
        "relevant_docs": ["Relevant Asana document"],
        "retry_count": 0
    }

    assert route_after_grading(relevant_state) == "answer"

    # Case 2: No relevant documents yet -> retry
    irrelevant_state = {
        "relevant_docs": [],
        "retry_count": 0
    }

    assert route_after_grading(irrelevant_state) == "rewrite"

    # Case 3: Still irrelevant after retry -> not found
    retry_state = {
        "relevant_docs": [],
        "retry_count": 1
    }

    assert route_after_grading(retry_state) == "not_found"
