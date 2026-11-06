# Lesson 00: Course setup: what you need, and how this course works

**Time:** about 30 minutes · **Difficulty:** Introductory · **Prerequisites:** None · **You need:** Python 3.11 or newer.

This course builds a retrieval augmented generation (RAG) system from scratch, measures it honestly at every step, and finishes with an agent that retrieves, grades its own evidence, and refuses what it cannot support. Before any of that, this lesson verifies your setup and walks the raw material, because every later lesson runs on the same corpus and the same golden set, and a broken setup discovered in Lesson 20 costs ten times what it costs here.

## What you need

Python 3.11 or newer, and nothing else for the canonical path. No accounts, no API keys, no package installs: every retriever, embedder stand-in, fusion, answerer, and harness in the course runs on the standard library, offline. A handful of lessons show real libraries (embedding models, FAISS, LlamaIndex, LangChain, RAGAS) as optional extras; each is headed as an extra, dated, and never required. If you finished Course 1, you already have the Python this course needs.

## The raw material: Fernhill Garden Centres

The corpus is 24 short documents for a fictional garden centre chain: store hours, delivery and returns policies, a plant guarantee, a loyalty programme, two sale documents (the spring terms are superseded by the autumn terms), plant care guides, and two restricted documents, a staff discount policy (staff and managers) and a supplier agreement (managers only). It is small enough to read in one sitting, which is the point: when retrieval fails, you can open the document it should have found and see exactly what went wrong. The golden set is 32 questions: 26 answerable ones, each naming the documents a correct retrieval must find and the facts a correct answer must contain, and 6 where the correct behaviour is refusal.

## The honesty rules

Every number in this course is the output of the lesson's own code on this corpus, recomputed when you run it. Lessons expose an `evaluate()` function returning the numbers their text quotes, and a `smoke_test.py` asserting them; CI runs the smoke tests. Where a technique does not help on this corpus, the lesson prints that. Three of the course's techniques produce honest negative results, and they are kept in the course deliberately, because knowing how to detect a technique that is not paying is worth more than one more technique.

## Run it

Run `python3 check_environment.py`. It finds the corpus by walking up from the lesson folder (every artifact in the course locates `corpus/` this way, so lessons run from any working directory), checks your Python, and reports the corpus shape: 24 documents, the golden set's 32 questions split into 26 answerable and 6 refuse-expected, and the three roles, public, staff, and manager.

## Common failures

- **Running artifacts from a copied lesson folder outside the repo.** The corpus lookup walks up from the artifact's own file; a lesson folder copied to your desktop has no `corpus/` above it and will say so. Keep lessons inside the repo tree, or copy the corpus with them.
- **Python older than 3.11.** The course uses current standard library behaviour throughout. `check_environment.py` reports `python_ok: False` rather than failing mysteriously later.
- **Expecting a hosted lab.** There is none, on purpose: the numbers in this course are only trustworthy because you can rerun them yourself, offline, forever.

## Recap checklist

- [ ] `check_environment.py` runs and reports `python_ok: True`.
- [ ] I have read the corpus manifest (`corpus/corpus.json`) and know which two documents are restricted.
- [ ] I can state the honesty rules: every number from code, stand-ins labelled, negatives printed.

## Resources

- [Course 1, Agentic AI for Beginners, Lessons 18 to 20](https://github.com/techaurah/agentic-ai-for-beginners): the RAG introduction this course deepens
- [The corpus README](../corpus/README.md): the manifest, the golden set, and the rules for changing them
- [Course glossary](../resources/glossary.md)
