
from langgraph.graph import StateGraph, START, END

from app.graph.state import BrandQAState
from app.graph.nodes import (
    retrieve_node,
    rewrite_node,
    answer_node,
    not_found_node
)
from app.graph.grading import grade_node


def route_after_grading(state: BrandQAState) -> str:
    """Decide the next graph step after relevance grading."""

    if state.get("relevant_docs"):
        return "answer"

    if state.get("retry_count", 0) < 1:
        return "rewrite"

    return "not_found"


def build_graph():
    workflow = StateGraph(BrandQAState)

    # Register graph nodes
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("grade", grade_node)
    workflow.add_node("rewrite", rewrite_node)
    workflow.add_node("answer", answer_node)
    workflow.add_node("not_found", not_found_node)

    # Define graph edges
    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "grade")

    workflow.add_conditional_edges(
        "grade",
        route_after_grading,
        {
            "answer": "answer",
            "rewrite": "rewrite",
            "not_found": "not_found"
        }
    )

    workflow.add_edge("rewrite", "retrieve")
    workflow.add_edge("answer", END)
    workflow.add_edge("not_found", END)

    return workflow.compile()


brand_qa_graph = build_graph()
