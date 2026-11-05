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
    documents_stored: int
    chunks_stored: int
    

class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    found_in_corpus: bool
    citations: list[dict]
    trace: list[str]
