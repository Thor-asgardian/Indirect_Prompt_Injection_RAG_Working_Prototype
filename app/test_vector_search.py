
from app.vector_store import VectorStore

store = VectorStore()

question = "How many days do I have to get my money back?"

results = store.search(question, top_k=3)

print("\nQUESTION:", question)
print("\nRETRIEVED DOCUMENTS:\n")

for document, metadata, distance in zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0]
):
    print("Source:", metadata["source"])
    print("Distance:", round(distance, 4))
    print("Content:", document)
    print("-" * 60)
