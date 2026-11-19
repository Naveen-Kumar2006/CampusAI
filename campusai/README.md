# CampusAI College Portal

A complete college website with a React frontend, FastAPI backend, and a RAG-powered AI chatbot that answers questions from college PDF documents.

## Architecture

- **Frontend**: React + Vite + Tailwind CSS + React Router
- **Backend**: FastAPI + SQLAlchemy + SQLite
- **AI Chatbot**: LangChain RAG pipeline with FAISS vector search
- **LLM**: Ollama — Qwen3 8B (`qwen3:8b-q4_K_M`)
- **Embeddings**: Ollama — Nomic Embed Text (`nomic-embed-text`)

## Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **Ollama** — [Install Ollama](https://ollama.com/download)

## Getting Started

### 1. Ollama Setup

Start the Ollama server and pull the required models:

```bash
# Start Ollama (if not already running)
ollama serve

# Pull the LLM model
ollama pull qwen3:8b-q4_K_M

# Pull the embedding model
ollama pull nomic-embed-text
```

Verify the models are available:

```bash
ollama list
```

You should see both `qwen3:8b-q4_K_M` and `nomic-embed-text` in the output.

### 2. Backend Setup

```bash
cd campusai/backend

# Create and activate virtual environment
python -m venv venv

# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Seed the database (first time only)
python seed.py

# Ingest documents into FAISS (first time only, or after adding new PDFs)
python test_ingestion.py

# Run the API server
uvicorn app.main:app --reload
```

The API will run on `http://localhost:8000`. View the API docs at `http://localhost:8000/docs`.

### 3. Frontend Setup

```bash
cd campusai/frontend
npm install
npm run dev
```

The frontend will run on `http://localhost:5173`.

## RAG Pipeline

The chatbot uses Retrieval-Augmented Generation to answer questions:

1. **Document Ingestion** — PDFs in `backend/data/documents/` are loaded and split into chunks using `RecursiveCharacterTextSplitter`.
2. **Embedding** — Each chunk is embedded using Ollama's `nomic-embed-text` model.
3. **Vector Storage** — Embeddings are stored in a FAISS index at `backend/data/vectorstore/`.
4. **Query** — When a student asks a question, the most relevant chunks are retrieved via similarity search.
5. **Answer Generation** — The retrieved context and question are sent to Qwen3 8B via Ollama to generate a grounded answer.

## Project Structure

```
campusai/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── database.py          # SQLAlchemy database setup
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   └── services/
│   │       ├── chat_service.py       # RAG chat orchestration
│   │       ├── document_service.py   # PDF loading & text splitting
│   │       ├── embedding_service.py  # Ollama embeddings
│   │       ├── llm_service.py        # Ollama LLM (Qwen3)
│   │       └── vector_service.py     # FAISS vector store
│   ├── data/
│   │   ├── documents/           # Source PDFs (college_rules.pdf)
│   │   └── vectorstore/         # FAISS index files
│   ├── requirements.txt
│   ├── seed.py                  # Database seeder
│   └── campusai.db              # SQLite database
├── frontend/
│   ├── src/
│   │   ├── App.tsx              # Main React application
│   │   ├── main.tsx             # Entry point
│   │   └── index.css            # Global styles (Tailwind)
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
└── README.md
```
