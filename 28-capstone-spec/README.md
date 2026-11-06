# Lesson 28: Capstone spec: the evaluated Fernhill assistant

**Time:** about 45 minutes · **Difficulty:** Intermediate · **Prerequisites:** All previous lessons · **You need:** The DESIGN.md capstone section, which this lesson operationalises.

The capstone is the course assembled: a complete, evaluated RAG system over the Fernhill corpus, built to a written spec, graded against stated gates, and shipped with its known miss documented. This lesson is the spec. Lessons 29 to 31 build it, grade it, and ship it. Read the spec as a contract: anything not in it is not required, and everything in it is testable.

## The system, specified

`capstone/system.json` in this lesson's folder is the machine readable contract, and the artifact checks its shape. Retrieval: paragraph chunking at a 90 word target; BM25 and vector legs fused by RRF over 20 candidates per leg; role filtering and freshness filtering always on; top 5 into the pack. Generation: the extractive single sentence composer with citations, refusal at unseen threshold 2, pack budget 400 words. Evaluation: the golden set for gates, the gap set reported beside it. Your own documents enter through the same manifest format (Lesson 31 covers adding them), because a system that only works on its teaching corpus has demonstrated nothing about yours.

## The acceptance gates

Eight gates, each traceable to a lesson: document recall at 5 at least 0.95 and fact recall at 5 at least 0.95 (Lesson 18's harness); citation coverage exactly 1.0 and grounded sentences exactly 1.0 (Lesson 20); refusal correct at least 5 of 6, with the known miss documented rather than hidden (Lesson 20); false refusals exactly 0; restricted leaks exactly 0 (Lesson 12); mean end to end latency under 50 ms per question on the grading machine (Lesson 26, set with headroom for a stdlib pipeline). The reference implementation's measured values (recall 0.9808 and 0.9808, refusal 5 of 6, latency in single digit milliseconds) sit inside every gate, and Lesson 30's harness prints the comparison table. Gates are stated before the build for a reason: a spec written after the system exists certifies whatever happened to happen.

## What the capstone is not

Not a chatbot demo, not a framework showcase, and not a claim about other corpora. It is a measurement backed reference system: every design decision in it points at a lesson, and every gate points at a number the harness recomputes. Extending it (your documents, a generating composer, a real embedder behind the same contracts) is the post-course work the final lesson maps.

## Run it

Run `python3 capstone_spec.py`. `evaluate()` validates the spec file and returns the gates. If `spec_valid` is False in your fork, fix the spec before building anything: Lesson 29 reads this file, and a malformed contract fails downstream in confusing places.

## Common failures

- **Gates negotiated after measuring.** That is grading your own homework with the answers visible. Spec first, build second, measure third.
- **A spec that lives only in prose.** The machine readable file is what the build reads and the harness checks; prose explains it, never replaces it.
- **Dropping the known miss from the spec.** q24 is named in the gates' context deliberately. A spec that hides its system's known failure teaches the next maintainer to rediscover it in production.

## Recap checklist

- [ ] I can list the eight gates and the lesson each descends from.
- [ ] The spec checker validates my copy of system.json.
- [ ] I understand the reference values are targets the harness recomputes, not promises.

## Resources

- [DESIGN.md](../DESIGN.md): the capstone design this spec operationalises
- [Course glossary](../resources/glossary.md)
