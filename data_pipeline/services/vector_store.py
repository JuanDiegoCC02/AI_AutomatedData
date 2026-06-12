# data_pipeline/services/vector_store.py

import chromadb

client = chromadb.PersistentClient(
    path="./vector_db"
)

collection = client.get_or_create_collection(
    name="documents"
)