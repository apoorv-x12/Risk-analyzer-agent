import chromadb
from chromadb.config import Settings
from chromadb import PersistentClient
from typing import List, Any

def store_chunks(chunks: List[str], embeddings: List[Any], collection_name: str = "clauses"):
    """
    Stores each chunk and its embedding in a Chroma collection, with chunk text as document and order as metadata.
    Returns the Chroma collection object.
    """
    client = PersistentClient(path="chroma_db")  # use PersistentClient for disk storage
    collection = client.get_or_create_collection(name=collection_name)
    
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{"order": i}]
        )
    
    print(f"Stored {len(chunks)} chunks in Chroma.")
    return collection

def query_chunks(query: str, collection_name: str = "clauses", n_results: int = 2):
    """
    Queries the Chroma collection for the most similar chunks to the query string.
    Returns the query results.
    """
    client = PersistentClient(path="chroma_db")  # use PersistentClient for disk storage
    collection = client.get_or_create_collection(name=collection_name)
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "distances", "metadatas"]
    )
    return results

if __name__ == "__main__":

    # Demo: Query the collection
    query = "First clause text here."
    results = query_chunks(query, n_results=2)
    print(results,'hi')
    print("Query results:")
    for doc, dist, meta in zip(results["documents"][0], results["distances"][0], results["metadatas"][0]):
        print(f"Text: {doc}\nDistance: {dist}\nMetadata: {meta}\n")
