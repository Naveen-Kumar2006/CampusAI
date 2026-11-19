from langchain_ollama import ChatOllama


llm=ChatOllama(
    model="qwen3:8b-q4_K_M",
    temperature=0.2,
)
def generate_answer(question: str, context: str) -> str:

    prompt = f"""
You are CampusAI, a college information assistant.

Answer the user's question ONLY using the information
provided in the college documents below.

COLLEGE DOCUMENTS:
{context}

USER QUESTION:
{question}

Rules:
1. Use only the provided college documents.
2. Do not invent college rules, dates, policies, or information.
3. If the answer is not available in the documents, say:
   "I couldn't find this information in the available college documents."
4. Give a clear and concise answer.
5. Do not mention that you are an AI unless necessary.
"""

    response = llm.invoke(prompt)
    return response.content.strip()