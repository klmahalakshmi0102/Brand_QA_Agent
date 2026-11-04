#Connect to Pinecone and create a vector store using the specified index and embeddings
#Connects Python application to Pinecone Index

from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

from app.config import PINECONE_API_KEY, PINECONE_INDEX_NAME

from app.services.embeddings import embeddings

pc = Pinecone(api_key=PINECONE_API_KEY)

index = pc.Index(PINECONE_INDEX_NAME)

def get_vector_store(tenant_id:str):
    return PineconeVectorStore(index=index, embedding=embeddings, namespace=tenant_id)




