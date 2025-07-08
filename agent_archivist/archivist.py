from .load_document import load_document
from .parse_clauses import parse_clauses
from .chunk_clauses import chunk_clauses
from .embed_chunks import embed_chunks

class AgentArchivist:
    def __init__(self, chunk_size=3):
        self.chunk_size = chunk_size

    def process(self, pdf_path):
        # 1. Load document
        text = load_document(pdf_path)
        # 2. Parse clauses
        clauses = parse_clauses(text)
        # 3. Chunk clauses
        chunks = chunk_clauses(clauses, chunk_size=self.chunk_size)
        # 4. Embed chunks
        embeddings = embed_chunks(chunks)
        return {
            "clauses": clauses,
            "chunks": chunks,
            "embeddings": embeddings,
        }

if __name__ == "__main__":
    agent = AgentArchivist(chunk_size=3)
    result = agent.process("sample.pdf")
    print(f"Found {len(result['clauses'])} clauses.")
    print(f"Found {len(result['chunks'])} chunks.")
    print(f"Generated {len(result['embeddings'])} embeddings.") 