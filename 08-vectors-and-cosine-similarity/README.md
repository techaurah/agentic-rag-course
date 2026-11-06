# Lesson 08: Vectors and cosine similarity: the geometry of meaning (and its limits)

**Time:** about 60 minutes · **Difficulty:** Beginner · **Prerequisites:** Lesson 05 · **You need:** A pen; this lesson rewards working the arithmetic once by hand.

Everything in the vector half of this course rests on one picture: a text becomes a point in a space, similar texts land near each other, and "near" is measured by the angle between their vectors. This lesson builds that picture with counts you can verify on paper, then states the limit that the rest of the module keeps honest: the geometry is only as meaningful as the mapping from text to numbers, and a bad mapping gives you precise nonsense.

## The worked example

Three toy chunks and the question "cafe coffee", as raw term count vectors after the course tokenizer drops stopwords. Chunk 0, "the cafe serves coffee and cake", becomes {cafe 1, serves 1, coffee 1, cake 1}. The question is {cafe 1, coffee 1}. The dot product is 2 (cafe and coffee each contribute 1). The question's length is sqrt(2) ≈ 1.414; chunk 0's length is sqrt(4) = 2. Cosine = 2 / (1.414 × 2) = 0.7071. Chunk 1, {cafe 1, opens 1, nine 1}, shares only cafe: cosine = 1 / (1.414 × 1.732) = 0.4082. Chunk 2 shares nothing: 0.0. The ranking 0.7071, 0.4082, 0.0 is exactly the ranking a human gives, produced by arithmetic a spreadsheet can do. That is the whole mechanism; everything after this lesson is about choosing better numbers to put in the vectors.

## Three properties to internalise

**Length does not win.** Double chunk 0 (repeat it verbatim) and its cosine is unchanged, 0.7071: the dot product and the length both double, and cancel. Cosine grades direction, not size, which is why Lesson 05's TF-IDF used it.

**Zero overlap is exactly zero.** A question sharing no terms with a chunk scores 0.0, and a question sharing no terms with anything (the artifact tests "pond fish stocking" against chunk 0) has no ranking at all, just ties at zero. Sparse vectors cannot soften this; only a different mapping (Lesson 09's hashing features, Lesson 10's learned embeddings) can put "greenfly" and "aphids" near each other, and only the learned kind actually knows they belong together.

**Similarity is not relevance.** Cosine measures angle between the vectors you built. If your mapping puts word counts in, you get word overlap geometry, as here. The number is always exact; what it means depends entirely on the mapping, which is why this course never reports a vector score without naming the embedder that produced it.

## Run it

Run `python3 cosine.py`. `evaluate()` returns the three cosines (0.7071, 0.4082, 0.0), the disjoint score (0.0), and the doubled chunk score, identical to the original at 0.7071. Recompute one of them by hand before moving on; the five minutes buys intuition no diagram provides.

## Common failures

- **Using dot product instead of cosine.** Dot product rewards length: the longest chunk wins broad questions regardless of direction. If a system feels biased toward big documents, check which one it computes.
- **Forgetting that zero is a valid, common score.** Sparse pipelines return empty or tied rankings constantly; code that assumes a positive top score breaks exactly on the questions users actually ask.
- **Reading meaning into a stand-in's geometry.** Lesson 09's embedder produces real cosines from hashed features. The angles are well defined; the semantics are approximate. Keep the two apart.

## Recap checklist

- [ ] I computed one cosine from the worked example by hand and matched 0.7071 or 0.4082.
- [ ] I can explain why doubling a chunk leaves its cosine unchanged.
- [ ] I can state the mapping caveat: similarity is only as meaningful as the text to numbers mapping.

## Resources

- [Course 1, Lesson 19: RAG with a framework, and agentic RAG](https://github.com/techaurah/agentic-ai-for-beginners): embeddings introduced in builder terms
- [Course glossary](../resources/glossary.md)
