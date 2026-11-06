# Lesson 05: TF-IDF from scratch: tokenisation and term statistics

**Time:** about 90 minutes · **Difficulty:** Beginner · **Prerequisites:** Lessons 02 to 04 · **You need:** Nothing extra; the artifact is the lesson.

TF-IDF is the oldest idea in this course and still the skeleton inside half the retrieval you will ever debug. This lesson builds it completely: a tokenizer, term frequencies, inverse document frequencies, sparse vectors, and cosine similarity, then measures it as the course's first real retriever over paragraph chunks.

## Tokenisation decides more than scoring does

The course tokenizer lowercases, extracts word and number pieces (keeping times like 5:30 and prices like 6.95 intact as single tokens, because "5:30" split into "5" and "30" is a fact destroyed), drops a stopword list (the, and, of, and their friends, words that appear everywhere and discriminate nothing), and drops single characters. Every choice here is a retrieval decision: a tokenizer that splits on the colon cannot answer "what time does it close", and a stopword list that dropped "not" would make "does not have a cafe" indistinguishable from its opposite. When a real system misretrieves, read its tokens before its scores.

## The scoring idea

Each chunk becomes a sparse vector: for each term, its count in the chunk weighted by the term's inverse document frequency, log((N + 1) / (df + 1)) + 1, where df is the number of chunks containing the term. Rare terms (aphids, in a handful of chunks) get high weight; common terms (plants, everywhere) get low weight. The artifact prints both IDF values so you can feel the spread. A question becomes a vector the same way, and ranking is cosine similarity: the angle between question and chunk vectors, which normalises for chunk length so a long chunk cannot win just by containing more words.

## The verdict

Over paragraph chunks with role filtering, TF-IDF scores document recall at 5 of 0.9808, fact recall at 5 of 0.9808, and MRR of 0.8731. Read those three numbers the course's way: recall says the right chunk is almost always in the top 5; MRR says it is not always first, and the gap between 0.98 recall and 0.87 MRR is the ranking work Lessons 06, 11, and 13 will do. Its worst question scores fact recall 0.5: one question where the facts split across chunks the ranking only half finds. TF-IDF's known blindness is vocabulary: it matches the words in the question against the words in the chunk, exactly, and Lesson 07 will catalogue what that costs.

## Run it

Run `python3 tfidf.py`. `evaluate()` returns the stage table plus the index's vocabulary size and the two example IDF values quoted above. Change one tokenizer rule (drop the stopword filter) and rerun: watching fact recall and MRR move is the fastest way to learn what the filter was doing.

## Common failures

- **Splitting numbers and times.** If your tokenizer turns "6.95" into "6" and "95", price questions retrieve any chunk containing a 6. Protect decimal and time shapes in the token pattern.
- **Forgetting length normalisation.** Without cosine normalisation, the longest chunk wins every broad question; the FAQ and the welcome pack would outrank every precise policy.
- **Treating IDF as a constant of nature.** IDF is computed from your corpus; the same term weighs differently in another corpus. Any code that hardcodes term weights has hidden a corpus assumption.

## Recap checklist

- [ ] I can build a TF-IDF vector by hand for a two sentence chunk.
- [ ] I know the stage table for TF-IDF on this corpus, and what the recall to MRR gap means.
- [ ] I can name the tokenizer decisions and one question each one protects.

## Resources

- [Course 1, Lesson 18: RAG from scratch](https://github.com/techaurah/agentic-ai-for-beginners): the same TF-IDF index in its first form
- [Course glossary](../resources/glossary.md)
