from fastapi import FastAPI
from app.routes.ingest import router as ingest_router

from app.routes.ask import router as ask_router

app = FastAPI(title = "Brand Q&A Agent",
              description = "Multi-tenant RAG application",
              version = "1.0.0")

app.include_router(ingest_router)
app.include_router(ask_router)


@app.get("/health")
async def health():
    # return {"status": "healthy"}
    return{"message": "Brand Q&A Agent is running successfully."}