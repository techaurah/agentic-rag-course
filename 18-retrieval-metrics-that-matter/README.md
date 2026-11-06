# Lesson 18: Retrieval metrics that matter

**Time:** about 60 minutes · **Difficulty:** Intermediate · **Prerequisites:** Lessons 05, 06, 09, and 11 · **You need:** The stage tables you have been collecting.

Every lesson so far quoted the same small set of numbers. This lesson makes the set explicit, defines each metric by the decision it informs, and assembles the course's full comparison table in one harness, the one the capstone's gates (Lesson 28) will read from. Metrics are not decoration: each exists because a system failed in a way the others could not see.

## The five, and what each catches

**Document recall at k**: of the documents a question needs, what fraction appear in the top k? It catches coverage failure (the evidence never arrives). **Fact recall at k**: of the facts a correct answer must contain, what fraction appear in the top k chunks' text? It catches the subtler failure where the right document arrives but the fact's chunk does not, and it is the course's primary metric because answers are made of facts, not documents. **Precision at k**: of the top k chunks, what fraction are gold? It catches dilution, the generator's context filling with plausible neighbours (Lesson 13's verdict turned on it). **MRR** (mean reciprocal rank): how high the first gold document ranks, averaged. It catches ranking laziness that recall forgives. **Worst case and below-perfect count**: the minimum fact recall over questions, and how many fall short. They catch the tail, where real users live and averages hide.

## The full table, one harness

TF-IDF: 0.9808 document recall, 0.9808 fact recall, 0.8731 MRR. BM25: 0.9615, 0.9615, 0.9359. Vector stand-in: 1.0, 0.9615, 0.9423. Hybrid: 0.9808, 0.9808, 0.9231. Read across a row for a system's character; read down a column for a metric's opinion. The hybrid's per type breakdown (in the artifact) is where the table earns its keep: single 1.0, paraphrase 1.0, freshness 1.0, permission 1.0, multi-hop 0.9: one type carries all the remaining failure, and Lessons 16 and 23 already know its name. Aggregate scores would have smeared that signal across five types and hidden the target.

## The extras shelf: answer level metrics

Retrieval metrics grade the evidence; answer level metrics grade the reply. The course builds its own in Lesson 20 (citation coverage, grounded sentence rate, refusal accuracy) because they must run offline and deterministically. The field's standard library here is RAGAS (faithfulness, answer relevancy, context precision, context recall, judged by a model), an optional extra requiring installs and API access, with an API that has changed across its 0.1, 0.2, and 0.4 lines (checked 2026-11-06): pin it, and treat its judge scores as a second opinion beside your deterministic checks, never a replacement for a golden set with known facts.

## Run it

Run `python3 metrics_lab.py`. `evaluate()` returns all four stage tables and the hybrid's per type breakdown. This harness is the one Lessons 29 and 30 reuse for the capstone; if you extend the course with a new retriever, this file is where it must report.

## Common failures

- **Reporting recall without the tail.** A 0.98 mean with a 0.0 worst case is a system that abandons one user in fifty entirely. Always print worst and below-perfect.
- **Changing k mid comparison.** Recall at 5 and recall at 10 are different claims. Fix k per comparison (this course: 5) and state it every time.
- **Averaging away the type structure.** Per type breakdowns are where the actionable signal lives. Aggregate for the headline, break down for the work.

## Recap checklist

- [ ] I can define all five metrics by the failure each catches.
- [ ] I can reproduce the four retriever table from the harness.
- [ ] I know where the hybrid's remaining failure concentrates (multi-hop, 0.9).

## Resources

- [RAGAS documentation](https://docs.ragas.io): the answer level metrics library, an optional extra (dated 2026-11-06)
- [Course glossary](../resources/glossary.md)
