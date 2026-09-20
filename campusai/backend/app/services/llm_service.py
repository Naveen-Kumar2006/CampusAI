import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured")


client = genai.Client(api_key=API_KEY)


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

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=prompt
    )

    return interaction.output_text