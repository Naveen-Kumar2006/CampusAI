import traceback
from .vector_service import load_vectorstore
from .llm_service import generate_answer
def ask_campus_ai(message: str):
    try:
        print("STEP 1: Loading FAISS vector store...")
        vectorstore = load_vectorstore()
        print("STEP 2: Retrieving documents...")
        results = vectorstore.similarity_search(
            message,
            k=3
        )
        print(f"STEP 3: Retrieved {len(results)} documents.")
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
        print("STEP 4: Sending context to Gemini...")
        answer = generate_answer(
            question=message,
            context=context
        )
        print("STEP 5: Answer generated successfully.")
        return {
            "answer": answer,
            "sources": sources
        }
    except Exception:
        print("\nERROR IN CAMPUSAI CHAT SERVICE:")
        traceback.print_exc()
        raise