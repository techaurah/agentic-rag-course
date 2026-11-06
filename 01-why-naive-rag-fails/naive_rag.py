"""Lesson 01 artifact: the naive RAG pipeline, measured.

Whole documents, one TF-IDF index, top 5, no chunking, no role
filter, no refusal: the pipeline most demos ship. evaluate()
reports its recall and its five failure modes.
Offline, standard library only. Run: python3 naive_rag.py
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



import math


class Tfidf:
    """TF-IDF vectors as sparse dicts, cosine similarity ranking."""

    def __init__(self, chunks, text_of=None):
        self.chunks = chunks
        self.text_of = text_of or (lambda c: c["title"] + " " + c["section"] + " " + c["text"])
        self.df = {}
        self.vecs = []
        for c in chunks:
            vec = {}
            for t in content_tokens(self.text_of(c)):
                vec[t] = vec.get(t, 0) + 1
            self.vecs.append(vec)
            for t in vec:
                self.df[t] = self.df.get(t, 0) + 1
        self.n = len(chunks)

    def idf(self, t):
        return math.log((self.n + 1) / (self.df.get(t, 0) + 1)) + 1.0

    def rank(self, query, k=10, allowed=None):
        q = {}
        for t in content_tokens(query):
            q[t] = q.get(t, 0) + 1
        scores = []
        for i, vec in enumerate(self.vecs):
            if allowed is not None and i not in allowed:
                continue
            dot = sum(cnt * self.idf(t) * q.get(t, 0) for t, cnt in vec.items())
            norm = math.sqrt(sum((cnt * self.idf(t)) ** 2 for t, cnt in vec.items())) or 1.0
            qnorm = math.sqrt(sum((cnt * self.idf(t)) ** 2 for t, cnt in q.items())) or 1.0
            scores.append((dot / (norm * qnorm), i))
        scores.sort(key=lambda s: (-s[0], self.chunks[s[1]]["chunk_id"]))
        return [(self.chunks[i], s) for s, i in scores[:k] if s > 0]



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



def evaluate():
    docs = load_docs()
    golden = load_golden()
    chunks = chunk_whole(docs)
    index = Tfidf(chunks)
    table = stage_table(lambda q, role: index.rank(q, 5), golden)
    public_qs = [q for q in golden if q["role"] == "public"]
    leaks = 0
    for q in public_qs:
        top = index.rank(q["question"], 5)
        if any("public" not in c["roles"] for c, _ in top):
            leaks += 1
    refuse_answered = 0
    for q in golden:
        if q.get("expect") == "refuse" and index.rank(q["question"], 1):
            refuse_answered += 1
    ans = [q for q in golden if q["gold_docs"]]
    words = sum(len(c["text"].split()) for q in ans for c, _ in index.rank(q["question"], 5)) / len(ans)
    return {
        **table,
        "public_questions": len(public_qs),
        "leaking_questions": leaks,
        "refuse_expected": sum(1 for q in golden if q.get("expect") == "refuse"),
        "refuse_questions_answered": refuse_answered,
        "avg_context_words": round(words),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
