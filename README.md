# 🎓 CampusAI – AI-Powered College Assistant

An AI-powered college assistant that helps students get instant answers to college-related questions using **Retrieval-Augmented Generation (RAG)**.

CampusAI uses uploaded college documents as its knowledge source, allowing students to ask questions and receive context-aware answers through an AI chatbot.

<p align="center">
  <b>Built with FastAPI • React • LangChain • FAISS • Ollama</b>
</p>

---

## 🚀 Overview

Finding accurate information about college regulations, attendance policies, departments and academic guidelines can sometimes be difficult.

**CampusAI** addresses this problem by providing an AI-powered chatbot that retrieves relevant information from uploaded college documents and generates meaningful answers.

Instead of relying entirely on general AI knowledge, CampusAI uses a RAG pipeline to retrieve relevant document content before generating responses.

---

## ✨ Key Features

- 🤖 **AI-Powered Chatbot** – Ask college-related questions in natural language.
- 📄 **PDF Document Processing** – Upload college documents to build the knowledge base.
- 🔍 **Semantic Search** – Retrieve relevant information using vector embeddings.
- 🧠 **Retrieval-Augmented Generation** – Generate answers using retrieved document context.
- ⚡ **FastAPI Backend** – Handle API requests and AI processing.
- 💬 **Interactive Frontend** – Chat through a React-based user interface.
- 🏠 **Local LLM Integration** – Run Qwen3 using Ollama.

---

## 🏗️ System Architecture

```text
           Student
              |
              v
       React Frontend
              |
              v
       FastAPI Backend
              |
              v
       RAG Pipeline
              |
       +------+------+
       |             |
       v             v
  Embeddings     Document
  (Nomic)        Processing
       |             |
       +------+------+
              |
              v
       FAISS Vector Store
              |
              v
       Relevant Context
              |
              v
       Ollama (Qwen3)
              |
              v
       Generated Answer
              |
              v
          Student
```

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend | FastAPI |
| Frontend | React, Vite |
| Styling | Tailwind CSS |
| AI Framework | LangChain |
| LLM | Qwen3 8B |
| LLM Runtime | Ollama |
| Embedding Model | nomic-embed-text |
| Vector Database | FAISS |
| Database | SQLite |
| API Testing | Postman |
| Version Control | Git & GitHub |

---

## 🔄 How It Works

CampusAI follows a Retrieval-Augmented Generation workflow.

**1. Document Upload**

College-related PDF documents are uploaded to the application.

**2. Text Extraction and Chunking**

The documents are processed, and their content is divided into smaller text chunks.

**3. Embedding Generation**

Nomic Embeddings converts the text chunks into numerical vector representations.

**4. Vector Storage**

The generated embeddings are stored in FAISS for efficient similarity search.

**5. Question Processing**

When a student asks a question, the system converts it into an embedding and searches for relevant document chunks.

**6. Answer Generation**

The retrieved context is passed to the Qwen3 language model through Ollama to generate a relevant response.

---

## 📂 Project Structure

```text
CampusAI/
│
├── campusai/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   ├── chat.py
│   │   │   └── documents.py
│   │   │
│   │   ├── rag/
│   │   │   ├── ingestion.py
│   │   │   ├── embeddings.py
│   │   │   ├── vectorstore.py
│   │   │   └── chatbot.py
│   │   │
│   │   └── services/
│   │       └── chat_service.py
│   │
│   ├── uploads/
│   ├── vectorstore/
│   └── requirements.txt
│
├── README.md
└── .gitignore
```

---

## ⚙️ Installation and Setup

### Prerequisites

Make sure you have installed:

- Python 3.10+
- Node.js and npm
- Git
- Ollama

### 1. Clone the Repository

```bash
git clone https://github.com/Naveen-Kumar2006/CampusAI.git

cd CampusAI
```

### 2. Backend Setup

```bash
cd campusai

python -m venv .venv
```

Activate the virtual environment.

**Windows:**

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Ollama

Pull the required models:

```bash
ollama pull qwen3:8b-q4_K_M
```

```bash
ollama pull nomic-embed-text
```

Make sure Ollama is running locally.

### 4. Start the Backend

From the directory containing the `app` package:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Frontend Setup

Navigate to the frontend directory containing `package.json`:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open the local frontend URL displayed in your terminal.

---

## 🎯 Use Cases

- Answering student queries about college regulations.
- Accessing attendance policies and academic guidelines.
- Finding information from college documents.
- Reducing the time spent searching through multiple PDF documents.
- Providing a centralized AI-powered college information assistant.

---

## 🔮 Future Improvements

- Support for additional document formats.
- Improved conversational memory.
- Source references for generated answers.
- Authentication and role-based access.
- Improved response accuracy and retrieval performance.
- Deployment for wider student accessibility.

---

## 👨‍💻 Developer

**Naveen Kumar T**

B.Tech – Artificial Intelligence and Data Science

Erode Sengunthar Engineering College

- GitHub: https://github.com/Naveen-Kumar2006
- LinkedIn: Add your LinkedIn profile here

---

## ⭐ Support

If you find CampusAI interesting, consider giving this repository a ⭐ on GitHub!

Contributions, suggestions and feedback are welcome.
