from pathlib import Path

from langchain_community.vectorstores import FAISS

from .embedding_service import get_embeddings


VECTORSTORE_DIR = Path("data/vectorstore")


def create_vectorstore(chunks):

    embeddings = get_embeddings()

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

    return vectorstore


def load_vectorstore():

    embeddings = get_embeddings()

    vectorstore = FAISS.load_local(
        str(VECTORSTORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore