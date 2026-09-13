from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ==========================================
# Configuration
# ==========================================

UPLOAD_DIR = Path("data/uploads")


# ==========================================
# Load PDF Documents
# ==========================================

def load_documents():
    """
    Load all PDF files from the uploads directory.

    Returns:
        list: List of LangChain Document objects.
    """

    documents = []

    for pdf_file in UPLOAD_DIR.glob("*.pdf"):

        try:

            loader = PyPDFLoader(str(pdf_file))

            pdf_documents = loader.load()

            documents.extend(pdf_documents)

            print(
                f"Loaded {pdf_file.name} "
                f"({len(pdf_documents)} pages)"
            )

        except Exception as error:

            print(
                f"Failed to load {pdf_file.name}: {error}"
            )

    return documents


# ==========================================
# Split Documents into Chunks
# ==========================================

def split_documents(documents):
    """
    Split documents into smaller chunks for RAG.

    Args:
        documents: List of LangChain Document objects.

    Returns:
        list: List of document chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    return chunks