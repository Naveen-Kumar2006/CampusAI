from pathlib import Path

from dotenv import load_dotenv
from google import genai
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS


load_dotenv()

VECTORSTORE_DIR = Path("data/vectorstore")

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

client = genai.Client()

MODEL_NAME = "gemini-3.6-flash"


def load_vectorstore():
    return FAISS.load_local(
        str(VECTORSTORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )


def ask_campus_ai(question):
    vectorstore = load_vectorstore()

    docs = vectorstore.similarity_search(
        question,
        k=3
    )

    context = "\n\n".join(
        f"Source: {doc.metadata.get('source', 'Unknown')}\n"
        f"{doc.page_content}"
        for doc in docs
    )

    prompt = f"""
You are CampusAI, a college knowledge assistant.

Answer the user's question using ONLY the provided context.

Rules:
- Do not invent information.
- If the answer is not available in the context, say:
  "I don't know based on the uploaded documents."
- Give a clear and concise answer.

Context:
{context}

Question:
{question}
"""

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=prompt
    )

    return interaction.output_text, docs


if __name__ == "__main__":
    question = input("Ask CampusAI: ")

    answer, sources = ask_campus_ai(question)

    print("\nCampusAI:")
    print(answer)

    print("\nSources:")

    for doc in sources:
        print(doc.metadata)