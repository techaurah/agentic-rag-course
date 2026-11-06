# Lesson 15: Query rewriting and vocabulary bridging

**Time:** about 60 minutes · **Difficulty:** Intermediate · **Prerequisites:** Lesson 07 · **You need:** Your three gap questions from Lesson 07's exercise.

Lesson 07 measured the vocabulary gap: BM25 scored 0.6667 on questions written in the asker's words. This lesson applies the oldest fix in search: rewrite the query into the corpus's vocabulary before retrieving. The instrument is a small curated synonym table, seven rows built from the gap set's failures, each row a pair a human chose (receipt to proof of purchase, greenfly to aphids, flagship to Fernbrook, rewards to points, opening to opens hours, charge to delivery costs, house to home). Rewriting appends the mapped terms to the question; the original words stay, so a bad row can dilute but rarely destroys.

## The measured verdict

Gap set, fact recall at 5. BM25: 0.6667 before, 1.0 after. Hybrid: 0.8333 before (the vector leg rescues the delivery charge question on its own), 1.0 after. And the safety check that separates engineering from demo tricks: the golden set under the same rewriting is unchanged, BM25 fact recall 0.9615 before and after. The table fixes exactly the failures it was built from and does no harm elsewhere, because its rows are specific pairs, not vibes. That specificity is also its ceiling: the table knows seven bridges because a human read seven failures. It will not know the eighth until a user hits it, which is why production rewriting pairs the table with failure logging (every zero recall real question is a candidate row) and why Lesson 17 examines the automatic alternatives and their honest costs.

## Where tables come from

Support tickets, chat transcripts, search logs with zero results, and your own gap set: the sources are always the asker's actual words. Build rows from observed failures, one pair at a time, and rerun both sets after each row; a row that lifts the gap set but dents the golden set is a bad row wearing a good story. Note the flagship row's lesson within the lesson: Fernbrook is this corpus's private name for its main store. No embedding model and no general thesaurus contains it. Private vocabulary (product names, internal codes, local terms) always needs the table, whatever else your stack does.

## Run it

Run `python3 rewriting.py`. `evaluate()` returns the four gap numbers, the golden no-harm pair, and the row count. Add the rows your Lesson 07 exercise questions need, one at a time, rerunning after each: the discipline is the deliverable.

## Common failures

- **Rewriting by replacement instead of expansion.** Swapping the asker's word for yours deletes signal when your guess is wrong. Append; let the retriever arbitrate.
- **Unbounded synonym lists.** A row per imagined pair dilutes queries and drifts rankings on questions that were working. Rows are earned from observed failures only.
- **Letting an LLM rewrite freely with no record.** Generated rewrites can help (Lesson 17), but an unlogged, unmeasured rewrite step makes failures undebuggable. Log the rewritten query beside the original, always.

## Recap checklist

- [ ] I know the gap set's before and after numbers for both retrievers (0.6667 to 1.0; 0.8333 to 1.0).
- [ ] I verified rewriting does no harm on the golden set (0.9615 both ways).
- [ ] I can name where table rows legitimately come from, and the private vocabulary argument.

## Resources

- [Course glossary](../resources/glossary.md)
- [DeepLearning.AI, Advanced Retrieval for AI with Chroma](https://www.deeplearning.ai/courses/): query expansion taught from the framework side (RESEARCH.md)
