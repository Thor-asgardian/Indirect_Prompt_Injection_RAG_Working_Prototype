
import chromadb
import requests
from pathlib import Path

OLLAMA_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"

class VectorStore:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="rag_security_documents",
            metadata={"hnsw:space": "cosine"}
        )

    def get_embedding(self, text):

        response = requests.post(
            f"{OLLAMA_URL}/api/embed",
            json={
                "model": EMBED_MODEL,
                "input": text
            },
            timeout=120
        )

        response.raise_for_status()

        return response.json()["embeddings"][0]

    def add_document(self, doc_id, text, source):

        embedding = self.get_embedding(text)

        self.collection.upsert(
            ids=[doc_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[{"source": source}]
        )

    def search(self, query, top_k=4):

        embedding = self.get_embedding(query)

        return self.collection.query(
            query_embeddings=[embedding],
            n_results=min(
                top_k,
                self.collection.count()
            )
        )
