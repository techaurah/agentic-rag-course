"""Lesson 18 artifact: the metrics toolkit.

One harness, every retriever, every metric the course uses:
recall, precision, MRR, fact recall, per type breakdowns.
Offline, standard library only. Run: python3 metrics_lab.py
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



import math


class BM25:
    """Okapi BM25 with the textbook defaults k1=1.5, b=0.75."""

    def __init__(self, chunks, k1=1.5, b=0.75, text_of=None):
        self.chunks = chunks
        self.k1, self.b = k1, b
        self.text_of = text_of or (lambda c: c["title"] + " " + c["section"] + " " + c["text"])
        self.toks = [content_tokens(self.text_of(c)) for c in chunks]
        self.lens = [len(t) for t in self.toks]
        self.avg = sum(self.lens) / max(1, len(self.lens))
        self.df = {}
        for toks in self.toks:
            for t in set(toks):
                self.df[t] = self.df.get(t, 0) + 1
        self.n = len(chunks)

    def idf(self, t):
        df = self.df.get(t, 0)
        return math.log(1 + (self.n - df + 0.5) / (df + 0.5))

    def rank(self, query, k=10, allowed=None):
        q = set(content_tokens(query))
        scores = []
        for i, toks in enumerate(self.toks):
            if allowed is not None and i not in allowed:
                continue
            tf = {}
            for t in toks:
                tf[t] = tf.get(t, 0) + 1
            s = 0.0
            for t in q:
                f = tf.get(t, 0)
                if f:
                    s += self.idf(t) * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.lens[i] / self.avg))
            scores.append((s, i))
        scores.sort(key=lambda s: (-s[0], self.chunks[s[1]]["chunk_id"]))
        return [(self.chunks[i], s) for s, i in scores[:k] if s > 0]



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



def rrf(rankings, k=10, c=60):
    """Reciprocal rank fusion: combine ranked lists by rank, not by
    raw score, so scores from different retrievers never mix units."""
    scores = {}
    by_id = {}
    for ranking in rankings:
        for rank, (chunk, _s) in enumerate(ranking):
            scores[chunk["chunk_id"]] = scores.get(chunk["chunk_id"], 0.0) + 1.0 / (c + rank + 1)
            by_id[chunk["chunk_id"]] = chunk
    out = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    return [(by_id[cid], s) for cid, s in out[:k]]



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



def make_hybrid(chunks):
    bm = BM25(chunks)
    vx = VectorIndex(chunks)

    def hybrid(question, role, k=5):
        a = allowed_for(chunks, role)
        return rrf([bm.rank(question, 20, a), vx.rank(question, 20, a)], k)

    return hybrid

from collections import defaultdict


def per_type(fn, golden):
    byt = defaultdict(list)
    for q in golden:
        if q["gold_docs"]:
            byt[q["type"]].append(fact_recall_at_k(fn(q["question"], q["role"]), q["facts"], 5))
    return {k: round(sum(v) / len(v), 4) for k, v in sorted(byt.items())}


def evaluate():
    docs = load_docs()
    golden = load_golden()
    chunks = chunk_paragraphs(docs)
    tf = Tfidf(chunks)
    bm = BM25(chunks)
    vx = VectorIndex(chunks)
    hybrid = make_hybrid(chunks)
    tables = {
        "tfidf": stage_table(lambda q, role: tf.rank(q, 5, allowed_for(chunks, role)), golden),
        "bm25": stage_table(lambda q, role: bm.rank(q, 5, allowed_for(chunks, role)), golden),
        "vector": stage_table(lambda q, role: vx.rank(q, 5, allowed_for(chunks, role)), golden),
        "hybrid": stage_table(lambda q, role: hybrid(q, role), golden),
    }
    return {
        "tables": tables,
        "hybrid_per_type_fact_recall": per_type(hybrid, golden),
        "metrics_defined": ["doc_recall_at_5", "fact_recall_at_5", "mrr",
                            "worst_fact_recall", "questions_below_perfect"],
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
