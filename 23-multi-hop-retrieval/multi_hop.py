"""Lesson 23 artifact: multi-hop retrieval, end to end.

Single shot against decomposed union retrieval on the
multi-hop questions, graded at two layers: documents found,
and facts present in the composed answer.
Offline, standard library only. Run: python3 multi_hop.py
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



def fresh_filter(question, idxs, chunks, manifest):
    """Drop superseded documents unless the question names their
    period (a question about the spring sale deserves the spring
    document; every other question deserves the current one)."""
    q = question.lower()
    keep = set()
    for i in idxs:
        d = manifest[chunks[i]["doc_id"]]
        if d.get("superseded_by"):
            period = d["id"].split("-")[0]
            if period not in q:
                continue
        keep.add(i)
    return keep



MONTHS = {"january", "february", "march", "april", "may", "june", "july",
          "august", "september", "october", "november", "december"}
NUMBER_WORDS = {"one", "two", "three", "four", "five", "six", "seven", "eight",
                "nine", "ten", "eleven", "twelve", "first", "second", "third"}
QUANTITY = ["how much", "how many", "how long", "what time", "what percentage",
            "what discount", "when"]
SENT = re.compile(r"(?<=[.!?])\s+")
UNSEEN_MIN = 2


def stem(t):
    for suf in ("ing", "ed", "es", "s"):
        if len(t) > len(suf) + 2 and t.endswith(suf):
            return t[: -len(suf)]
    return t


def fuzzy_in(qt, toks):
    qs = stem(qt)
    return any(stem(t) == qs or qt == t or (len(qt) >= 5 and len(t) >= 5 and qt[:5] == t[:5]) for t in toks)


def compose_answer(question, ranking, df, n_chunks, permitted_tokens, k=5):
    """Extractive answer composer with the refusal rules.

    An answer is one sentence copied from a retrieved chunk, with
    its citation. The composer refuses (returns None) when:
    - the question carries at least UNSEEN_MIN content concepts the
      permitted corpus does not contain at all, or
    - no retrieved sentence shares at least two question tokens
      (fuzzy) including one reasonably specific token, or
    - the question asks for a quantity and the sentence has no digit.
    """
    qtoks = set(content_tokens(question))
    unseen = {t for t in qtoks if df.get(t, 0) == 0 and not any(ch.isdigit() for ch in t)
              and t not in MONTHS and t not in NUMBER_WORDS
              and not fuzzy_in(t, permitted_tokens)}
    if len(unseen) >= UNSEEN_MIN:
        return None
    wants_number = any(w in question.lower() for w in QUANTITY)
    best = []
    for chunk, _s in ranking[:k]:
        for sent in [s.strip() for s in SENT.split(chunk["text"]) if s.strip()]:
            stoks = set(content_tokens(sent))
            shared = {t for t in qtoks if fuzzy_in(t, stoks)}
            distinctive = {t for t in shared if df.get(t, 0) <= max(2, n_chunks // 4)}
            if len(shared) < 2 or not distinctive:
                continue
            if wants_number and not any(ch.isdigit() for ch in sent):
                continue
            best.append((len(shared), sent, chunk))
    best.sort(key=lambda x: -x[0])
    return best[0] if best else None



def build_system(chunks):
    return BM25(chunks), VectorIndex(chunks)


def hybrid_rank(question, role, chunks, bm, vx, manifest, k=5):
    """Hybrid RRF ranking with role and freshness filters applied."""
    a = allowed_for(chunks, role)
    raw = rrf([bm.rank(question, 20, a), vx.rank(question, 20, a)], 20)
    smap = {c["chunk_id"]: s for c, s in raw}
    by_id = {c["chunk_id"]: i for i, c in enumerate(chunks)}
    ordered = [by_id[c["chunk_id"]] for c, _ in raw]
    keep = fresh_filter(question, ordered, chunks, manifest)
    return [(chunks[i], smap[chunks[i]["chunk_id"]]) for i in ordered if i in keep][:k]


def permitted_stats(chunks, role):
    """Token document frequencies and vocabulary of the permitted corpus."""
    df, toks = {}, set()
    for i in allowed_for(chunks, role):
        st = set(content_tokens(chunks[i]["text"]))
        toks |= st
        for t in st:
            df[t] = df.get(t, 0) + 1
    return df, toks

HAND_SUBQUERIES = {
    "q09": ["Fern Club Gold members delivery", "delivery charges free over 75 pounds"],
    "q10": ["plant guarantee 12 months", "sale items plants covered guarantee returns"],
    "q11": ["gift cards expire months"],
    "q28": ["loyalty vouchers gift cards", "gift cards bought with loyalty vouchers"],
    "q29": ["stores open Sundays hours", "which stores have a cafe"],
}


def union_rank(question, role, subqueries, chunks, bm, vx, manifest, per=3):
    seen, out = set(), []
    for s in subqueries:
        for c, sc in hybrid_rank(s, role, chunks, bm, vx, manifest, per):
            if c["chunk_id"] not in seen:
                seen.add(c["chunk_id"])
                out.append((c, sc))
    return out


def answer_coverage(question, ranking, chunks):
    df, toks = permitted_stats(chunks, question["role"])
    ans = compose_answer(question["question"], ranking, df, len(chunks), toks)
    if ans is None:
        return 0.0
    return round(sum(1 for f in question["facts"] if f.lower() in ans[1].lower()) / len(question["facts"]), 4)


def evaluate():
    docs = load_docs()
    golden = load_golden()
    chunks = chunk_paragraphs(docs)
    manifest = {d["id"]: d for d in docs}
    bm, vx = build_system(chunks)
    multi = [q for q in golden if q["type"] == "multihop"]
    per_q = {}
    sd, ud, sc, uc = [], [], [], []
    for q in multi:
        single = hybrid_rank(q["question"], q["role"], chunks, bm, vx, manifest, 5)
        union = union_rank(q["question"], q["role"], HAND_SUBQUERIES[q["id"]], chunks, bm, vx, manifest)
        a = doc_recall_at_k(single, q["gold_docs"], 5)
        b = doc_recall_at_k(union, q["gold_docs"], len(union))
        c1 = answer_coverage(q, single, chunks)
        c2 = answer_coverage(q, union, chunks)
        per_q[q["id"]] = {"doc_single": a, "doc_union": b, "coverage_single": c1, "coverage_union": c2}
        sd.append(a); ud.append(b); sc.append(c1); uc.append(c2)
    n = len(multi)
    return {
        "per_question": per_q,
        "doc_recall_single": round(sum(sd) / n, 4),
        "doc_recall_union": round(sum(ud) / n, 4),
        "coverage_single": round(sum(sc) / n, 4),
        "coverage_union": round(sum(uc) / n, 4),
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
