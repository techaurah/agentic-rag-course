"""Lesson 30 artifact: evaluate and harden the capstone.

Imports Lesson 29's system, runs the full golden set, and
compares every measurement with Lesson 28's gates.
Offline, standard library only. Run: python3 evaluate_capstone.py
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



def paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def chunk_whole(docs):
    """One chunk per document: the naive baseline's unit."""
    chunks = []
    for d in docs:
        body = re.sub(r"^#.*$", "", d["text"], flags=re.M).strip()
        chunks.append({"chunk_id": d["id"], "doc_id": d["id"], "title": d["title"],
                       "section": "", "text": body, "roles": d["roles"]})
    return chunks


def chunk_paragraphs(docs, target=90):
    """Pack paragraphs into chunks of about `target` words, breaking
    at section headings so a chunk never straddles two sections."""
    chunks = []
    for d in docs:
        section = ""
        buf, buf_section = [], ""
        buf_words = 0

        def flush():
            nonlocal buf, buf_words
            if buf:
                text = " ".join(buf)
                cid = f"{d['id']}#{len([c for c in chunks if c['doc_id'] == d['id']])}"
                chunks.append({"chunk_id": cid, "doc_id": d["id"], "title": d["title"],
                               "section": buf_section, "text": text, "roles": d["roles"]})
            buf, buf_words = [], 0

        for para in paragraphs(d["text"]):
            if para.startswith("#"):
                flush()
                section = para.lstrip("# ").strip()
                continue
            w = len(para.split())
            if buf and buf_words + w > target:
                flush()
            if not buf:
                buf_section = section
            buf.append(para)
            buf_words += w
            if buf_words >= target:
                flush()
        flush()
    return chunks


def chunk_sections(docs):
    """One chunk per markdown section: heading plus its paragraphs."""
    chunks = []
    for d in docs:
        section = d["title"]
        buf = []
        n = 0

        def flush():
            nonlocal buf, n
            if buf:
                cid = f"{d['id']}#{n}"
                chunks.append({"chunk_id": cid, "doc_id": d["id"], "title": d["title"],
                               "section": section, "text": " ".join(buf), "roles": d["roles"]})
                n += 1
            buf = []

        for para in paragraphs(d["text"]):
            if para.startswith("##"):
                flush()
                section = para.lstrip("# ").strip()
                continue
            if para.startswith("#"):
                section = d["title"]
                continue
            buf.append(para)
        flush()
    return chunks



def doc_recall_at_k(ranking, gold_docs, k):
    if not gold_docs:
        return None
    got = {c["doc_id"] for c, _ in ranking[:k]}
    return len(got & set(gold_docs)) / len(gold_docs)


def fact_recall_at_k(ranking, facts, k):
    if not facts:
        return None
    text = " ".join(c["text"] for c, _ in ranking[:k]).lower()
    return sum(1 for f in facts if f.lower() in text) / len(facts)


def precision_at_k(ranking, gold_docs, k):
    if not gold_docs or k == 0:
        return None
    return sum(1 for c, _ in ranking[:k] if c["doc_id"] in gold_docs) / k


def mrr(ranking, gold_docs):
    if not gold_docs:
        return None
    for i, (c, _s) in enumerate(ranking):
        if c["doc_id"] in gold_docs:
            return 1.0 / (i + 1)
    return 0.0


def allowed_for(chunks, role):
    return {i for i, c in enumerate(chunks) if role in c["roles"]}


def stage_table(rank_fn, golden, k=5):
    ans = [q for q in golden if q["gold_docs"]]
    dr = [doc_recall_at_k(rank_fn(q["question"], q["role"]), q["gold_docs"], k) for q in ans]
    fr = [fact_recall_at_k(rank_fn(q["question"], q["role"]), q["facts"], k) for q in ans]
    mr = [mrr(rank_fn(q["question"], q["role"]), q["gold_docs"]) for q in ans]
    return {"doc_recall_at_5": round(sum(dr) / len(dr), 4),
            "fact_recall_at_5": round(sum(fr) / len(fr), 4),
            "mrr": round(sum(mr) / len(mr), 4),
            "worst_fact_recall": round(min(fr), 4),
            "questions_below_perfect": sum(1 for v in fr if v < 1.0)}


import importlib.util
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location(
    "capstone_system", os.path.join(HERE, "..", "29-build-the-capstone-system", "capstone_system.py"))
capstone = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(capstone)


def evaluate():
    s = capstone.get_system()
    golden = load_golden()
    gates = s.config["gates"]
    ans = [q for q in golden if q["gold_docs"]]
    dr, fr = [], []
    leaks = 0
    for q in golden:
        ranking = s.retrieve(q["question"], q["role"])
        if q["role"] == "public" and any("public" not in c["roles"] for c, _ in ranking):
            leaks += 1
        if q["gold_docs"]:
            dr.append(doc_recall_at_k(ranking, q["gold_docs"], 5))
            fr.append(fact_recall_at_k(ranking, q["facts"], 5))
    refused, false_ref, answered, grounded, cited = 0, 0, 0, 0, 0
    start = time.perf_counter()
    for q in golden:
        a = s.answer(q["question"], q["role"])
        if q.get("expect") == "refuse":
            if a["refused"]:
                refused += 1
        else:
            if a["refused"]:
                false_ref += 1
            else:
                answered += 1
                if a["citation"]:
                    cited += 1
                doc_text = next(d["text"] for d in s.docs if d["id"] == a["doc_id"])
                if a["answer"] in doc_text:
                    grounded += 1
    mean_ms = round((time.perf_counter() - start) / len(golden) * 1000, 3)
    values = {
        "doc_recall_at_5": round(sum(dr) / len(dr), 4),
        "fact_recall_at_5": round(sum(fr) / len(fr), 4),
        "citation_coverage": round(cited / answered, 4) if answered else 0.0,
        "grounded": round(grounded / answered, 4) if answered else 0.0,
        "refusal_correct": refused,
        "false_refusals": false_ref,
        "restricted_leaks": leaks,
        "mean_latency_ms": mean_ms,
    }
    checks = {
        "doc_recall_at_5": values["doc_recall_at_5"] >= gates["doc_recall_at_5_min"],
        "fact_recall_at_5": values["fact_recall_at_5"] >= gates["fact_recall_at_5_min"],
        "citation_coverage": values["citation_coverage"] >= gates["citation_coverage_min"],
        "grounded": values["grounded"] >= gates["grounded_min"],
        "refusal_correct": values["refusal_correct"] >= gates["refusal_correct_min"],
        "false_refusals": values["false_refusals"] <= gates["false_refusals_max"],
        "restricted_leaks": values["restricted_leaks"] <= gates["restricted_leaks_max"],
        "mean_latency_ms": values["mean_latency_ms"] < gates["mean_latency_ms_max"],
    }
    return {
        "values": values,
        "doc_recall_at_5": values["doc_recall_at_5"],
        "fact_recall_at_5": values["fact_recall_at_5"],
        "refusal_correct": values["refusal_correct"],
        "false_refusals": values["false_refusals"],
        "restricted_leaks": values["restricted_leaks"],
        "gates_pass": checks,
        "all_gates_pass": all(checks.values()),
        "known_miss": "q24 price matching is answered; see Lesson 20 and the refusal gate note",
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
