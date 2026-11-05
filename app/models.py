from pydantic import BaseModel, HttpUrl, model_validator
from typing import List, Optional

class DocumentInput(BaseModel):
    
    url: Optional[HttpUrl] = None
    text: Optional[str] = None
    source: Optional[str] = None
    brand : list[str]
    
    @model_validator(mode="after")
    def validate_document_content(self):
        if bool(self.url) == bool(self.text):
            raise ValueError(
                "Provide exactly one of url or text."
            )
        return self
    
    
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
