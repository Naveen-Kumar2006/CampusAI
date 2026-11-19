# 🎓 CampusAI

CampusAI is an AI-powered college assistant that uses **RAG (Retrieval-Augmented Generation)** to answer student queries from uploaded college documents.

## 🚀 Features

- 🤖 AI-powered college chatbot (RAG)
- 📚 PDF document-based Q&A
- 🔎 FAISS vector search
- 🧠 Ollama LLM (Qwen3 8B)
- 📐 Nomic Embeddings (nomic-embed-text)
- ⚡ FastAPI backend
- 🌐 React + Vite frontend

## 🛠️ Tech Stack

Python • FastAPI • LangChain • FAISS • Ollama (Qwen3 8B) • Nomic Embeddings • React • Vite • Tailwind CSS • SQLite

## 🔄 Workflow

```text
Student Question
       ↓
React Frontend
       ↓
FastAPI Backend
       ↓
FAISS Vector Search (RAG)
       ↓
Ollama (Qwen3 8B)
       ↓
Answer
```

See [campusai/README.md](campusai/README.md) for full setup instructions.
