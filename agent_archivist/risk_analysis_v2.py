from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Example training data (expand for real use)
clauses = [
    "The party may terminate this agreement at any time without notice.",
    "All data will be handled in accordance with applicable privacy laws.",
    "The customer is liable for all damages.",
    "This contract is void if payment is late.",
    "The agreement may be renewed annually."
]
labels = ["Risky", "Not Risky", "Risky", "Risky", "Not Risky"]

# Train model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(clauses)
clf = LogisticRegression()
clf.fit(X, labels)

def analyze_risk_sklearn(clauses_to_check: List[str]) -> List[Dict[str, str]]:
    X_test = vectorizer.transform(clauses_to_check)
    preds = clf.predict(X_test)
    results = []
    for clause, label in zip(clauses_to_check, preds):
        explanation = (
            "Classified as risky based on training data." if label == "Risky"
            else "No risky pattern detected."
        )
        results.append({
            "clause": clause,
            "risk_label": label,
            "explanation": explanation
        })
    return results

if __name__ == "__main__":
    test_clauses = [
        "The party may terminate this agreement at any time without notice.",
        "All data will be handled in accordance with applicable privacy laws.",
    ]
    for r in analyze_risk_sklearn(test_clauses):
        print(f"Clause:      {r['clause']}\n"
              f"Risk Label:  {r['risk_label']}\n"
              f"Explanation: {r['explanation']}\n") 