# import os
# from dotenv import load_dotenv
# from pinecone import Pinecone, ServerlessSpec

# # Load API key and index name from .env
# load_dotenv()

# api_key = os.getenv("PINECONE_API_KEY")
# index_name = "brand-qa-vector-index"

# if not api_key:
#     raise ValueError("PINECONE_API_KEY is missing from .env")

# # Connect to Pinecone
# pc = Pinecone(api_key=api_key)

# # Check whether the index already exists
# existing_indexes = pc.list_indexes().names()

# if index_name in existing_indexes:
#     print(f"Index '{index_name}' already exists.")
# else:
#     print("Creating vector index...")

#     pc.create_index(
#         name=index_name,
#         dimension=384,
#         metric="cosine",
#         spec=ServerlessSpec(
#             cloud="aws",
#             region="us-east-1"
#         )
#     )

#     print("Index creation request submitted.")

# # Verify the index
# description = pc.describe_index(index_name)

# print("Index details:")
# print("Name:", description.name)
# print("Dimension:", description.dimension)
# print("Metric:", description.metric)
# print("Status:", description.status)


import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")

if not api_key:
    raise ValueError("PINECONE_API_KEY is missing from .env")

pc = Pinecone(api_key=api_key)

index_name = "brand-qa-vectors-384"

print("Creating a fresh vector index...")

pc.create_index(
    name=index_name,
    dimension=384,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

print("Index created successfully!")

description = pc.describe_index(index_name)

print("Name:", description.name)
print("Dimension:", description.dimension)
print("Metric:", description.metric)
print("Status:", description.status)