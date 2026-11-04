#combines document loading, chunking, hashing, embedding, and Pinecone storage

import hashlib
from langchain_core.documents import Document
from app.services.document_loader import load_document
from app.services.chunking import split_document
from app.services.vector_store import get_vector_store,index

def generate_doc_id(document, text:str)->str:
    #Generate a Stable ID using the URL or document
    
    if document.url:
        unique_content = str(document.url) + text
    else:
        unique_content = text
    return hashlib.sha256(unique_content.encode('utf-8')).hexdigest()

async def ingest_documents(tenant_id: str,documents: list):
    vector_store = get_vector_store(tenant_id)
    document_stored = 0
    chunks_stored = 0
    processed_doc_ids = set()
    for document in documents:
        #Step 1: Extract document content
        text = await load_document(document)
        if not text.strip():
            #print(f"Document {document} has no text content. Skipping.")
            continue
        
        #Step 2: Generate Stable ID for the document
        doc_id = generate_doc_id(document, text)
        
        #Avoid processing the same document multiple times
        if doc_id in processed_doc_ids:
            #print(f"Document {document} has already been processed. Skipping.")
            continue
        
        processed_doc_ids.add(doc_id)
        
        #step 3: Split the document into chunks
        chunks = split_document(text)
        if not chunks:
            #print(f"Document {document} could not be split into chunks. Skipping.")
            continue
        
        #step 4: Remove previous chunks of this document
        #this also removes stale chunks if the document becomes shorter
        # index.delete(filter={"doc_id": doc_id, "namespace": tenant_id})
        stats = index.describe_index_stats()
        existing_namespaces = stats.namespaces or {}
        if (
            tenant_id in existing_namespaces
            and existing_namespaces[tenant_id].vector_count > 0
        ):
            # Delete previous chunks belonging to this document
            index.delete(
                filter={
                    "doc_id": {"$eq": doc_id}
                },
                namespace=tenant_id
            )
        
        #step 5: Create langchain documents with metadata
        langchain_docs = []
        chunk_ids = []
        source = document.source or str(document.url) if document.url else "manual"
        for chunk_index, chunk_text in enumerate(chunks):
            metadata = {
                "tenant_id": tenant_id,
                "doc_id": doc_id,
                "chunk_index": chunk_index,
                "source": source
            }
            langchain_docs.append(Document(page_content=chunk_text, metadata=metadata))
            chunk_ids.append(f"{doc_id}_{chunk_index}")
            
        #step 6: generate embeddings and store in Pinecone
        vector_store.add_documents(documents = langchain_docs, ids=chunk_ids)
        document_stored += 1
        chunks_stored += len(chunks)
    return {
            "documents_stored": document_stored,
            "chunks_stored": chunks_stored
        }
    
    