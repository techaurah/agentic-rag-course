"""Lesson 31 artifact: ship check and demo transcript.

Runs five showcase questions through the capstone system,
verifies sample citations against the corpus itself, and
prints the transcript the lesson ships as its demo.
Offline, standard library only. Run: python3 ship_check.py
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


import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location(
    "capstone_system", os.path.join(HERE, "..", "29-build-the-capstone-system", "capstone_system.py"))
capstone = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(capstone)

DEMO = [
    ("How long do gift cards last before they expire?", "public"),
    ("How much discount is there on shrubs in the current sale?", "public"),
    ("I am a Gold member of the Fern Club. Do I pay for delivery on a 40 pound order?", "public"),
    ("What is the wifi password for the cafe?", "public"),
    ("Do you match prices from other garden centres?", "public"),
]


def evaluate():
    s = capstone.get_system()
    transcript = []
    for q, role in DEMO:
        a = s.answer(q, role)
        transcript.append(a)
    verified = 0
    checked = 0
    doc_text = {d["id"]: d["text"] for d in s.docs}
    for a in transcript:
        if a["refused"] or checked >= 3:
            continue
        checked += 1
        if a["doc_id"] in doc_text and a["answer"] in doc_text[a["doc_id"]]:
            verified += 1
    return {
        "demo_questions": len(DEMO),
        "answered": sum(1 for a in transcript if not a["refused"]),
        "refused": sum(1 for a in transcript if a["refused"]),
        "citations_checked": checked,
        "citations_verified": verified,
        "known_miss_in_demo": any(
            (not a["refused"]) and "match prices" in a["question"] for a in transcript),
        "transcript": [
            {"question": a["question"], "refused": a["refused"],
             "answer": a["answer"], "citation": a["citation"]} for a in transcript
        ],
    }


if __name__ == "__main__":
    result = evaluate()
    for entry in result["transcript"]:
        print("Q:", entry["question"])
        if entry["refused"]:
            print("A: (refused) The documents available do not cover that.")
        else:
            print("A:", entry["answer"])
            print("   Source:", entry["citation"])
    print({k: v for k, v in result.items() if k != "transcript"})
