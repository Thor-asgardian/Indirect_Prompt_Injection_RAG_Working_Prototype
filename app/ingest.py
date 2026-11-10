
from pathlib import Path
from app.vector_store import VectorStore

def main():

    store = VectorStore()

    data_folder = Path("data")

    for file in data_folder.glob("*.txt"):

        text = file.read_text(encoding="utf-8")

        store.add_document(
            doc_id=file.stem,
            text=text,
            source=file.name
        )

        print(f"Indexed: {file.name}")

    print("\nDocument ingestion completed!")
    print("Total documents:", store.collection.count())

if __name__ == "__main__":
    main()
