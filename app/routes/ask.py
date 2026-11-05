
import logging

from fastapi import APIRouter, HTTPException

from app.models import AskRequest, AskResponse
from app.graph.graph import brand_qa_graph

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/tenants/{tenant_id}/ask",
    response_model=AskResponse
)
async def ask_question(
    tenant_id: str,
    request: AskRequest
):
    try:
        initial_state = {
            "tenant_id": tenant_id,
            "question": request.question,
            "search_query": request.question,
            "retrieved_docs": [],
            "relevant_docs": [],
            "retry_count": 0,
            "answer": "",
            "found_in_corpus": False,
            "citations": [],
            "trace": []
        }

        result = await brand_qa_graph.ainvoke(initial_state)

        return {
            "answer": result["answer"],
            "found_in_corpus": result["found_in_corpus"],
            "citations": result["citations"],
            "trace": result["trace"]
        }

    except Exception:
        logger.exception("Question answering failed")
        raise HTTPException(
            status_code=500,
            detail="Question answering failed. Check application logs."
        )
