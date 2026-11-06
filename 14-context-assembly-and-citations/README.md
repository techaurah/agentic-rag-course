# Lesson 14: Context assembly and citations: what the model actually sees

**Time:** about 60 minutes · **Difficulty:** Intermediate · **Prerequisites:** Lessons 11 and 12 · **You need:** Lesson 04's expansion decision in mind.

Retrieval ends and rhetoric begins: the context pack is the exact text a generator will read, and its assembly decides whether answers come with checkable citations or confident fog. This lesson builds the pack deliberately: freshness filtered (the mechanism is Lesson 25's; the pack applies it now), each item labelled with its document title, section, and updated date, the whole pack held under a word budget, and every item carrying the identifiers a citation needs.

## Anatomy of a pack item

Each item is a chunk plus a label line: `[Delivery and Click and Collect | Standard delivery | updated 2026-09-18]`. The label does three jobs. It tells the generator where the text came from, so the answer can cite it. It tells the generator how current the text claims to be, so a stale-looking source can be treated with suspicion. And it tells your future debugging self exactly what the model saw, because the pack, logged whole, is the unit of evidence in every answer dispute. An item without a label is a rumour; the artifact verifies that 122 of 122 items across the golden set's packs carry complete labels (130 chunks retrieved, 8 superseded chunks removed by the freshness filter before labelling), a citation readiness of 1.0, and Lesson 20's grounding checker will refuse to credit an answer sentence that cannot point at one.

## Budgets are a quality feature

The pack budget here is 400 words; the measured average pack is 161 words, and all 26 answerable questions' packs fit. Budgets force the ranking to matter (only so much context survives) and protect the generator from the lost in the middle failure, where relevant text buried in a huge context is effectively absent. Set budgets from your generator's behaviour, not from its context window marketing: a model that accepts 100,000 tokens may still answer best from 400 well chosen words. Anthropic's contextual retrieval work (RESEARCH.md) makes the companion point: prepending a short generated context to each chunk before embedding measurably improved their retrieval, which is the same insight from the other side: chunks travel better with their context attached. This course's labels are the deterministic, no model required version of that idea.

## Order and dedup

Packs preserve fused rank order (generators weight early context), drop chunks whose document was superseded for this question (freshness filter), and never repeat a chunk. Near duplicate chunks from neighbouring documents (the FAQ paraphrasing a policy) are a real corpus hazard the budget partially tames: five slots are precious, and Lesson 27's playbook covers the case where duplicates crowd out the canonical document entirely.

## Run it

Run `python3 context_pack.py`. `evaluate()` returns the budget, the average pack size (161 words), item counts, citation readiness (1.0), and packs within budget (26 of 26). Print one full pack for q17 (the shrub discount question) and read it as the generator would: the current autumn terms labelled and dated, the superseded spring chunk filtered out. That reading experience is the product.

## Common failures

- **Unlabelled context.** Answers that cannot cite are answers you cannot audit, debug, or defend. Labels are cheap; retrofit them before you need them, which is immediately.
- **Budget by window size.** "The model takes 200k tokens" is not an assembly strategy. Measure answer quality against pack size on your golden set, as Lesson 26 does for cost.
- **Logging answers without packs.** When a user disputes an answer, the pack is the evidence. Log the pack with the answer, every time, or accept that the dispute is unwinnable.

## Recap checklist

- [ ] I can name the three jobs a pack label does.
- [ ] I know the measured pack statistics: 161 average words, 26 of 26 within budget, citation readiness 1.0.
- [ ] I can explain the budget as a quality decision, not a model limit.

## Resources

- [Anthropic, Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval): the generated context variant of this lesson's labels, with their measured results
- [Course 1, Lesson 20: Grounding and citations](https://github.com/techaurah/agentic-ai-for-beginners)
