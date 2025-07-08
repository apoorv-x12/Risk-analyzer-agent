import datetime
from typing import List, Dict

def generate_report(risk_results: List[Dict[str, str]], document_name: str = "sample.pdf", output_path: str = "risk_report.md"):
    """
    Generates a Markdown report from risk analysis results and saves it to disk.
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = len(risk_results)
    risky = sum(1 for r in risk_results if r["risk_label"].lower() == "risky")
    not_risky = sum(1 for r in risk_results if r["risk_label"].lower() == "not risky")
    unknown = total - risky - not_risky
    percent_risky = (risky / total * 100) if total else 0

    lines = [
        f"# Risk Analysis Report",
        f"**Document:** {document_name}",
        f"**Generated:** {now}",
        f"",
        f"## Summary",
        f"- Total clauses: {total}",
        f"- Risky clauses: {risky}",
        f"- Not risky clauses: {not_risky}",
        f"- Unknown: {unknown}",
        f"- % Risky: {percent_risky:.1f}%",
        f"",
        f"## Clause Analysis",
    ]
    for i, r in enumerate(risk_results, 1):
        lines.append(f"### Clause {i}")
        lines.append(f"> {r['clause']}")
        lines.append(f"- **Risk:** {r['risk_label']}")
        lines.append(f"- **Explanation:** {r['explanation']}")
        lines.append("")

    report = "\n".join(lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report saved to {output_path}")
    return report

if __name__ == "__main__":
    # Demo with sample data
    sample_results = [
        {"clause": "The party may terminate this agreement at any time without notice.", "risk_label": "Risky", "explanation": "This clause allows termination without notice, which may expose parties to sudden contract end."},
        {"clause": "All data will be handled in accordance with applicable privacy laws.", "risk_label": "Not Risky", "explanation": "This clause ensures compliance with privacy laws, reducing legal risk."},
    ]
    generate_report(sample_results, document_name="sample.pdf") 