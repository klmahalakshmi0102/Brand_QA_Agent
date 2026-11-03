#DOCUMENT LOADING

import httpx
import trafilatura

from app.models import DocumentInput

async def load_document(document_input: DocumentInput) -> str:
    
    #case 1: If raw text is provided
    if document_input.text:
        return document_input.text
    
    #case 2: If a URL is provided
    if document_input.url:
        async with httpx.AsyncClient(
            timeout=20,
            follow_redirects=True
        ) as client:
            response = await client.get(str(document_input.url))
            response.raise_for_status()
            # html_content = response.text
            text_content = trafilatura.extract(response.text)
            if not text_content:
                raise ValueError(f"Failed to extract text from the {document_input.url}.")
            return text_content
        raise ValueError("No valid text or URL provided in the document input.")
    