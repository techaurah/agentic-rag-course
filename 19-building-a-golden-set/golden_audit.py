"""Lesson 19 artifact: golden set audit.

Validates the golden set the whole course grades against:
structure, literal fact annotation, coverage, and the shape
of a set that can actually fail a bad system.
Offline, standard library only. Run: python3 golden_audit.py
"""

import json
import os


def find_corpus_dir():
    """Walk up from this file until a folder holding corpus/ is found."""
    here = os.path.dirname(os.path.abspath(__file__))
    cur = here
    while True:
        if os.path.isdir(os.path.join(cur, "corpus")):
            return os.path.join(cur, "corpus")
        parent = os.path.dirname(cur)
        if parent == cur:
            raise FileNotFoundError("corpus/ not found above " + here)
        cur = parent


CORPUS_DIR = find_corpus_dir()


def load_docs():
    with open(os.path.join(CORPUS_DIR, "corpus.json")) as f:
        manifest = json.load(f)
    docs = []
    for entry in manifest:
        with open(os.path.join(CORPUS_DIR, entry["file"])) as f:
            docs.append({**entry, "text": f.read()})
    return docs


def load_golden():
    with open(os.path.join(CORPUS_DIR, "golden.json")) as f:
        return json.load(f)



def evaluate():
    docs = load_docs()
    golden = load_golden()
    doc_text = {d["id"]: d["text"].lower() for d in docs}
    missing = []
    for q in golden:
        gold_text = " ".join(doc_text[d] for d in q["gold_docs"])
        for f in q["facts"]:
            if f.lower() not in gold_text:
                missing.append((q["id"], f))
    types = {}
    for q in golden:
        types[q["type"]] = types.get(q["type"], 0) + 1
    refuse = [q for q in golden if q.get("expect") == "refuse"]
    covered = {d for q in golden for d in q["gold_docs"]}
    return {
        "questions": len(golden),
        "unique_ids": len({q["id"] for q in golden}) == len(golden),
        "missing_facts": len(missing),
        "types": types,
        "refuse_questions": len(refuse),
        "refuse_with_gold_docs": sum(1 for q in refuse if q["gold_docs"]),
        "answerable_without_facts": sum(1 for q in golden if q["gold_docs"] and not q["facts"]),
        "documents_covered_as_gold": len(covered),
        "documents_never_gold": sorted({d["id"] for d in docs} - covered),
        "all_answerable_have_gold": all(q["gold_docs"] for q in golden if q.get("expect") != "refuse"),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
