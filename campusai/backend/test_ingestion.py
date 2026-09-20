from app.services.document_service import (
    load_documents,
    split_documents
)

from app.services.vector_service import create_vectorstore


documents = load_documents()

print("Documents loaded:", len(documents))


chunks = split_documents(documents)

print("Chunks created:", len(chunks))


vectorstore = create_vectorstore(chunks)

print("Vectorstore created successfully!")