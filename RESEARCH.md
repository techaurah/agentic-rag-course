# Competitor research: learning retrieval augmented generation

Written 2026-11-06, before any lesson was drafted, per the
TechAurah GitHub programme rule: competitor research first,
always. Every fact below was observed in web search results or
pages fetched on that date. Enrolment counts, star counts, and
catalogue details are point in time observations from the named
source, not live guarantees, and vendor claims are recorded as
vendor claims.

## The platform courses: strong, gated, and stack bound

- **DeepLearning.AI, Retrieval Augmented Generation (RAG)**
  (Coursera, instructor Zain Hasan of Together AI): the most
  complete single RAG course in this scan. Five modules,
  roughly 26 hours, covering RAG architecture, keyword and
  semantic search, vector databases, chunking and reranking,
  generation, and production, with a graded programming
  assignment per module (course page and reviews read
  2026-11-06; the Coursera page showed about 57,000 enrolled
  learners). The first module previews free; the certificate
  is paid through Coursera. Strength: completeness and grading.
  Gap for us: it needs intermediate Python plus a vendor stack
  and API access from early on, and its numbers are the
  learner's own coursework, not a published, reproducible
  scoreboard the next learner can check.
- **DeepLearning.AI short courses** (learn.deeplearning.ai,
  read 2026-11-06): LangChain Chat with Your Data (Harrison
  Chase, about 1 hour), Building and Evaluating Advanced RAG
  (Jerry Liu of LlamaIndex with Anupam Datta of TruEra, about
  2 hours; sentence window retrieval, auto merging, and
  evaluation with TruLens), Advanced Retrieval for AI with
  Chroma (about 1 hour; query expansion and cross encoder
  reranking), and Building Agentic RAG with LlamaIndex.
  Strength: each is a sharp two hour slice taught by the tool's
  own people. Gap: the slices assume the partner stack, run in
  a hosted lab, and stop where this course's middle begins:
  nobody owns the whole arc from chunking to refusal behaviour
  in one measured system.
- **IBM, RAG and Agentic AI Professional Certificate**
  (Coursera, surveyed via Class Central and review coverage,
  read 2026-11-06): a long programme (about 101 hours by one
  review's module count) ending in a professional certificate,
  plus IBM's shorter Advanced RAG with Vector Databases and
  Retrievers. Strength: credential weight and structure. Gap:
  subscription gated, certificate first, and the retrieval
  internals arrive wrapped in platform tooling.
- **Class Central's best RAG courses list** (classcentral.com,
  read 2026-11-06) rounds up the rest of the platform field:
  Udemy's long LangChain, FAISS and OpenAI course (about 40
  hours), a freeCodeCamp advanced RAG tutorial, DataCamp's
  Retrieval Augmented Generation with LangChain. The pattern
  across the list is consistent: framework first, hosted or
  paid, and evaluation, where it appears, is a late module
  rather than the spine.

## The GitHub collections: deep, and not courses

- **NirDiamant/RAG_Techniques** (github.com, read 2026-11-06):
  the largest RAG tutorial collection in this scan, 42 or more
  runnable notebooks across foundational techniques, context
  enrichment, advanced retrieval (including fusion), query
  enhancement, evaluation (RAGAS, DeepEval, GroUSE), GraphRAG,
  Self-RAG, Corrective RAG, and RAPTOR, with runnable script
  versions of many notebooks and a companion book. Strength:
  unmatched technique breadth, actively maintained. Gaps for
  us: the notebooks are a catalogue, not a curriculum: no
  order, no exercises with solutions, no shared corpus or
  golden set to compare techniques against each other, most
  need an OpenAI API key, and the repository carries a custom
  non-commercial licence rather than an open one, according to
  its licence file as surfaced in search results.
- **langchain-ai/rag-from-scratch** (github.com, read
  2026-11-06): Lance Martin's notebook series in four arcs
  (indexing and basic retrieval, query translation, routing,
  and indexing extras including ColBERT via RAGatouille),
  companion to a well known video series. Strength: the query
  translation arc is the clearest public treatment of rewriting,
  decomposition, and HyDE style expansion. Gaps: notebooks
  assume LangChain, Chroma, and an OpenAI key from the first
  cell; there is no evaluation set, so a learner cannot tell
  whether a technique helped; and framework APIs have moved
  since the notebooks were written, a rot problem this scan met
  repeatedly (see below).

## The framework docs: authoritative, and perishable

- **LlamaIndex and LangChain documentation** (docs and
  tutorials read 2026-11-06): LlamaIndex's one line path,
  VectorStoreIndex.from_documents plus as_query_engine, is the
  fastest route from a folder of documents to an answer, and
  LangChain's composition model (LCEL pipes, the retriever as
  a tool for agents) gives the most control. Both are the right
  tools in production. The teaching problem is churn: secondary
  coverage read in this scan (learnwithparam.com, August 2026)
  records LangChain at version 1.x with legacy chains moved to
  langchain-classic, llama-index-core at 0.14.x with a modular
  package split, and Haystack at 3.0 with renamed generator
  classes, and warns that half the tutorials a learner finds
  use APIs that changed within the year. A course welded to
  those APIs teaches archaeology alongside RAG. This course
  keeps the canonical path on the standard library, where the
  APIs are stable, and teaches the frameworks as dated,
  clearly marked extras in Lesson 10.

## The primary sources the field builds on

- **Anthropic, Introducing Contextual Retrieval**
  (anthropic.com, 2024-09-19; figures as re-reported in
  multiple sources read 2026-11-06): prepending a short
  generated context to each chunk before embedding and BM25
  indexing cut top 20 retrieval failures from 5.7 percent to
  3.7 percent (contextual embeddings), to 2.9 percent (adding
  contextual BM25), and to 1.9 percent (adding a reranker over
  the top 150). Those are Anthropic's numbers on Anthropic's
  data, and this course cites them as exactly that: evidence
  the techniques can pay, never as a promise about the
  learner's corpus. Lessons 13 and 14 teach the mechanisms and
  make the learner measure the local effect.
- **RAGAS** (open source evaluation framework, EACL 2024;
  docs and guides read 2026-11-06): the field's reference
  metrics: faithfulness and answer relevancy grade the
  generation side, context precision and context recall grade
  the retrieval side, most computed with a judge model. This
  course teaches the same split with deterministic, offline
  versions (fact recall, citation coverage, grounding checks)
  in Lessons 18 to 20, and names RAGAS as the tool to graduate
  to when a judge model is available. Guides read in this scan
  note the RAGAS API changed substantially between its 0.1,
  0.2, and 0.4 lines, which is one more reason the course's
  canonical harness is its own small, stable code.

## The gap this course takes

Everything above is either a catalogue without a curriculum,
a curriculum behind an account on someone else's stack, or
documentation that rots with the framework's release cycle.
Nobody in this scan teaches the whole retrieval stack from
scratch, offline, on the standard library alone, over one
small corpus the learner can hold in their head, with one
golden set whose numbers are published, reproducible, and
recomputed by every lesson's own code, and then keeps going
past retrieval into the parts production systems actually
fail on: permissions, freshness, refusal, and cost. That is
the course below. Its corpus is fictional and tiny on purpose:
on 24 documents almost any retriever looks good, and the
course says so in Lesson 01, because the failures that remain
visible at that scale (leaks, stale answers, confident nonsense
on unanswerable questions, multi-hop misses) are exactly the
failures that matter at real scale too.
