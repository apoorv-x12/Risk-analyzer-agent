"""
Risk Analysis Functions for Contract Clauses

- analyze_risk_flan_t5: Uses Flan-T5 (HuggingFace/transformers) for local inference (requires model and torch installed).
- analyze_risk_mistral_ollama: Uses Mistral via local Ollama server (HTTP API) for inference. Recommended for local Mistral users.

Each function takes a list of clauses and returns a list of dicts with 'clause', 'risk_label', and 'explanation'.
"""
import re
from typing import List, Dict
import requests

LABEL_RE = re.compile(r'^(Risky|Not Risky)[:\-]?\s*(.+)$', re.IGNORECASE)

def analyze_risk_flan_t5(clauses: List[str]) -> List[Dict[str, str]]:
    """
    For each clause, use Flan-T5 Small to classify as 'Risky' or 'Not Risky' and provide an explanation.
    Requires HuggingFace transformers and a local Flan-T5 model.
    """
    # NOTE: This function is left as a placeholder. Actual model loading code should be added if needed.
    raise NotImplementedError("Flan-T5 local inference is not currently supported in this refactored file. Use analyze_risk_mistral_ollama instead.")

def analyze_risk_mistral_ollama(clauses: List[str], model: str = "mistral") -> List[Dict[str, str]]:
    """
    For each clause, use Mistral via Ollama to classify as 'Risky' or 'Not Risky' and provide an explanation.
    """
    results = []
    for clause in clauses:
        prompt = (
            "You are a legal risk classifier. For each clause, respond with either:\n"
            "Risky: <one-sentence explanation>\n"
            "or\n"
            "Not Risky: <one-sentence explanation>\n\n"
            "Example:\n"
            "Clause: The party may terminate this agreement at any time without notice.\n"
            "Answer: Risky: This clause allows termination without notice, which poses a risk to contract stability.\n\n"
            "Now classify the following clause:\n"
            f"Clause: {clause}\n"
            "Answer:"
        )
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        content = response.json()["response"].strip()
        # Try to extract label and explanation
        m = LABEL_RE.search(content)
        if m:
            label = m.group(1).title()
            explanation = m.group(2).strip()
        else:
            label = "Unknown"
            explanation = content
        results.append({
            "clause": clause,
            "risk_label": label,
            "explanation": explanation
        })
    return results

if __name__ == "__main__":
    sample_clauses = [
        "The party may terminate this agreement at any time without notice.",
        "All data will be handled in accordance with applicable privacy laws.",
    ]
    for r in analyze_risk_mistral_ollama(sample_clauses):
        print(f"Clause:      {r['clause']}\n"
              f"Risk Label:  {r['risk_label']}\n"
              f"Explanation: {r['explanation']}\n")
