"""Lesson 02 artifact: corpus audit.

Counts and checks the manifest the whole course depends on:
roles, dates, supersession, sections, vocabulary.
Offline, standard library only. Run: python3 corpus_audit.py
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


import re

STOP = set("""a an the and or of to in on at for with by from is are was were be been it its this that these those
i you he she we they my your his her our their me him us them do does did can could will would should may might
what when where which who how why is it if then than so such as into about over under per am many much get""".split())

TOKEN = re.compile(r"[a-z0-9]+(?:[.:][0-9]+)?")


def tokenize(text):
    return [t for t in TOKEN.findall(text.lower()) if t not in STOP and len(t) > 1]


def content_tokens(text):
    return tokenize(text)



def evaluate():
    docs = load_docs()
    golden = load_golden()
    by_role = {}
    for d in docs:
        for r in d["roles"]:
            by_role[r] = by_role.get(r, 0) + 1
    sections = sum(d["text"].count("\n## ") + (1 if d["text"].startswith("# ") else 0) for d in docs)
    vocab = set()
    for d in docs:
        vocab |= set(content_tokens(d["text"]))
    types = {}
    for q in golden:
        types[q["type"]] = types.get(q["type"], 0) + 1
    return {
        "documents": len(docs),
        "total_words": sum(len(d["text"].split()) for d in docs),
        "sections": sections,
        "vocabulary_size": len(vocab),
        "public_documents": by_role.get("public", 0),
        "staff_documents": by_role.get("staff", 0),
        "manager_documents": by_role.get("manager", 0),
        "superseded_pairs": sum(1 for d in docs if d.get("superseded_by")),
        "all_have_updated": all(d.get("updated") for d in docs),
        "all_have_roles": all(d.get("roles") for d in docs),
        "golden_types": types,
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
