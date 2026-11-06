"""Lesson 13 artifact: reranking, measured honestly.

A deterministic second pass scorer over the hybrid top 10,
judged on fact recall, document recall, precision, and
fact at rank 1. It does not win. The lesson is the verdict.
Offline, standard library only. Run: python3 reranking.py
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


def rerank2(query, candidates, k=5):
    """Second pass: question token coverage + title hits + number bonus."""
    qtoks = set(content_tokens(query))
    wants_number = any(w in query.lower() for w in
                       ["how much", "how many", "how long", "what time", "when",
                        "percent", "percentage", "cost"])

    def score(chunk):
        tset = set(content_tokens(chunk["text"]))
        coverage = len(qtoks & tset) / max(1, len(qtoks))
        title_hit = len(qtoks & set(content_tokens(chunk["title"] + " " + chunk["section"]))) / max(1, len(qtoks))
        has_number = 1.0 if any(ch.isdigit() for ch in chunk["text"]) else 0.0
        return 2.0 * coverage + 1.5 * title_hit + (0.8 * has_number if wants_number else 0.0)

    scored = [(c, score(c)) for c, _ in candidates]
    scored.sort(key=lambda s: (-s[1], s[0]["chunk_id"]))
    return scored[:k]


def num_rerank(query, candidates, k=5):
    """Number aware variant from Experiment 5 of the course build."""
    qtoks = set(content_tokens(query))
    wants_number = any(w in query.lower() for w in
                       ["how much", "how many", "how long", "what time", "percent", "cost"])

    def score(item):
        chunk, _s = item
        tset = set(content_tokens(chunk["text"]))
        coverage = len(qtoks & tset) / max(1, len(qtoks))
        num = 1.0 if any(ch.isdigit() for ch in chunk["text"]) else 0.0
        return coverage + (0.6 * num if wants_number else 0.0)

    scored = [(c, score((c, s))) for c, s in candidates]
    scored.sort(key=lambda x: (-x[1], x[0]["chunk_id"]))
    return scored[:k]


def profile(fn, golden):
    ans = [q for q in golden if q["gold_docs"]]
    fr = [fact_recall_at_k(fn(q["question"], q["role"]), q["facts"], 5) for q in ans]
    dr = [doc_recall_at_k(fn(q["question"], q["role"]), q["gold_docs"], 5) for q in ans]
    p3 = [precision_at_k(fn(q["question"], q["role"]), q["gold_docs"], 3) for q in ans]
    p5 = [precision_at_k(fn(q["question"], q["role"]), q["gold_docs"], 5) for q in ans]
    f1 = [fact_recall_at_k(fn(q["question"], q["role"]), q["facts"], 1) for q in ans]
    n = len(ans)
    return {
        "fact_recall_at_5": round(sum(fr) / n, 4), "doc_recall_at_5": round(sum(dr) / n, 4),
        "precision_at_3": round(sum(p3) / n, 4), "precision_at_5": round(sum(p5) / n, 4),
        "fact_at_1": round(sum(f1) / n, 4),
    }


def evaluate():
    docs = load_docs()
    golden = load_golden()
    chunks = chunk_paragraphs(docs)
    hybrid = make_hybrid(chunks)

    def raw(q, role):
        return hybrid(q, role, 5)

    def wide(q, role):
        a = allowed_for(chunks, role)
        bm = BM25(chunks)
        vx = VectorIndex(chunks)
        return rrf([bm.rank(q, 20, a), vx.rank(q, 20, a)], 10)

    raw_p = profile(raw, golden)
    rr_p = profile(lambda q, role: rerank2(q, wide(q, role), 5), golden)
    num_p = profile(lambda q, role: num_rerank(q, wide(q, role), 5), golden)
    return {
        "raw": raw_p,
        "reranked": rr_p,
        "num_rerank_fact_at_1": num_p["fact_at_1"],
        "verdict": "reranker does not earn its place on this corpus",
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
