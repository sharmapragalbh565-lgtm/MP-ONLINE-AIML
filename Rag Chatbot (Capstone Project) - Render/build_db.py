from rag_engine import get_rag

print("Pre-building the ChromaDB vector store for production...")
rag = get_rag()
print("Vector store build complete!")
