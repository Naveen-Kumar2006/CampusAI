from app.services.vector_service import load_vectorstore
from app.services.llm_service import generate_answer


# Load FAISS vector database
vectorstore = load_vectorstore()


# User question
question = "What is the hostel fee?"

# Retrieve relevant documents
results = vectorstore.similarity_search(
    question,
    k=3
)


print("\nQuestion:")
print(question)


print("\nRetrieved Documents:")
print()


# Check whether documents were retrieved
if not results:
    print("No relevant documents found.")
    exit()


# Build context for Gemini
context_parts = []
sources = []


for i, doc in enumerate(results, start=1):

    print(f"--- Result {i} ---")
    print(doc.page_content)
    print("Metadata:", doc.metadata)
    print()

    context_parts.append(doc.page_content)

    source = doc.metadata.get("source")

    if source and source not in sources:
        sources.append(source)


context = "\n\n--- DOCUMENT CHUNK ---\n\n".join(
    context_parts
)


# Generate answer using Gemini
answer = generate_answer(
    question=question,
    context=context
)


print("\n==============================")
print("CampusAI Answer:")
print("==============================")
print(answer)


print("\nSources:")
for source in sources:
    print(source)