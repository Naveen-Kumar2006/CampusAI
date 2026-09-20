from .vector_service import load_vectorstore
from .llm_service import generate_answer


def ask_campus_ai(message: str):

    vectorstore = load_vectorstore()

    results = vectorstore.similarity_search(
        message,
        k=3
    )

    if not results:
        return {
            "answer": "I couldn't find this information in the available college documents.",
            "sources": []
        }

    context_parts = []
    sources = []

    for doc in results:

        context_parts.append(doc.page_content)

        source = doc.metadata.get("source")

        if source and source not in sources:
            sources.append(source)

    context = "\n\n--- DOCUMENT CHUNK ---\n\n".join(
        context_parts
    )

    answer = generate_answer(
        question=message,
        context=context
    )

    return {
        "answer": answer,
        "sources": sources
    }