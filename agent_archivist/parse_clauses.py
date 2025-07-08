# moved from project root
import re
from typing import List, Tuple

CLAUSE_RE = re.compile(
    r'''
    ^                                    # start of a line
    (?P<number>\d+(?:\.\d+)*)            # clause number (1, 3.1, 3.1.2, etc.)
    (?:\.\s|\s)                          # either “.”+space (e.g. “2. ”) or just space (e.g. “3.1 ”)
    (?P<text>.*?)                        # the clause text, non‑greedy
    (?=                                  # stop when you hit:
       ^(?:\d+(?:\.\d+)*)(?:\.\s|\s)     #   another clause header on its own line
      |\Z                                 # or end‑of‑string
    )
    ''',
    re.MULTILINE | re.DOTALL | re.VERBOSE
)

def parse_clauses(text: str) -> List[Tuple[str, str]]:
    """
    Splits `text` into numbered clauses and sub‑clauses.
    Returns a list of (number, text) tuples.
    """
    return [
        f"{m.group('number')} {m.group('text').strip()}"
        for m in CLAUSE_RE.finditer(text)
    ]

if __name__ == "__main__":
    sample_text = """1. First clause text here.
2. Second clause text here.
3.1 Third clause, subclause 1.
3.2 Third clause, subclause 2.
"""
    clauses = parse_clauses(sample_text)
    print(clauses)
    print(f"Found {len(clauses)} clauses.")
    for clause in clauses:
        print("-----")
        print(clause) 