# CampusAI College Portal

A complete dummy college website with a React frontend and FastAPI backend. It features a cleanly separated placeholder for a RAG chatbot integration.

## Architecture

- **Frontend**: React + Vite + Tailwind CSS + React Router
- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Chatbot Placeholder**: `/api/chat` POST endpoint that points to `services/chat_service.py`.

## Getting Started

### 1. Backend Setup

```bash
cd campusai/backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt

# Seed the database
python seed.py

# Run the API server
uvicorn app.main:app --reload
```
The API will run on `http://localhost:8000`. You can view the docs at `http://localhost:8000/docs`.

### 2. Frontend Setup

```bash
cd campusai/frontend
npm install
npm run dev
```
The frontend will run on `http://localhost:5173`.

## Connecting Your RAG Implementation

Open `backend/app/services/chat_service.py`. You will see the placeholder function:

```python
async def ask_campus_ai(message: str):
    # PLACEHOLDER
    # You will replace this with your RAG implementation
    return {
        "answer": "CampusAI is currently connecting to the knowledge system.",
        "sources": []
    }
```
Replace the logic in this function to connect to your Chroma/Pinecone DB and your LLM. The frontend will automatically pick up the new responses since it connects through the `/api/chat` endpoint.
