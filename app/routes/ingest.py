# from fastapi import APIRouter,HTTPException
# from app.models import IngestRequest, IngestResponse
# from app.services.ingestion import ingest_documents

# router = APIRouter()

# @router.post("/tenants/{tenant_id}/ingest",
#              response_model=IngestResponse)
# async def ingest(
#     tenant_id: str,
#     request: IngestRequest):
#     try:
#         result = await ingest_documents(tenant_id, request.documents)
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Document ingestion failed: {str(e)}")

import logging

from fastapi import APIRouter, HTTPException

from app.models import IngestRequest, IngestResponse
from app.services.ingestion import ingest_documents

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post(
    "/tenants/{tenant_id}/ingest",
    response_model=IngestResponse
)
async def ingest(tenant_id: str, request: IngestRequest):

    try:
        result = await ingest_documents(
            tenant_id=tenant_id,
            documents=request.documents
        )

        return result

    except Exception as e:

        logger.exception("Document ingestion failed")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )