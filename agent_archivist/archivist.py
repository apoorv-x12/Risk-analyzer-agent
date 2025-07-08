from langgraph.graph import StateGraph
from typing import TypedDict, List, Any
from .load_document import load_document
from .parse_clauses import parse_clauses
from .chunk_clauses import chunk_clauses
from .embed_chunks import embed_chunks
from .store_chunks import store_chunks
from .risk_analysis import analyze_risk_mistral_ollama
from .generate_report import generate_report
import os

class PipelineState(TypedDict):
    pdf_path: str
    text: str
    clauses: List[str]
    chunks: List[str]
    embeddings: Any
    chroma_collection: Any
    risk_results: Any
    report_path: str

def load_document_node(state: PipelineState):
    text = load_document(state["pdf_path"])
    return {"text": text}

def parse_clauses_node(state: PipelineState):
    clauses = parse_clauses(state["text"])
    return {"clauses": clauses}

def chunk_clauses_node(state: PipelineState):
    chunks = chunk_clauses(state["clauses"], chunk_size=3)
    return {"chunks": chunks}

def embed_chunks_node(state: PipelineState):
    embeddings = embed_chunks(state["chunks"])
    return {"embeddings": embeddings}

def store_chunks_node(state: PipelineState):
    collection = store_chunks(state["chunks"], state["embeddings"])
    return {"chroma_collection": collection}

def risk_analysis_node(state: PipelineState):
    risk_results = analyze_risk_mistral_ollama(state["clauses"])
    return {"risk_results": risk_results}

def generate_report_node(state: PipelineState):
    doc_name = os.path.basename(state["pdf_path"])
    report_path = "risk_report.md"
    generate_report(state["risk_results"], document_name=doc_name, output_path=report_path)
    return {"report_path": report_path}

def build_workflow():
    graph = StateGraph(PipelineState)
    graph.add_node("load_document", load_document_node)
    graph.add_node("parse_clauses", parse_clauses_node)
    graph.add_node("chunk_clauses", chunk_clauses_node)
    graph.add_node("embed_chunks", embed_chunks_node)
    graph.add_node("store_chunks", store_chunks_node)
    graph.add_node("risk_analysis", risk_analysis_node)
    graph.add_node("generate_report", generate_report_node)

    graph.add_edge("load_document", "parse_clauses")
    graph.add_edge("parse_clauses", "chunk_clauses")
    graph.add_edge("chunk_clauses", "embed_chunks")
    graph.add_edge("embed_chunks", "store_chunks")
    graph.add_edge("parse_clauses", "risk_analysis")
    graph.add_edge("risk_analysis", "generate_report")

    graph.set_entry_point("load_document")
    return graph.compile()

if __name__ == "__main__":
    workflow = build_workflow()
    result = workflow.invoke({"pdf_path": "sample_contract.pdf"})
    print(f"Found {len(result['clauses'])} clauses.")
    print(f"Found {len(result['chunks'])} chunks.")
    print(f"Generated {len(result['embeddings'])} embeddings.")
    print("Chunks and embeddings stored in Chroma DB.")
    print(f"Risk analysis and report generated: {result['report_path']}") 