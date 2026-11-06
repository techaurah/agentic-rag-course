# Lesson 19: Building a golden set: questions that can fail you

**Time:** about 75 minutes · **Difficulty:** Intermediate · **Prerequisites:** Lessons 02 and 18 · **You need:** `corpus/golden.json` open; you will read every entry before the lesson ends.

Every number in this course descends from 32 questions. This lesson audits that set the way Lesson 02 audited the corpus, then teaches the design rules for building your own: a golden set is a measuring instrument, and like any instrument it can be miscalibrated in ways that make every later reading wrong.

## The audit

Structure: 32 questions, ids unique, split by type as single 8, paraphrase 9, multi-hop 5, freshness 2, permission 3, unanswerable 5. Annotation quality: every fact string in every entry appears literally in at least one of its gold documents (the audit's missing count is 0), because a fact the gold documents do not contain would grade correct retrievals as failures. Refusal shape: 6 questions expect refusal, and none of them carries gold documents, because "refuse" must mean the system should not answer from evidence, so there must be no evidence to find. Coverage: 14 of the 24 documents appear as gold somewhere; the 10 that never do are the distractors and restricted documents by design (the FAQ, the offers archive, the welcome pack and friends exist to be wrongly retrieved, and their absence from gold is what makes precision measurable).

## Design rules

**Write questions from the asker's side.** Mix document worded questions with asker worded ones (the gap set exists because the main set leans document worded; Lesson 07 showed the cost of pretending otherwise). **Include the negative space.** Unanswerable questions, permission questions in both directions, and stale fact traps are not edge cases; they are the behaviours production incidents are made of, and a set without them certifies systems that leak and confabulate. **Annotate facts, not vibes.** A fact is a literal string a checker can find ("25 percent", "6.95"); "mentions the discount" cannot be graded by code and will be graded by mood. **Keep the set frozen while comparing.** Tuning against a moving set is Lesson 13's overfitting warning at the level of the instrument itself: version the set, change it in reviewed commits, and rerun baselines when it changes. **Size it to the decisions.** 32 questions sufficed to separate every technique in this course because each question targets a behaviour; 300 unfocused questions would have measured less.

## Run it

Run `python3 golden_audit.py`. `evaluate()` returns the audit: 0 missing facts, refusal shape clean, coverage as designed. If you extend the set in the exercise, this audit is your acceptance test; a set that fails it grades nothing.

## Common failures

- **Facts that are not in the gold documents.** Paraphrased annotations ("about 25%") make fact recall unmeasurable. Annotate literally, then audit mechanically, as here.
- **Only happy path questions.** A set of answerable, well worded questions certifies the demo and betrays the deployment.
- **Letting the set drift.** Quiet edits after a bad run are how teams tune the test to the system. Version it; review changes like code.

## Recap checklist

- [ ] I can recite the audit's checks and why each exists.
- [ ] I know the set's type split and coverage design (14 gold documents, 10 deliberate non gold).
- [ ] I can state the five design rules and the failure each prevents.

## Resources

- [Course glossary](../resources/glossary.md)
- [The corpus README](../corpus/README.md): the frozen set policy for this course's own corpus
