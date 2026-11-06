# Lesson 07: Lexical failure modes: the vocabulary gap

**Time:** about 60 minutes · **Difficulty:** Beginner · **Prerequisites:** Lessons 05 and 06 · **You need:** The gap set, `corpus/gap_questions.json`, open beside the lesson.

Lexical retrieval matches words, so its failures are word shaped. This lesson builds the habit that separates debugging from guessing: for every imperfect result, name the failure before reaching for a fix. The artifact classifies BM25's imperfect golden questions by cause, then introduces a second, crueller test set that the rest of the course keeps returning to.

## A taxonomy of lexical failure

**Document missing.** The gold document never reaches the top 5. Either the question's words barely occur in it (vocabulary), or competitors crowd it out (ranking). **Fact not in top chunks.** The right document arrives, but the chunk carrying the fact does not: a chunking or within-document ranking problem. **Vocabulary gap.** The asker and the document use different words for the same thing, so the overlap the scorer needs never happens. The classifier in the artifact separates the first two mechanically; the third is diagnosed by reading, which is why the lesson makes you read.

On the golden set, BM25 is imperfect on very few questions (the artifact lists them; on the reference build it is the multi-hop questions whose second document slips below the cut). The golden set, written in the documents' own vocabulary, is kind to lexical retrieval. Real users are not kind.

## The gap set: questions in the asker's words

`corpus/gap_questions.json` holds six questions written the way people actually ask: "bring something back" for a return, "lost the receipt" where the policy says "proof of purchase", "greenfly" where the guide says "aphids", "the flagship" where the corpus says "Fernbrook", "rewards" where the programme says "points", "charge for bringing my order to my house" for a delivery fee. BM25's fact recall at 5 on the gap set is 0.6667: two of the six (the receipt and the delivery charge) score zero. Same corpus, same retriever, same facts: only the wording changed, and a third of the system's competence evaporated. That is the vocabulary gap, measured.

## Why this lesson sits here

Three different repairs are coming, and they are not interchangeable. Vector retrieval (Lesson 09) softens the gap where words share shape or context, but a hashing stand-in cannot know greenfly are aphids, and the lesson will say so with numbers. Query rewriting (Lesson 15) attacks the gap directly with a synonym table, and takes the gap set to 1.0. Decomposition (Lesson 16) fixes the multi-hop misses, a different cause entirely. Keeping the causes separate is what lets you pick the repair that matches the failure, instead of adding machinery until something moves.

## Run it

Run `python3 vocab_gap.py`. `evaluate()` returns the imperfect golden questions with their classified causes, and the gap set's per question scores: [0.0, 1.0, 0.0, 1.0, 1.0, 1.0] on the reference build, mean 0.6667. Read the two zero questions beside their gold documents and name the missing shared words yourself before Lesson 15 fixes them.

## Common failures

- **Fixing ranking when the cause is vocabulary.** No reweighting of shared words helps when there are no shared words. Diagnose first.
- **Testing only in the documents' vocabulary.** A golden set written by the team that wrote the documents flatters lexical retrieval exactly as this course's main set does. Add asker worded questions, support tickets, and chat logs to yours.
- **Calling every miss a retrieval failure.** "Fact not in top chunks" is a chunking failure wearing retrieval's clothes; the fix lives in Lesson 03, not here.

## Recap checklist

- [ ] I can classify a miss as document missing, fact not in top chunks, or vocabulary gap.
- [ ] I know the gap set's BM25 score (0.6667) and which two questions score zero, and why.
- [ ] I can name the three different repairs coming, and the cause each one treats.

## Resources

- [Course glossary](../resources/glossary.md)
- [RESEARCH.md](../RESEARCH.md): the Advanced Retrieval for AI short course covers the same gap from the query expansion side
