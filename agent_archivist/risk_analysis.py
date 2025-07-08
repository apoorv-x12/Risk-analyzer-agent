import re
import ollama
from typing import List, Dict

LABEL_RE = re.compile(r'^(Risky|Not Risky)[:\-]?\s*(.+)$', re.IGNORECASE)

def analyze_risk_ollama(clauses: List[str], model: str = "mistral") -> List[Dict[str, str]]:
    """
    For each clause, ask the Ollama LLM if it's “Risky” or “Not Risky”,
    then parse out the one‑sentence explanation.
    """
    results = []
    for clause in clauses:
        prompt = (
            "Is the following clause risky in a legal or compliance context? "
            "Reply with 'Risky:' or 'Not Risky:' followed by a one-sentence explanation.\n\n"
            f"Clause: {clause}"
        )
        # Official Ollama Python API returns a dict with 'choices'
        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        content = response["message"]["content"].strip()

        m = LABEL_RE.match(content)
        if m:
            label = m.group(1).title()        # “Risky” or “Not Risky”
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
    for r in analyze_risk_ollama(sample_clauses):
        print(f"Clause:      {r['clause']}\n"
              f"Risk Label:  {r['risk_label']}\n"
              f"Explanation: {r['explanation']}\n")
