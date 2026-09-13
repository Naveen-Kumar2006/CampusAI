from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel

from app.ingestion import load_documents, split_documents
from app.vectorstore import embeddings, VECTORSTORE_DIR
from app.chatbot import ask_campus_ai

from langchain_community.vectorstores import FAISS


# ==========================================
# Configuration
# ==========================================

UPLOAD_DIR = Path("data/uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

VECTORSTORE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# FastAPI Application
# ==========================================

app = FastAPI(
    title="CampusAI API",
    description="RAG backend for the CampusAI college assistant",
    version="1.0.0"
)


# ==========================================
# Request Schema
# ==========================================

class ChatRequest(BaseModel):
    question: str


# ==========================================
# Root Endpoint
# ==========================================

@app.get("/")
def root():

    return {
        "message": "CampusAI API is running",
        "status": "success"
    }


# ==========================================
# Health Check
# ==========================================

@app.get("/api/health")
def health_check():

    return {
        "status": "healthy"
    }


# ==========================================
# Admin - Upload PDF
# ==========================================

@app.post("/api/admin/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    # --------------------------------------
    # Validate File Type
    # --------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )


    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )


    # --------------------------------------
    # Save File
    # --------------------------------------

    file_path = (
        UPLOAD_DIR /
        Path(file.filename).name
    )


    try:

        contents = await file.read()

        with open(
            file_path,
            "wb"
        ) as output_file:

            output_file.write(
                contents
            )


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to save PDF: {error}"
        )


    return {

        "message":
            "PDF uploaded successfully",

        "filename":
            file_path.name,

        "path":
            str(file_path)
    }


# ==========================================
# Admin - Process Documents
# ==========================================

@app.post("/api/admin/process")
def process_documents():

    try:

        # ----------------------------------
        # Load PDFs
        # ----------------------------------

        documents = load_documents()


        if not documents:

            raise HTTPException(
                status_code=404,
                detail="No PDF documents found."
            )


        # ----------------------------------
        # Split Documents
        # ----------------------------------

        chunks = split_documents(
            documents
        )


        if not chunks:

            raise HTTPException(
                status_code=400,
                detail="No text chunks were created."
            )


        # ----------------------------------
        # Create FAISS
        # ----------------------------------

        vectorstore = FAISS.from_documents(
            chunks,
            embeddings
        )


        # ----------------------------------
        # Save FAISS
        # ----------------------------------

        vectorstore.save_local(
            str(VECTORSTORE_DIR)
        )


        return {

            "message":
                "Documents processed successfully",

            "documents":
                len(documents),

            "chunks":
                len(chunks)
        }


    except HTTPException:

        raise


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {error}"
        )


# ==========================================
# Admin - List PDFs
# ==========================================

@app.get("/api/admin/documents")
def list_documents():

    pdf_files = list(
        UPLOAD_DIR.glob("*.pdf")
    )


    documents = []

    for pdf_file in pdf_files:

        documents.append({

            "filename":
                pdf_file.name,

            "size_bytes":
                pdf_file.stat().st_size
        })


    return {

        "count":
            len(documents),

        "documents":
            documents
    }


# ==========================================
# Student - Chat
# ==========================================

@app.post("/api/chat")
def chat(
    request: ChatRequest
):

    question = request.question.strip()


    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )


    # --------------------------------------
    # Check Vector Store
    # --------------------------------------

    index_file = (
        VECTORSTORE_DIR /
        "index.faiss"
    )


    if not index_file.exists():

        raise HTTPException(
            status_code=400,
            detail=(
                "Knowledge base is not ready. "
                "Please process documents first."
            )
        )


    # --------------------------------------
    # RAG
    # --------------------------------------

    try:

        answer, docs = ask_campus_ai(
            question
        )


        # ------------------------------
        # Build Sources
        # ------------------------------

        sources = []

        displayed_sources = set()


        for doc in docs:

            source = Path(
                doc.metadata.get(
                    "source",
                    "Unknown"
                )
            ).name


            page = (
                doc.metadata.get(
                    "page",
                    0
                ) + 1
            )


            source_key = (
                source,
                page
            )


            if source_key not in displayed_sources:

                displayed_sources.add(
                    source_key
                )


                sources.append({

                    "file":
                        source,

                    "page":
                        page
                })


        return {

            "question":
                question,

            "answer":
                answer,

            "sources":
                sources
        }


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"RAG processing failed: {error}"
        )