# Lesson 16: Query decomposition: one question, several retrievals

**Time:** about 75 minutes · **Difficulty:** Intermediate · **Prerequisites:** Lessons 11 and 15 · **You need:** The five multi-hop golden questions (q09, q10, q11, q28, q29).

Some questions cannot be answered from one place: "I am a Gold member; do I pay delivery on a 40 pound order?" needs the loyalty document (what Gold means) and the delivery document (the free threshold). A single ranking must surface both, and Lesson 06's worst failure was exactly this shape. Decomposition splits the question into subqueries, retrieves for each, and unions the results. This lesson measures three versions and gets a result every builder should see once: the mechanism works, the naive automation of it does not.

## The three numbers

Document recall on the five multi-hop questions. Single shot hybrid: 0.9 (q29, the Sunday opening plus cafe question, loses one of its two documents). Hand written subqueries with union retrieval: 1.0; every gold document for every multi-hop question is found, because each subquery is a clean single fact question of the kind retrievers answer well. Naive automatic decomposition (split on sentence boundaries and ", and"): 0.8, worse than doing nothing. The artifact shows why: the splitter fires on only one of the five questions, and there it produces a fragment ("have a cafe?") that retrieves mush, while the genuinely two part questions (q09's membership condition, q28's voucher rule) are single sentences whose parts no punctuation separates.

## The lesson inside the lesson

Decomposition quality is the whole game. In production the decomposer is usually a language model prompted to emit subquestions, and it earns its cost exactly when it produces subqueries like the hand written ones: self contained, single fact, in the corpus's vocabulary. A regex cannot do that, and this lesson's 0.8 is what "cannot" looks like measured. Two design rules follow. First, evaluate decomposition on retrieval (document recall over multi-hop questions), not on how plausible the subqueries read. Second, union is not free: it widens the context (Lesson 14's budget applies to the union), and Lesson 23 will show a subtler cost, that better retrieval does not automatically mean better answers when the composer can only pick one sentence.

## Run it

Run `python3 decomposition.py`. `evaluate()` returns the three document recalls (0.9, 0.8, 1.0), the split counts per question, and how many questions the automatic splitter actually split (1 of 5). Read q29's split and q09's non split and predict both outcomes before checking the recalls; the prediction skill is the one you will use on your own decomposer.

## Common failures

- **Decomposing every question.** Single fact questions decomposed into fragments retrieve worse than the original. Gate decomposition on multi-hop signals (multiple facts requested, conditions plus questions), and keep the original query in the union as one of the retrievals.
- **Judging subqueries by eye.** "Sounds reasonable" subqueries scored 0.8 here. Only the union's document recall grades a decomposer.
- **Dropping the union's duplicates carelessly.** The same chunk retrieved by two subqueries is evidence of centrality; dedup by chunk, but consider the double hit a ranking signal rather than noise (Lesson 23 uses plain dedup and reports the consequence honestly).

## Recap checklist

- [ ] I know the three document recalls and can explain each.
- [ ] I can state the two design rules for decomposition.
- [ ] I understand why a language model decomposer still needs a retrieval based evaluation.

## Resources

- [Course glossary](../resources/glossary.md)
- [RESEARCH.md](../RESEARCH.md): the RAG from scratch notebooks cover query translation, the family decomposition belongs to
