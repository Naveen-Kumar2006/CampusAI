from pathlib import Path

from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

from ingestion import load_documents, split_documents


VECTORSTORE_DIR = Path("data/vectorstore")


embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


def create_vectorstore():
    documents = load_documents()

    if not documents:
        print("No documents found.")
        return

    chunks = split_documents(documents)

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    vectorstore.save_local(str(VECTORSTORE_DIR))

    print(f"Vector store created with {len(chunks)} chunks.")


if __name__ == "__main__":
    create_vectorstore()