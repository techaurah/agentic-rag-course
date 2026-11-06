"""Lesson 00 artifact: environment and corpus check.

Verifies the Python version, finds the corpus by walking up
from this file, and reports what the course will measure.
Offline, standard library only. Run: python3 check_environment.py
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


import sys


def evaluate():
    docs = load_docs()
    golden = load_golden()
    words = sum(len(d["text"].split()) for d in docs)
    answerable = sum(1 for q in golden if q["gold_docs"])
    refuse = sum(1 for q in golden if q.get("expect") == "refuse")
    roles = sorted({r for d in docs for r in d["roles"]})
    return {
        "python_ok": sys.version_info >= (3, 11),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "documents": len(docs),
        "corpus_words": words,
        "golden_questions": len(golden),
        "answerable": answerable,
        "refuse_expected": refuse,
        "roles": roles,
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
