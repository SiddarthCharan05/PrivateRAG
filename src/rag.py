from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM

from access_control import get_allowed_departments
from privacy_scanner import scan_for_pii, calculate_risk
from audit_logger import log_interaction

CHROMA_DIR = "chroma_db"

EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

LLM_MODEL = "llama3.2:3b"


def load_vector_store():
    """Load the existing NordWerk vector database."""

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
        collection_name="nordwerk_knowledge",
    )


def retrieve_authorized_context(
    vector_store,
    question,
    role,
):
    """Retrieve only documents the employee role can access."""

    allowed_departments = get_allowed_departments(role)

    print(
        "\nAuthorised knowledge domains:",
        ", ".join(allowed_departments),
    )

    results = vector_store.similarity_search(
        question,
        k=8,
        filter={
            "department": {
                "$in": allowed_departments
            }
        },
    )

    return results


def generate_answer(
    question,
    documents,
):
    """Generate a grounded answer using authorised context only."""

    llm = OllamaLLM(
        model=LLM_MODEL,
        temperature=0,
    )

    context = "\n\n".join(
        [
            (
                f"SOURCE: {doc.metadata['source']}\n"
                f"DEPARTMENT: "
                f"{doc.metadata['department']}\n"
                f"CONTENT:\n"
                f"{doc.page_content}"
            )
            for doc in documents
        ]
    )

    prompt = f"""
You are PrivateRAG, the internal AI assistant
for NordWerk Solutions GmbH.

Answer using ONLY the authorised company context
provided below.

SECURITY RULES:

1. Never use outside knowledge.
2. Never invent NordWerk information.
3. Do not infer confidential information.
4. If the available context does not contain the
   answer, respond exactly:

   "I cannot answer this from the company information
   available to your role."

5. Do not invent page numbers or section numbers.
6. Keep your response concise and professional.

AUTHORISED CONTEXT:

{context}

EMPLOYEE QUESTION:

{question}

ANSWER:
"""

    return llm.invoke(prompt)


def ask_privaterag(
    question,
    role,
):
    """Run privacy scanning, access control, retrieval and generation."""

    # -------------------------------------------------
    # STEP 1: PRIVACY SCAN
    # -------------------------------------------------

    pii_entities = scan_for_pii(question)
    privacy_risk = calculate_risk(pii_entities)

    print("\nPrivacy Risk:", privacy_risk)

    if pii_entities:
        print("PII detected:")

        for entity in pii_entities:
            print(
                f"- {entity['type']} "
                f"(confidence: {entity['score']})"
            )

    else:
        print("PII detected: None")

    # -------------------------------------------------
    # STEP 2: LOAD VECTOR DATABASE
    # -------------------------------------------------

    vector_store = load_vector_store()

    # -------------------------------------------------
    # STEP 3: ROLE-BASED RETRIEVAL
    # -------------------------------------------------

    documents = retrieve_authorized_context(
        vector_store,
        question,
        role,
    )

    # -------------------------------------------------
    # STEP 4: LOCAL LLM GENERATION
    # -------------------------------------------------

    answer = generate_answer(
        question,
        documents,
    )
    # Record privacy-safe audit metadata
    log_interaction(
        role=role,
        privacy_risk=privacy_risk,
        pii_entities=pii_entities,
        documents=documents,
    )
    # -------------------------------------------------
    # STEP 5: DISPLAY RESULT
    # -------------------------------------------------

    print("\n" + "=" * 65)
    print("PRIVATE RAG - NORDWERK SOLUTIONS GMBH")
    print("=" * 65)

    print(f"\nEmployee role: {role.upper()}")

    print(f"\nPrivacy Risk: {privacy_risk}")

    print(f"\nQuestion:\n{question}")

    print("\nAnswer:")
    print(answer)

    print("\nAuthorised sources used:")

    if documents:

        sources = set()

        for document in documents:

            source = (
                document.metadata["source"],
                document.metadata["department"],
            )

            sources.add(source)

        for source, department in sources:

            print(
                f"- {source} [{department}]"
            )

    else:

        print("- No authorised source retrieved")

    print("\n" + "=" * 65)

    return {
        "answer": answer,
        "privacy_risk": privacy_risk,
        "pii_entities": pii_entities,
        "documents": documents,
    }


if __name__ == "__main__":

    print("\nPRIVATE RAG")
    print("NordWerk Solutions GmbH\n")

    print("Available roles:")
    print("1 - General Employee")
    print("2 - IT")
    print("3 - HR")
    print("4 - Finance")

    role_selection = input(
        "\nSelect your role: "
    )

    roles = {
        "1": "general",
        "2": "it",
        "3": "hr",
        "4": "finance",
    }

    role = roles.get(
        role_selection,
        "general",
    )

    question = input(
        "\nAsk PrivateRAG:\n> "
    )

    ask_privaterag(
        question,
        role,
    )