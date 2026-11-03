from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class DocumentInput(BaseModel):
    
    url: Optional[HttpUrl] = None
    text: Optional[str] = None
    source: Optional[str] = None
    brand : str
    
    
class IngestRequest(BaseModel):
    documents: List[DocumentInput]
    
class IngestResponse(BaseModel):
    document_stored: str
    chunks_stored: int