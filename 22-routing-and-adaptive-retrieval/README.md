# Lesson 22: Routing and adaptive retrieval: the right effort per question

**Time:** about 60 minutes · **Difficulty:** Intermediate · **Prerequisites:** Lessons 11, 16, and 21 · **You need:** The per type table from Lesson 18.

Not every question deserves the full pipeline. Routing sends each question to the cheapest strategy that answers its kind well: here, single fact and freshness questions go to BM25 alone, and paraphrase, multi-hop, and permission questions get the hybrid. The router in this lesson classifies by the golden set's type labels, which production cannot do; read it as the upper bound study it is (what routing could save if classification were perfect), with the classification problem itself addressed below.

## The measured verdict

Per type fact recall at 5, routed against always hybrid: identical, type for type (single 1.0, paraphrase 1.0, multi-hop 0.9, freshness 1.0, permission 1.0). The saving is cost, not accuracy: average leg invocations per question fall from 2.0 to 1.6154, about a fifth fewer retrievals, because BM25 alone is already perfect on the two types routed to it (Lesson 18's breakdown is what licenses this: you can only route cheaply where a cheap leg is measured equal). Adaptive retrieval's honest pitch is exactly this: same answers, less compute and latency, at the price of a classifier that can misroute. Any routing claim that promises accuracy gains on the routed types should be treated as a measurement error until proven otherwise; the gains live in cost, and occasionally in avoiding a strong leg's characteristic harm (a vector leg's vagueness on exact figure questions is the usual case).

## The classification problem

Production routers classify from the question's surface: length, presence of condition clauses, quantity phrases, named entities, or a small model. Every misroute costs the difference between strategies on that question, so the router's own accuracy belongs on the golden set: extend each golden entry with the strategy it should receive, and grade routing as a classification problem beside the retrieval problem. The safe default matters more than the clever rule: when classification is uncertain, route up (to the hybrid), never down, because the expensive strategy's failure mode is cost while the cheap one's is a wrong answer. Lesson 16's decomposition is routing's sibling (multi-hop questions route to a decomposition strategy in Lesson 23's full loop), and the same grading applies.

## Run it

Run `python3 routing.py`. `evaluate()` returns both per type tables, their equality, and the leg counts (1.6154 against 2.0). Convert legs to your own system's currency: if a leg costs 30 ms or a fraction of a cent per call at your scale, the router's annual saving is arithmetic; its risk is the misroute column you have not measured yet.

## Common failures

- **Routing on vibes.** "Simple questions to the cheap path" without per type measurements is how figure questions end up on the vague leg. Route where a leg is measured equal, nowhere else.
- **No uncertain default.** A router that must choose will sometimes choose down on a hard question. Uncertainty routes up, always.
- **Forgetting the router in evaluation.** A pipeline change that alters per type performance can silently break the routing table's assumptions. The router's grading reruns with the golden set, every time.

## Recap checklist

- [ ] I know the routed and hybrid per type tables are identical here, and the saving is 2.0 to 1.6154 legs.
- [ ] I can state routing's honest pitch (cost, not accuracy) and its misroute risk.
- [ ] I know the uncertain default rule and why direction matters.

## Resources

- [Course glossary](../resources/glossary.md)
- [Course 1, Lesson 22: Routing and orchestration patterns](https://github.com/techaurah/agentic-ai-for-beginners): routing in the wider agent picture
