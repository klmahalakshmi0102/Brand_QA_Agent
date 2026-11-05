#DOCUMENT LOADING

import httpx
import trafilatura

from app.models import DocumentInput

async def load_document(document_input: DocumentInput) -> str:
    # case 1: If raw text is provided
    if document_input.text:
        text = document_input.text.strip()
        if not text:
            raise ValueError("The supplied document text is empty.")
        return text

    # case 2: If a URL is provided
    if document_input.url:
        url = str(document_input.url)

        try:
            async with httpx.AsyncClient(
                timeout=20.0,
                follow_redirects=True,
            ) as client:
                response = await client.get(url)
                response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise TimeoutError(
                f"Request timed out while accessing {url}"
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise ValueError(
                f"URL returned HTTP {exc.response.status_code}: {url}"
            ) from exc
        except httpx.RequestError as exc:
            raise ConnectionError(
                f"Could not connect to URL: {url}"
            ) from exc

        # Extract readable text from HTML
        text_content = trafilatura.extract(response.text)

        if not text_content or not text_content.strip():
            raise ValueError(
                f"Failed to extract readable text from {url}"
            )

        return text_content.strip()

    raise ValueError("No valid text or URL provided in the document input.")

    