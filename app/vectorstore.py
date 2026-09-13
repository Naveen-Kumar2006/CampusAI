from pathlib import Path

from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

from app.ingestion import load_documents, split_documents


# ==========================================
# Configuration
# ==========================================

VECTORSTORE_DIR = Path("data/vectorstore")


# ==========================================
# Ollama Embeddings
# ==========================================

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# ==========================================
# Create Vector Store
# ==========================================

def create_vectorstore():
    """
    Load PDFs, split them into chunks,
    create embeddings and save the FAISS index.
    """

    print("Loading PDF documents...")

    documents = load_documents()

    if not documents:

        print("No PDF documents found.")

        return False

    print(
        f"Loaded {len(documents)} document pages."
    )

    print("Splitting documents into chunks...")

    chunks = split_documents(documents)

    print(
        f"Created {len(chunks)} chunks."
    )

    print("Creating embeddings with Ollama...")

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    VECTORSTORE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    vectorstore.save_local(
        str(VECTORSTORE_DIR)
    )

    print(
        f"Vector store saved to {VECTORSTORE_DIR}"
    )

    print(
        f"Vector store created with "
        f"{len(chunks)} chunks."
    )

    return True


# ==========================================
# Run Directly
# ==========================================

if __name__ == "__main__":

    create_vectorstore()