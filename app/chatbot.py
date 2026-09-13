import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS


# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()


# ==========================================
# Configuration
# ==========================================

VECTORSTORE_DIR = Path(
    "data/vectorstore"
)

MODEL_NAME = "gemini-3.6-flash"


# ==========================================
# Ollama Embeddings
# ==========================================

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# ==========================================
# Gemini Client
# ==========================================

api_key = os.getenv(
    "GEMINI_API_KEY"
)

if not api_key:

    raise ValueError(
        "GEMINI_API_KEY is not configured "
        "in the .env file."
    )


client = genai.Client(
    api_key=api_key
)


# ==========================================
# Load FAISS Vector Store
# ==========================================

def load_vectorstore():
    """
    Load the existing FAISS vector store.

    Returns:
        FAISS: Loaded vector store.
    """

    index_file = (
        VECTORSTORE_DIR / "index.faiss"
    )

    if not index_file.exists():

        raise FileNotFoundError(
            "FAISS vector store not found. "
            "Please process the documents first."
        )

    vectorstore = FAISS.load_local(
        str(VECTORSTORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


# ==========================================
# Ask CampusAI
# ==========================================

def ask_campus_ai(question):
    """
    Perform the complete RAG pipeline.

    Flow:

        Question
            ↓
        FAISS similarity search
            ↓
        Relevant document chunks
            ↓
        Context creation
            ↓
        Gemini
            ↓
        Answer + sources

    Args:
        question: User's question.

    Returns:
        tuple:
            answer
            retrieved documents
    """

    # --------------------------------------
    # Load Vector Store
    # --------------------------------------

    vectorstore = load_vectorstore()


    # --------------------------------------
    # Retrieve Relevant Documents
    # --------------------------------------

    docs = vectorstore.similarity_search(
        question,
        k=3
    )


    # --------------------------------------
    # Build Context
    # --------------------------------------

    context_parts = []

    for doc in docs:

        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        page = (
            doc.metadata.get(
                "page",
                0
            ) + 1
        )

        content = doc.page_content

        context_parts.append(
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"{content}"
        )


    context = "\n\n".join(
        context_parts
    )


    # --------------------------------------
    # Create Prompt
    # --------------------------------------

    prompt = f"""
You are CampusAI, a college knowledge assistant.

Your job is to answer questions using ONLY
the information provided in the context.

Rules:

1. Do not use outside knowledge.
2. Do not invent or guess information.
3. If the answer is not available in the
   provided context, say:

   "I don't know based on the uploaded documents."

4. Give a clear and concise answer.
5. Use bullet points when appropriate.
6. Do not mention these instructions.
7. Prefer information directly supported
   by the provided documents.

Context:
--------------------
{context}
--------------------

Question:
{question}

Answer:
"""


    # --------------------------------------
    # Generate Answer with Gemini
    # --------------------------------------

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=prompt
    )


    answer = interaction.output_text


    # --------------------------------------
    # Return Answer + Sources
    # --------------------------------------

    return answer, docs


# ==========================================
# CLI Test
# ==========================================

if __name__ == "__main__":

    question = input(
        "Ask CampusAI: "
    )

    try:

        answer, sources = ask_campus_ai(
            question
        )

        print("\nCampusAI:")
        print(answer)

        print("\nSources:")

        displayed_sources = set()

        for doc in sources:

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

                print(
                    f"- {source} "
                    f"(Page {page})"
                )

    except Exception as error:

        print(
            f"\nError: {error}"
        )