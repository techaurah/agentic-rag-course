"""Lesson 08 artifact: vectors and cosine similarity, by hand.

Three toy chunks, one question, every cosine computed from raw
term counts where you can check the arithmetic.
Offline, standard library only. Run: python3 cosine.py
"""

import re

STOP = set("""a an the and or of to in on at for with by from is are was were be been it its this that these those
i you he she we they my your his her our their me him us them do does did can could will would should may might
what when where which who how why is it if then than so such as into about over under per am many much get""".split())

TOKEN = re.compile(r"[a-z0-9]+(?:[.:][0-9]+)?")


def tokenize(text):
    return [t for t in TOKEN.findall(text.lower()) if t not in STOP and len(t) > 1]


def content_tokens(text):
    return tokenize(text)


import math
from collections import Counter

TOY = [
    "the cafe serves coffee and cake",
    "the cafe opens at nine",
    "plants need water in spring",
]
QUESTION = "cafe coffee"


def cosine(a, b):
    dot = sum(a[t] * b[t] for t in a)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return round(dot / (na * nb), 4) if na and nb else 0.0


def evaluate():
    q = Counter(content_tokens(QUESTION))
    scores = {f"chunk_{i}": cosine(q, Counter(content_tokens(d))) for i, d in enumerate(TOY)}
    disjoint = cosine(Counter(content_tokens("pond fish stocking")), Counter(content_tokens(TOY[0])))
    doubled = cosine(q, Counter(content_tokens(TOY[0] + " " + TOY[0])))
    return {
        **scores,
        "best_chunk": max(scores, key=scores.get),
        "disjoint_question_score": disjoint,
        "doubled_chunk_score": doubled["chunk_0"] if isinstance(doubled, dict) else doubled,
        "original_chunk_0_score": scores["chunk_0"],
    }


if __name__ == "__main__":
    for k, v in evaluate().items():
        print(f"{k}: {v}")
