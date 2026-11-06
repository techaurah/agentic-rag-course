# Lesson 06: BM25: the lexical workhorse

**Time:** about 75 minutes · **Difficulty:** Beginner · **Prerequisites:** Lesson 05 · **You need:** The TF-IDF numbers from Lesson 05 for comparison.

BM25 is the ranking function inside most production search engines' lexical leg, and the correct default for word based retrieval. It keeps TF-IDF's insight (rare terms discriminate) and fixes its two crudities: term frequency saturates, and chunk length is normalised explicitly rather than by the cosine's side effect.

## The two fixes

Saturation: in TF-IDF, a chunk mentioning "guarantee" ten times scores ten times a chunk mentioning it once. In reality the second mention adds little; BM25's term frequency component, f(k1 + 1) / (f + k1), asymptotes, so repetition stops paying. Length normalisation: a chunk's term frequencies are adjusted by its length relative to the corpus average, governed by b: at b = 0.75 (the textbook default, with k1 = 1.5), a chunk twice the average length needs proportionally more evidence to score the same. BM25's IDF variant, log(1 + (N - df + 0.5) / (df + 0.5)), also stays positive for terms in more than half the corpus, where the classic formula goes negative.

## The verdict, and the honest comparison

BM25 over paragraph chunks: document recall at 5 of 0.9615, fact recall at 5 of 0.9615, MRR of 0.9359. Against Lesson 05's TF-IDF (0.9808, 0.9808, 0.8731): BM25 ranks notably better (MRR up by about 0.06: the right chunk is first more often) while recalling a shade less at 5, because one multi-hop question loses its second document below the cut. Neither dominates; they fail differently, which is the first hint of Lesson 11's fusion argument. The sensitivity sweep is the second honest result: across k1 in {1.2, 1.5, 2.0} and b in {0.5, 0.75, 1.0}, fact recall at 5 does not move at all on this corpus (0.9615 everywhere). On 84 short chunks the knobs have almost nothing to bite on. Record that before touching them on any real system: parameter tuning without a golden set that can register the change is theatre.

## Where BM25 sits in the stack

BM25 is fast (an inverted index in production; here, a direct scan that is still milliseconds at this scale), exact (numbers, codes, and names match perfectly, which is why quantity questions love it), and completely blind to meaning: it cannot know that "greenfly" and "aphids" are the same problem. That blindness is Lesson 07's catalogue and the motivation for both the vector leg (Lesson 09) and rewriting (Lesson 15).

## Run it

Run `python3 bm25.py`. `evaluate()` returns BM25's stage table and the five point sensitivity sweep. Find the one question where BM25's fact recall is 0.0 (its worst): it is a multi-hop question, and Lesson 16 exists because of questions like it.

## Common failures

- **Tuning k1 and b by vibes.** The sweep shows a flat line on this corpus. On yours it may not be flat, but only a golden set can tell you; default to 1.5 and 0.75 until yours speaks.
- **Comparing retrievers on one number.** BM25 versus TF-IDF flips depending on whether you read recall or MRR. Report the table, not a winner.
- **Indexing different text per retriever.** Comparisons are only honest when every retriever indexes the same chunk text (here: title, section, body). Change the text and you have changed two variables.

## Recap checklist

- [ ] I can explain saturation and length normalisation in one sentence each.
- [ ] I know BM25's stage table and how it differs from TF-IDF's, number for number.
- [ ] I measured the sensitivity sweep and can say what it proves about tuning on small corpora.

## Resources

- [Course glossary](../resources/glossary.md): BM25, saturation, and the metric definitions
- [RESEARCH.md](../RESEARCH.md): how the platform courses present BM25 inside their stacks
