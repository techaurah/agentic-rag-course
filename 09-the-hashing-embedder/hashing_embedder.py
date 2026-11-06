"""Lesson 09 artifact: the hashing embedder, a teaching stand-in.

Deterministic feature hashing (signed, md5 based) maps text to
256 dimensional vectors. Measured on the golden set, labelled
a stand-in everywhere it appears.
Offline, standard library only. Run: python3 hashing_embedder.py
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



import hashlib
import math


def _hash(s):
    return int(hashlib.md5(s.encode()).hexdigest()[:8], 16)


class HashEmbedder:
    """A deterministic TEACHING STAND-IN for a learned embedding model.

    Signed feature hashing over word tokens and character trigrams,
    256 dimensions, L2 normalised. It captures morphology (watering
    sits near water) and word overlap. It does NOT capture meaning:
    it has never seen text before, knows no synonyms, and must never
    be described as matching a real embedding model's quality. Real
    models are Lesson 10's subject.
    """

    DIM = 256

    def embed(self, text):
        vec = [0.0] * self.DIM
        feats = []
        for t in content_tokens(text):
            feats.append("w:" + t)
            padded = "#" + t + "#"
            for i in range(len(padded) - 2):
                feats.append("c:" + padded[i:i + 3])
        for f in feats:
            h = _hash(f)
            vec[h % self.DIM] += 1.0 if (h >> 8) % 2 == 0 else -1.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]


class VectorIndex:
    def __init__(self, chunks, emb=None, text_of=None):
        self.chunks = chunks
        self.emb = emb or HashEmbedder()
        self.text_of = text_of or (lambda c: c["title"] + " " + c["section"] + " " + c["text"])
        self.vecs = [self.emb.embed(self.text_of(c)) for c in chunks]

    def rank(self, query, k=10, allowed=None):
        qv = self.emb.embed(query)
        scores = []
        for i, v in enumerate(self.vecs):
            if allowed is not None and i not in allowed:
                continue
            s = sum(a * b for a, b in zip(qv, v))
            scores.append((s, i))
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
    chunks = chunk_paragraphs(docs)
    index = VectorIndex(chunks)
    table = stage_table(lambda q, role: index.rank(q, 5, allowed_for(chunks, role)), golden)
    emb = HashEmbedder()
    v1 = emb.embed("aphids on the roses")
    v2 = emb.embed("aphids on the roses")
    v3 = emb.embed("roses on the aphids")
    import math
    bag_same = max(abs(a - b) for a, b in zip(v1, v3)) < 1e-9
    return {
        **table,
        "dimensions": len(v1),
        "deterministic": v1 == v2,
        "word_order_blind": bag_same,
        "unit_norm": round(math.sqrt(sum(x * x for x in v1)), 4),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
