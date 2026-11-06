# Lesson 26: Cost and latency budgets

**Time:** about 60 minutes · **Difficulty:** Intermediate · **Prerequisites:** Lessons 14, 22, and 24 · **You need:** A rough idea of your production question volume; the worksheet adapts.

Retrieval systems fail commercially in two currencies: milliseconds and money. This lesson measures the course pipeline's latency stage by stage on the machine running it, builds the budget worksheet the capstone's gates will enforce, and is deliberately price free: per token and per call prices change quarterly and differ by provider, so the worksheet has blanks to fill from your provider's current pricing page, and any course that printed prices here would be teaching you stale numbers with confidence.

## The latency sheet

The artifact times each stage over the 26 answerable questions: BM25 alone, the vector leg alone, the fused hybrid with filters, and the end to end pipeline including composition. On the build machine these land in single digit milliseconds per question (the artifact prints this run's values; yours will differ, which is the point of measuring rather than quoting). Three budget lessons survive every machine. The legs cost roughly their ranking work and little else at this scale; the filters are free compared to ranking, so Lesson 12 and 25's safety layers are not where latency hides. At production scale the ranking costs move to the index (Lesson 10's approximate indexes exist because brute force cosine grows linearly), and the generation call, absent here because the composer is extractive, dominates everything: a hosted model call costs orders of magnitude more time than this entire pipeline. Budget for the stage that dominates, and remeasure when any stage changes identity (embedder, index, model), not on a schedule.

## The money worksheet

Per answered question, a generated system's cost is approximately: embedding the query (one small call), the generation call over the context pack (input tokens about the pack's words, here about 161 words, plus the answer's output tokens), plus any retry attempts (Lesson 24's measured retry rate, about 0.038, multiplies the retrieval and generation cost of those questions), plus the routing saving (Lesson 22's 1.6154 legs against 2.0) where legs are billed. Fill the unit prices from your provider, multiply by your monthly question volume, and the budget conversation becomes arithmetic instead of anxiety. The two levers that actually move the total are pack size (Lesson 14's budget) and retry discipline (Lesson 24's bound), both already in your hands from earlier lessons.

## Budgets as gates

A budget nobody enforces is a wish. The capstone (Lesson 28) sets a latency gate (mean end to end under 50 ms per question on the grading machine, generous for this stdlib pipeline, impossible to game because Lesson 30 measures it in the harness), and the same pattern extends to money: a cost per answered question ceiling, computed by the harness from the worksheet's filled prices, failing the build when a change (a bigger pack, a looser retry) breaches it.

## Run it

Run `python3 budgets.py`. `evaluate()` returns the four stage timings for this run, the gate, and whether the end to end mean sits within it. Run it twice and note the variance; a budget set inside the noise band of your own measurement is a coin flip, and gates deserve margins.

## Common failures

- **Budgeting from vendor pages.** Your corpus, your pack sizes, your retry rate: measure on your harness. Vendor numbers describe their demo, not your system.
- **Ignoring the retry multiplier.** A 3.8 percent retry rate is small; an unbounded loop's is not. Cost the loop you actually shipped.
- **Latency gates without margins.** Machines vary, neighbours are noisy, and a gate at the edge of variance fails randomly, teaching the team to ignore gates. Set gates with headroom and investigate trends.

## Recap checklist

- [ ] I have this run's four stage timings and know which stage would dominate with a generating model.
- [ ] I can fill the money worksheet for a stated volume and provider.
- [ ] I know the capstone's latency gate and the margin principle behind it.

## Resources

- [Course glossary](../resources/glossary.md)
- Your provider's current pricing page: the only legitimate source for the worksheet's unit prices
