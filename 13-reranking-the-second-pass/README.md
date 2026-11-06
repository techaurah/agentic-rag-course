# Lesson 13: Reranking: the second pass, and when it does not pay

**Time:** about 60 minutes · **Difficulty:** Intermediate · **Prerequisites:** Lesson 11 · **You need:** The hybrid's stage table from Lesson 11.

Reranking is the standard second act of a retrieval pipeline: a cheap retriever proposes a wide candidate set (here the hybrid's top 10), and a more careful scorer reorders it into the final top 5. In production the second scorer is often a cross-encoder model that reads question and chunk together; this lesson's deterministic scorer (question token coverage, title and section hits, a bonus for containing numbers when the question asks for a quantity) is its stdlib stand-in, and it plays the role honestly, including the outcome: on this corpus, reranking does not pay, and the lesson's job is to make that verdict precise and generalisable.

## The measured verdict

Fact recall at 5: raw hybrid 0.9808, reranked 0.9808. No gain. Document recall at 5: 0.9808 down to 0.9615; the reranker actually pushes one gold document out of the final five. Precision at 3: 0.6026 down to 0.4615; precision at 5: 0.5231 down to 0.4154. The reranked list is a worse set: more non gold chunks occupy the places a generator reads. One metric improves: fact at rank 1 rises from 0.75 to 0.7885 (the number aware variant scores 0.7692), because coverage plus a number bonus is genuinely good at picking the single most fact dense chunk. So the reranker is not broken; it optimises the top slot at the expense of the set. Whether that trade serves you depends on what your generator consumes: a system that answers from the top chunk gains; a system that reads a five chunk context, as this course's does, loses.

## Why it fails here, and when it would not

The candidate set is already good. With 84 chunks and clean documents, the hybrid's top 10 almost always contains the gold chunks in a sane order; a hand built scorer has no extra signal to add, only its own biases (coverage double counts what BM25 already rewarded; the title bonus over promotes heading heavy chunks). Reranking earns its keep when the first pass is weak relative to the corpus: hundreds of thousands of chunks, noisy OCR text, or questions whose relevance is semantic in ways the first pass cannot see, and when the second scorer is a trained model bringing genuinely new information. The generalisable skill is the keep or drop rule: rerank on your golden set, compare the full profile (recall, precision, fact at 1), and keep the stage only if the profile your product feels improves by more than the added latency costs. "Everyone reranks" is not a measurement.

## Run it

Run `python3 reranking.py`. `evaluate()` returns both profiles and the verdict string. Note what the artifact does not do: it does not tune the reranker until it wins. Tuning a stage against the same 26 questions until the table flips is overfitting with extra steps, and Lesson 19's golden set hygiene section names it as such.

## Common failures

- **Judging a reranker on one metric.** Fact at 1 improved while the set degraded. Report the profile, and know which profile your generator actually consumes.
- **Reranking a tiny candidate set.** Reordering a top 3 can only demote; the second pass needs depth (here 10) to have anything to promote.
- **Keeping a stage because it is standard.** Every stage costs latency and a failure surface. A stage that does not move your golden set's profile is a liability wearing a best practice costume.

## Recap checklist

- [ ] I can recite the reranker's profile against raw hybrid on all five metrics.
- [ ] I can explain why the reranker helps fact at 1 while hurting the set.
- [ ] I have a keep or drop rule I could apply to a production cross-encoder.

## Resources

- [Course glossary](../resources/glossary.md)
- [RESEARCH.md](../RESEARCH.md): the platform courses present reranking inside managed stacks; this lesson is the manual version
