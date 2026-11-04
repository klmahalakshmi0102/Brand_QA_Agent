#Test file to check if Pinecone connection is successful
from app.services.vector_store import index

stats  = index.describe_index_stats()

print("Pinecone Connection Successful")
print("Index Stats:", stats)