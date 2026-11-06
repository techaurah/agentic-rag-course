# Lesson 09: The hashing embedder: a deterministic stand-in

**Time:** about 75 minutes · **Difficulty:** Beginner · **Prerequisites:** Lesson 08 · **You need:** Lesson 08's caveat in mind: a mapping is not meaning.

Real text embeddings come from trained neural models (Lesson 10). They cannot run in this course's stdlib core, so the vector leg needs a stand-in: a deterministic function from text to vectors that behaves enough like an embedder to teach indexing, fusion, and evaluation honestly, without pretending to understand language. This lesson builds it, measures it, and states precisely what it can and cannot do. Throughout the course it is labelled a teaching stand-in. That label is load bearing.

## How it works

The embedder hashes features into 256 dimensions. Features are the content tokens plus character trigrams of each token (so "aphid" and "aphids" share most of their features, which is the stand-in's one semantic trick: shape similarity). Each feature is hashed with MD5 (never Python's salted `hash()`, which changes between runs and would make every measurement irreproducible), the hash chooses a dimension and a sign, and the vector is L2 normalised. Same text, same vector, forever, on any machine: the artifact asserts determinism and unit norm. Indexing is brute force cosine over all chunks, which at 84 chunks is instant and at a million is what Lesson 10's vector stores exist to avoid.

## The measured verdict

Over paragraph chunks with role filtering: document recall at 5 of 1.0, fact recall at 5 of 0.9615, MRR of 0.9423. Better ranking than both lexical legs (MRR 0.9423 against BM25's 0.9359 and TF-IDF's 0.8731), same fact recall as BM25, and a different worst question: its worst fact recall is 0.0 on a question where its shape features mislead it. Read that table correctly: on a corpus of short, clean, well separated documents, character shingles carry a hashing stand-in surprisingly far. It has learned nothing about language. It cannot connect "greenfly" to "aphids" (different shapes, no shared trigrams worth the name), and on real text, paraphrase heavy questions, synonyms, and any semantic distinction ("refund" versus "exchange"), it falls behind a trained model by a wide margin. Lesson 10 shows the real thing and Lesson 15 fixes the gap a different way.

## Why teach with a stand-in at all

Because everything downstream of the embedder (indexing, cosine ranking, fusion weights, evaluation, the agent's tool contract) is identical whether the vectors come from this hasher or from a frontier model, and those mechanics are most of what a builder actually operates. The stand-in makes the full stack runnable offline, deterministic, and testable in CI, at the price of semantic quality, which the course prices openly in every affected lesson instead of hiding.

## Run it

Run `python3 hashing_embedder.py`. `evaluate()` returns the stage table plus the embedder's properties: 256 dimensions, deterministic True, unit norm 1.0, and `word_order_blind: True`, the artifact embedding "aphids on the roses" and "roses on the aphids" to the same vector, a one line proof of what bag of features geometry cannot see.

## Common failures

- **Using Python's built-in `hash()` for features.** It is salted per process; your index would differ between runs and every smoke test would flake. Use a stable digest (the course uses MD5) for anything persisted or measured.
- **Claiming stand-in numbers for real embeddings.** The metrics tables in this course name their embedder for a reason. Quoting 0.9423 MRR as "vector search performance" without the stand-in label is how honest measurements become marketing.
- **Skipping normalisation.** Cosine over unnormalised hashed vectors silently becomes a dot product, and Lesson 08's length bias returns through the back door.

## Recap checklist

- [ ] I can describe the stand-in's features (tokens plus char trigrams, signed hashing, 256 dims).
- [ ] I know its stage table and how its failures differ from BM25's.
- [ ] I can state in one sentence what it cannot do, and which lessons address that.

## Resources

- [Lesson 10](../10-real-embeddings-and-vector-stores/README.md): the real models this stands in for
- [Course glossary](../resources/glossary.md)
