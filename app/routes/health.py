
from fastapi import APIRouter
from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY, GROQ_MODEL
from app.services.vector_store import index

router = APIRouter()


@router.get("/health")
async def health_check():
    # Check Pinecone connectivity
    vector_db_status = "unavailable"

    try:
        await __import__("asyncio").to_thread(
            index.describe_index_stats
        )
        vector_db_status = "reachable"
    except Exception:
        pass

    # Check Groq connectivity
    llm_status = "unavailable"

    try:
        if GROQ_API_KEY:
            llm = ChatGroq(
                model=GROQ_MODEL,
                temperature=0,
                api_key=GROQ_API_KEY
            )

            await llm.ainvoke("Reply with OK.")
            llm_status = "reachable"
    except Exception:
        pass

    return {
        "status": (
            "healthy"
            if vector_db_status == "reachable"
            and llm_status == "reachable"
            else "degraded"
        ),
        "vector_database": vector_db_status,
        "llm_provider": llm_status
    }
