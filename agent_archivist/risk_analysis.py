import re
from typing import List, Dict
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

LABEL_RE = re.compile(r'^(Risky|Not Risky)[:\-]?\s*(.+)$', re.IGNORECASE)

# Load model and tokenizer once (global for efficiency)
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

def analyze_risk_flan_t5(clauses: List[str]) -> List[Dict[str, str]]:
    """
    For each clause, use Flan-T5 Small to classify as 'Risky' or 'Not Risky' and provide an explanation.
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
        inputs = tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=64)
        content = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
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
    for r in analyze_risk_flan_t5(sample_clauses):
        print(f"Clause:      {r['clause']}\n"
              f"Risk Label:  {r['risk_label']}\n"
              f"Explanation: {r['explanation']}\n")
