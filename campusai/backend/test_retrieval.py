from app.services.vector_service import load_vectorstore


vectorstore = load_vectorstore()

question = "What is the minimum attendance requirement?"

results = vectorstore.similarity_search(
    question,
    k=3
)

print("\nQuestion:")
print(question)

print("\nRetrieved Documents:\n")

for i, doc in enumerate(results, start=1):
    print(f"--- Result {i} ---")
    print(doc.page_content)
    print("Metadata:", doc.metadata)
    print()