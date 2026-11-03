from fastapi import FastAPI
app = FastAPI(title = "Brand Q&A Agent")

@app.get("/health")
async def health():
    return {"status": "healthy"}