# moved from project root
from sentence_transformers import SentenceTransformer
from typing import List

def embed_chunks(chunks: List[str], model_name: str = "all-MiniLM-L6-v2") -> List[List[float]]:
    """
    Generates embeddings for a list of text chunks using a HuggingFace sentence-transformers model.
    Returns a list of embedding vectors.
    """
    model = SentenceTransformer(model_name)
    embeddings = model.encode(chunks, show_progress_bar=True)
    return embeddings

if __name__ == "__main__":
    # Example chunks
    chunks = [
        "1. First clause text here.\n2. Second clause text here.",
        "3.1 Third clause, subclause 1.\n3.2 Third clause, subclause 2.",
        "4. Fourth clause."
    ]
    embeddings = embed_chunks(chunks)
    print(f"Generated {len(embeddings)} embeddings.")
    print("First embedding vector (truncated):", embeddings[0][:10]) 