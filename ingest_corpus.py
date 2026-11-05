
import asyncio
from pathlib import Path

from app.models import DocumentInput
from app.services.ingestion import ingest_documents


DATA_DIR = Path(__file__).resolve().parent / "data"
TENANT_ID = "acme"


async def main():
    documents = []

    # Find every text file in the data folder
    text_files = sorted(DATA_DIR.glob("*.txt"))

    if not text_files:
        print("No .txt files found in the data folder.")
        return

    print(f"Found {len(text_files)} text files.")

    for file_path in text_files:
        text = file_path.read_text(encoding="utf-8").strip()

        if not text:
            print(f"Skipping empty file: {file_path.name}")
            continue

        # Extract the source URL from the file, if present
        source_url = next(
            (
                line.split(":", 1)[1].strip()
                for line in text.splitlines()
                if line.lower().startswith("source url:")
            ),
            ""
        )

        documents.append(
            DocumentInput(
                text=text,
                brand="Project Management",
                source=f"{file_path.name} | {source_url}"
            )
        )

    if not documents:
        print("No documents with usable text were found.")
        return

    # Send all documents through the existing ingestion pipeline
    result = await ingest_documents(
        tenant_id=TENANT_ID,
        documents=documents
    )

    print("\nIngestion completed!")
    print(f"Tenant: {TENANT_ID}")
    print(f"Documents stored: {result['documents_stored']}")
    print(f"Chunks stored: {result['chunks_stored']}")


if __name__ == "__main__":
    asyncio.run(main())
