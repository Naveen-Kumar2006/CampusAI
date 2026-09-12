import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai

from app.ingestion import load_documents, split_documents
from app.vectorstore import embeddings, VECTORSTORE_DIR
from langchain_community.vectorstores import FAISS


# ==========================================
# Configuration
# ==========================================

load_dotenv()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# Gemini Client
# ==========================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is not configured in the .env file.")
    st.stop()

client = genai.Client(
    api_key=api_key
)

MODEL_NAME = "gemini-3.6-flash"


# ==========================================
# Streamlit Configuration
# ==========================================

st.set_page_config(
    page_title="CampusAI",
    page_icon="🎓",
    layout="wide"
)


# ==========================================
# Header
# ==========================================

st.title("🎓 CampusAI")
st.write("AI assistant for college documents")


# ==========================================
# Sidebar - Upload Documents
# ==========================================

st.sidebar.header("📄 Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True
)


if uploaded_files:

    for uploaded_file in uploaded_files:

        file_path = UPLOAD_DIR / uploaded_file.name

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    st.sidebar.success(
        f"{len(uploaded_files)} document(s) uploaded."
    )


# ==========================================
# Sidebar - Process Documents
# ==========================================

st.sidebar.header("⚙️ Document Processing")

if st.sidebar.button("🔄 Process Documents"):

    with st.spinner("Processing documents..."):

        documents = load_documents()

        if not documents:

            st.error("No PDF documents found.")

        else:

            chunks = split_documents(documents)

            vectorstore = FAISS.from_documents(
                chunks,
                embeddings
            )

            vectorstore.save_local(
                str(VECTORSTORE_DIR)
            )

            st.success(
                f"✅ Processed {len(chunks)} chunks."
            )


# ==========================================
# Chat Input
# ==========================================

question = st.chat_input(
    "Ask something about your college..."
)


# ==========================================
# Question Processing
# ==========================================

if question:

    # Check whether vectorstore exists
    index_file = VECTORSTORE_DIR / "index.faiss"

    if not index_file.exists():

        st.error(
            "Please upload and process documents first."
        )

        st.stop()


    # ======================================
    # Retrieve Documents
    # ======================================

    with st.spinner("🔎 Searching documents..."):

        vectorstore = FAISS.load_local(
            str(VECTORSTORE_DIR),
            embeddings,
            allow_dangerous_deserialization=True
        )

        docs = vectorstore.similarity_search(
            question,
            k=3
        )


    # ======================================
    # Build Context
    # ======================================

    context = "\n\n".join(
        f"Source: {doc.metadata.get('source', 'Unknown')}\n"
        f"Page: {doc.metadata.get('page', 0) + 1}\n"
        f"{doc.page_content}"
        for doc in docs
    )


    # ======================================
    # Gemini Prompt
    # ======================================

    prompt = f"""
You are CampusAI, a college knowledge assistant.

Answer the user's question using ONLY the provided context.

Rules:
- Do not use outside knowledge.
- Do not invent information.
- If the answer is not available in the context, say:
  "I don't know based on the uploaded documents."
- Give a clear and concise answer.
- Use bullet points when appropriate.

Context:
{context}

Question:
{question}
"""


    # ======================================
    # Generate Answer
    # ======================================

    with st.spinner("🤖 CampusAI is thinking..."):

        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=prompt
        )

        answer = interaction.output_text


    # ======================================
    # Display User Question
    # ======================================

    st.chat_message("user").write(question)


    # ======================================
    # Display Assistant Answer
    # ======================================

    with st.chat_message("assistant"):

        st.write(answer)


        # ==================================
        # Sources
        # ==================================

        st.markdown("### 📚 Sources")

        displayed_sources = set()

        for doc in docs:

            source = Path(
                doc.metadata.get(
                    "source",
                    "Unknown"
                )
            ).name

            page = (
                doc.metadata.get("page", 0) + 1
            )

            source_key = (source, page)

            if source_key not in displayed_sources:

                displayed_sources.add(source_key)

                st.write(
                    f"📄 {source} — Page {page}"
                )