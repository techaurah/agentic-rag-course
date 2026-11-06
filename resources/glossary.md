# Glossary

Every term this course uses, defined in plain language, in
the order a learner meets them.

**Retrieval augmented generation (RAG).** Answering a question
by first searching your own documents, then generating the
answer from what the search found, instead of from the model's
memory alone.

**Corpus.** The set of documents a system may search. In this
course, the 24 Fernhill documents in `corpus/`.

**Chunk.** A piece of a document, cut for indexing. Retrieval
returns chunks, not whole documents.

**Chunking.** The discipline of cutting documents into chunks:
size, overlap, and whether cuts respect structure.

**Parent-child retrieval.** Retrieving with small chunks for
precision, then handing the generator the larger section each
small chunk came from, for context.

**Token.** For this course's tokenizer, a lowercase word or
number piece, with stopwords removed. Not the same as a model
token, though the budget lesson uses words as a proxy for both.

**Stopword.** A word the tokenizer drops because it carries no
retrieval signal: the, and, of, and their friends.

**Term frequency (TF).** How often a term appears in a chunk.

**Inverse document frequency (IDF).** A rarity weight: a term
in few chunks is worth more than a term in every chunk.

**TF-IDF.** The classic sparse vector: term frequency weighted
by inverse document frequency, compared with cosine similarity.

**BM25.** The standard lexical ranking function. TF-IDF's
successor in practice: it saturates term frequency (the tenth
mention counts for little) and normalises for chunk length.

**Lexical retrieval.** Retrieval by the words themselves:
TF-IDF and BM25. Exact, fast, blind to synonyms.

**Embedding.** A list of numbers (a vector) produced by a model
so that texts about similar things get similar vectors.

**Vector retrieval.** Retrieval by embedding similarity:
embed the question, find the nearest chunk vectors.

**Hashing embedder (stand-in).** This course's deterministic
teaching substitute for an embedding model: signed feature
hashing over words and character trigrams. It captures
morphology, not meaning, and is always labelled a stand-in.

**Cosine similarity.** The angle between two vectors, used as
their similarity score. One means same direction.

**Hybrid retrieval.** Running lexical and vector retrieval
together and combining their results.

**Reciprocal rank fusion (RRF).** Combining ranked lists by
rank position rather than raw score, so different retrievers'
score scales never mix.

**Metadata filter.** Restricting retrieval to chunks whose
metadata passes a rule: a role, a date, a store, a document
kind. Permissions are metadata filters enforced before ranking.

**Reranking.** A second scoring pass over a shortlist, using a
more expensive or more specific scorer than the first pass.

**Context assembly.** Building the exact text handed to the
generator: which chunks, in what order, under what token
budget, with what citation labels.

**Citation.** A pointer from an answer sentence to the chunk
it came from, named so a reader can check it.

**Grounding.** The property that every claim in an answer is
supported by the cited evidence. This course checks it
mechanically for extractive answers.

**Extractive answer.** An answer composed of sentences copied
from the evidence, rather than newly generated text. The
course's offline substitute for a generation model.

**Refusal.** The system's deliberate non-answer when the
corpus cannot support one. A feature, graded like any other.

**Golden set.** A fixed set of questions with known correct
documents and facts, used to measure a system the same way
every time.

**Recall at k.** Of the documents (or facts) a question needs,
the fraction present in the first k retrieved chunks.

**Precision at k.** Of the first k retrieved chunks, the
fraction that are actually relevant.

**MRR (mean reciprocal rank).** Averaged over questions, one
divided by the rank of the first relevant chunk. Rewards
putting the right chunk first.

**Fact recall.** Recall measured on the fact strings an answer
must contain, rather than on documents. Stricter than document
recall, and closer to what generation needs.

**Query rewriting.** Changing the question before retrieval:
expanding synonyms, normalising terms, bridging the gap
between the asker's words and the documents' words.

**Query decomposition.** Splitting a multi-part question into
subquestions, retrieving for each, and combining the evidence.

**HyDE.** Hypothetical document embeddings: generate a fake
answer passage, embed that, and retrieve against it. The
course's template stand-in adds no new vocabulary, and
Lesson 17 measures the consequence honestly.

**Pseudo relevance feedback (PRF).** Expanding a query with
terms from its own top results. Powerful when the top result
is right, drifting when it is wrong; Lesson 17 measures both.

**Agentic RAG.** Retrieval as a tool an agent may call, skip,
repeat, or reformulate, inside its decision loop, instead of
a fixed pipeline step.

**Routing.** Choosing a retrieval strategy per question, by
its type or features, instead of one strategy for everything.

**Multi-hop retrieval.** Retrieval in rounds, where facts from
the first round's evidence decide what the second round asks.

**Self correction.** A loop that grades its own retrieval,
and on a failing grade changes something (wider k, a rewrite)
and tries once more.

**Freshness.** Whether the corpus reflects the world as it is
now: superseded documents, updated dates, reindexing.

**Superseded document.** A document replaced by a newer one,
kept for the record and for questions about its own period.

**Judge model.** A model used to grade answers, as in the
RAGAS metrics. This course's harness is deterministic
instead; Lesson 20 explains what a judge adds and costs.
