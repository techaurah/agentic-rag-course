# Lesson 17: HyDE and expansion techniques: promise and caveats

**Time:** about 60 minutes · **Difficulty:** Intermediate · **Prerequisites:** Lessons 09 and 15 · **You need:** Lesson 15's table in mind as the baseline these techniques must beat.

Two fashionable query expansion techniques promise to bridge the vocabulary gap automatically. HyDE (hypothetical document embeddings) has a model write a fake answer passage, then retrieves with the passage, betting that answer shaped text matches documents better than question shaped text. Pseudo relevance feedback (PRF) retrieves once, assumes the top result is relevant, and appends its frequent terms to the query. This lesson implements honest stand-ins for both (a template pseudo document for HyDE, since no model runs in the stdlib core; textbook PRF, which needs no model) and measures them where they should shine. Both disappoint, and the reasons generalise beyond the stand-ins.

## HyDE, measured

On the paraphrase subset with BM25, the template HyDE expansion moves fact recall at 5 from 1.0 to 0.8889: it makes things worse. The mechanism is visible: the template's generic words (policy, details, conditions, prices) are shared by many documents, so the expanded query drifts toward every policy at once. A real HyDE passage, written by a model that knows the domain, carries specific guessed terms (that is its actual bet: the model hallucinates the right vocabulary), and with a real embedding model the passage's semantics do the matching; both advantages are absent from a template, and the lesson says so plainly rather than letting the stand-in's failure libel the technique. The caveat that survives every implementation: HyDE costs a generation call per query, its hallucinated facts can steer retrieval confidently wrong, and it must be measured per question type, exactly as here, before it earns that cost. On this corpus the paraphrase questions were already at 1.0; there was nothing to gain, and expansion had only room to harm, which is the first question to ask any expansion technique: what headroom exists on the questions it targets?

## PRF, measured

On the gap set, PRF moves BM25 fact recall at 5 from 0.6667 to 0.5: g5 (the Millfield coffee question) breaks, falling from 1.0 to 0.0, because its first retrieval is confidently wrong (a cafe chunk from the wrong store), and PRF amplifies the error by feeding the wrong chunk's terms back into the query. That is PRF's structural risk in one number: it assumes the top result is relevant, and on precisely the questions where retrieval is already failing, that assumption is false. Feedback loops compound the first error; Lesson 24's self-correction works because it grades before it trusts, the step PRF skips.

## The standing comparison

Against Lesson 15's seven row table (gap set to 1.0, golden set unharmed, zero per query cost), both automatic techniques lose on this corpus. That is not a universal verdict on HyDE or PRF; it is the course's recurring point in its sharpest form: techniques have conditions, corpora differ, and the golden set, not the literature, decides what ships in your system.

## Run it

Run `python3 hyde_expansion.py`. `evaluate()` returns both before and after pairs and PRF's per question scores ([0.0, 1.0, 0.0, 1.0, 0.0, 1.0] after, against [0.0, 1.0, 0.0, 1.0, 1.0, 1.0] before). Find g5's first retrieval and watch the feedback loop start from a plausible, wrong chunk.

## Common failures

- **Expanding questions that are already perfect.** No headroom means only downside. Target expansion at measured failure classes.
- **Trusting the first retrieval.** PRF's assumption fails exactly where help is needed. Grade first (Lesson 24) or do not feed back.
- **Judging a technique by its paper's corpus.** HyDE's published gains come from specific setups. Your corpus, your golden set, your verdict.

## Recap checklist

- [ ] I know both techniques' measured effects here (1.0 to 0.8889; 0.6667 to 0.5) and the mechanism of each failure.
- [ ] I can state what a real HyDE has that the template stand-in lacks, fairly.
- [ ] I can ask the headroom question about any proposed expansion.

## Resources

- [Course glossary](../resources/glossary.md): HyDE, pseudo relevance feedback
- [RESEARCH.md](../RESEARCH.md): where the platform courses teach these inside advanced RAG modules
