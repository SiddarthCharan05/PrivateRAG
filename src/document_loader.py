from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


DATA_DIR = Path("data")


def load_documents():
    """Load all text documents from the company knowledge base."""

    documents = []

    for file_path in DATA_DIR.rglob("*.txt"):

        department = file_path.parent.name

        text = file_path.read_text(encoding="utf-8")

        document = Document(
            page_content=text,
            metadata={
                "source": file_path.name,
                "department": department,
                "file_path": str(file_path),
            },
        )

        documents.append(document)

    return documents


def split_documents(documents):
    """Split documents into smaller chunks for semantic retrieval."""

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
    )

    return text_splitter.split_documents(documents)


if __name__ == "__main__":

    documents = load_documents()

    print(f"\nLoaded {len(documents)} company documents.")

    chunks = split_documents(documents)

    print(f"Created {len(chunks)} searchable chunks.\n")

    for number, chunk in enumerate(chunks[:5], start=1):

        print("=" * 60)
        print(f"CHUNK {number}")
        print(f"Source: {chunk.metadata['source']}")
        print(f"Department: {chunk.metadata['department']}")
        print("-" * 60)
        print(chunk.page_content[:300])
        print()