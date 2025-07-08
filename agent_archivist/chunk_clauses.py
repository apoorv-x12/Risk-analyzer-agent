# moved from project root
from typing import List

def chunk_clauses(clauses: List[str], chunk_size: int = 3) -> List[str]:
    """
    Groups clauses into chunks of `chunk_size`.
    Returns a list of chunked text blocks.
    """
    return [
        "\n".join(clauses[i:i+chunk_size])
        for i in range(0, len(clauses), chunk_size)
    ]

if __name__ == "__main__":
    # Example input
    clauses = [
        "1. First clause text here.",
        "2. Second clause text here.",
        "3.1 Third clause, subclause 1.",
        "3.2 Third clause, subclause 2.",
        "4. Fourth clause.",
    ]
    chunks = chunk_clauses(clauses, chunk_size=2)
    print(f"Found {len(chunks)} chunks.")
    for i, chunk in enumerate(chunks, 1):
        print(f"--- Chunk {i} ---")
        print(chunk) 