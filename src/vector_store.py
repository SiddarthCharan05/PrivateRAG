from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from document_loader import load_documents, split_documents


CHROMA_DIR = Path("chroma_db")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def create_vector_store():
    """Create a persistent vector database from company documents."""

    print("\nLoading NordWerk company documents...")

    documents = load_documents()
    chunks = split_documents(documents)

    print(f"Loaded {len(documents)} documents.")
    print(f"Preparing {len(chunks)} searchable chunks.")

    print("\nLoading local embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    print("Creating local ChromaDB vector store...")

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name="nordwerk_knowledge",
    )

    print("\n✓ PrivateRAG knowledge base created successfully.")
    print(f"✓ Stored {len(chunks)} chunks.")
    print(f"✓ Database location: {CHROMA_DIR.resolve()}")

    return vector_store


if __name__ == "__main__":
    create_vector_store()