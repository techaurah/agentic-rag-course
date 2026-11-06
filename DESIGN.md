# Course design: Agentic RAG

The design this repository was built to. Research behind it:
[RESEARCH.md](RESEARCH.md). House standard inherited from
Course 1, Agentic AI for Beginners, Course 2, AI Automation
with n8n, Course 3, Build MCP Servers, and Course 4, AI Agents
for Business: numbered lesson folders, every lesson a complete
unit (written lesson, runnable artifact, exercise, worked
solution), no em dashes, no invented statistics, no
certificates. This course is the programme's deep retrieval
course: Course 1's Lessons 18 to 20 introduce RAG and agentic
RAG for agent builders; this course takes the same ground to
production depth and cross links Course 1 wherever the agent
side is the honest next step.

## Title and promise

**Agentic RAG** is a free, complete course that teaches
builders to design, build, evaluate, and harden a
retrieval augmented generation system, from a corpus they can
hold in their head to an agent that decides when to retrieve,
follows evidence across documents, corrects its own retrieval,
and refuses questions the corpus cannot answer, with every
claim in the course measured by runnable code on the course's
own golden set.

## Audience

- Builders who finished Course 1, Agentic AI for Beginners
  (especially Lessons 18 to 20), or who have equivalent
  experience calling model APIs and want the retrieval depth
  Course 1 deliberately did not carry.
- Engineers inheriting a RAG system at work who need to know
  which part is failing and how to prove it.
- Technical founders and consultants who evaluate RAG products
  and want the mechanics, not the marketing.

Not for: total beginners to Python (Course 1 is the on ramp),
and not for anyone shopping for a certificate. There is none;
the evaluated capstone system in the showcase is the artifact.

## Prerequisites

- Python 3.11 or newer, and comfort reading plain Python:
  functions, classes, dictionaries, comprehensions.
- Course 1 Lessons 18 to 20, or equivalent: you know what
  chunking, embedding, and retrieval are for. This course
  rebuilds each from scratch anyway, so the prerequisite is
  familiarity, not mastery.
- No accounts, no API keys, no installs for the canonical
  path. Lessons that show real libraries mark them as optional
  extras, state the offline versus install split in the lesson,
  and keep the standard library twin canonical.

## The arc

One fictional business, Fernhill Garden Centres, a three
store garden centre chain, provides the whole course's raw
material: 24 short documents (policies, guides, sale terms,
a staff only discount policy, a manager only supplier
agreement) and a 32 question golden set with the documents
and facts each answer needs, plus 6 questions the correct
behaviour for is refusal. The corpus is small enough to read
in one sitting, which is the point: when retrieval fails, the
learner can see the document it should have found. Across
the modules the learner measures a naive pipeline's failures,
builds lexical and vector retrieval from scratch, fuses them,
adds permissions, rewriting, decomposition, and evaluation,
turns retrieval into an agent tool with routing, multi-hop,
and self correction, handles freshness and budgets, and
finishes with a complete evaluated system that passes stated
acceptance gates.

## Canonical corpus and golden set design

- `corpus/corpus.json` is the manifest: id, file, title,
  roles (public, staff, manager), updated date, and
  supersession links. The spring sale terms and the offers
  archive are both superseded by the autumn terms; a website
  FAQ paraphrases policies vaguely on purpose, so ranking
  quality is observable.
- Documents are Markdown with section headings, because
  Lesson 04's structure aware chunking needs real structure.
- `corpus/golden.json` holds 32 questions in six types:
  single (8), paraphrase (8), multi-hop (5), freshness (2),
  permission (3), and unanswerable or permission-refusal (6
  marked expect: refuse). Each answerable question names its
  gold documents and the fact strings a correct answer must
  contain; a Lesson 19 audit verifies every fact string
  literally appears in a gold document.
- `corpus/gap_questions.json` holds 6 purpose built
  vocabulary gap questions used by Lessons 07, 15, and 17.
- Every number quoted in a lesson is the output of that
  lesson's own `evaluate()` on this corpus and golden set,
  recomputed when the code runs. Where a technique does not
  help on this corpus (reranking, HyDE stand-in, PRF), the
  lesson reports the negative result and explains why.

## Lesson map: 32 lessons, 10 modules

### Module 0: Start here

| # | Lesson | Builds |
|---|--------|--------|
| 00 | Course setup: what you need, and how this course works | A verified setup: Python checked, the corpus found, and the honesty rules stated |
| 01 | Why naive RAG fails: the five failure modes | A working naive pipeline, and the five measured ways it lets you down |

### Module 1: The corpus and chunking

| # | Lesson | Builds |
|---|--------|--------|
| 02 | Know your corpus: documents, metadata, and the manifest | A corpus audit: counts, roles, dates, and the metadata every later lesson leans on |
| 03 | Chunking from first principles: size, overlap, and boundaries | Three chunkers measured against each other on the same golden set |
| 04 | Structure aware chunking: sections and parent-child retrieval | Section chunks, and the parent expansion tradeoff measured in facts and words |

### Module 2: Lexical retrieval

| # | Lesson | Builds |
|---|--------|--------|
| 05 | TF-IDF from scratch: tokenisation and term statistics | A complete TF-IDF retriever, built line by line and measured |
| 06 | BM25: the lexical workhorse | BM25 implemented and measured, plus a sensitivity check on its two knobs |
| 07 | Lexical failure modes: the vocabulary gap | A failure classifier for lexical retrieval, and the gap set the course reuses |

### Module 3: Vector retrieval

| # | Lesson | Builds |
|---|--------|--------|
| 08 | Vectors and cosine similarity from first principles | Cosine similarity computed by hand, then on the corpus |
| 09 | The hashing embedder: a teaching stand-in for learned embeddings | A deterministic stand-in embedder, measured, with its limits stated plainly |
| 10 | Real embedding models and vector stores (optional extras) | The same index rebuilt with real tools, marked as installs, dated and caveated |

### Module 4: Hybrid search and ranking

| # | Lesson | Builds |
|---|--------|--------|
| 11 | Hybrid search and reciprocal rank fusion | BM25 and vectors fused by rank, measured against each leg alone |
| 12 | Metadata filtering and permissions aware retrieval | Role filters that take restricted leaks from six questions to zero |
| 13 | Reranking: the second pass, measured honestly | Two deterministic rerankers, a measured negative result, and a keep or drop rule |
| 14 | Context assembly and citation discipline | Token budgeted context packs where every item carries its source |

### Module 5: Query understanding

| # | Lesson | Builds |
|---|--------|--------|
| 15 | Query rewriting: bridging the vocabulary gap | A synonym table that takes the gap set from 0.6667 to 1.0, measured |
| 16 | Query decomposition for multi-part questions | Sentence and clause splitting that lifts multi-hop retrieval, measured |
| 17 | HyDE and expansion techniques, with honest caveats | Two expansion methods measured: one neutral, one harmful, both explained |

### Module 6: Evaluation

| # | Lesson | Builds |
|---|--------|--------|
| 18 | Retrieval metrics that matter: recall, precision, MRR | The metric toolkit, implemented once and reused by every later lesson |
| 19 | Building a golden set that tells the truth | The course's own golden set audited: schema, coverage, and fact checks |
| 20 | Answer grounding and refusal: grading the generation side | An extractive answerer that cites everything, grounds everything, and refuses |

### Module 7: Agentic RAG

| # | Lesson | Builds |
|---|--------|--------|
| 21 | Retrieval as a tool: the agent decides | A search tool with a contract, and an agent that skips it for small talk |
| 22 | Routing and adaptive retrieval | A router measured per question type, and the honest case for routing anyway |
| 23 | Multi-hop retrieval: following the evidence chain | Iterative retrieval across two documents, measured against single shot |
| 24 | Self-correction: grade, widen, retry | A grading loop that rescues the two questions the first pass fails |

### Module 8: Production concerns

| # | Lesson | Builds |
|---|--------|--------|
| 25 | Freshness: versioning, staleness, and reindexing | Superseded documents handled by rule, and a reindex diff you can inspect |
| 26 | Cost and latency budgets | Per stage latency measured on your machine, and a cost worksheet with no fake prices |
| 27 | Failure modes in production and the debugging playbook | Every golden miss classified into a playbook entry, with the real q24 case |

### Module 9: Capstone

| # | Lesson | Builds |
|---|--------|--------|
| 28 | Capstone spec: the evaluated RAG system, fixed in advance | The capstone config and its acceptance gates, fixed before any code |
| 29 | Build the capstone system | The full stack assembled into one system that reads the Lesson 28 config |
| 30 | Evaluate and harden the capstone | The harness run end to end, gate by gate, with the failure report |
| 31 | Ship it: document, demo, and showcase your system | A verified demo transcript, a release checklist, and your showcase row |

## Capstone spec (fixed in Lesson 28, built in 29, graded in 30)

The capstone is a complete RAG system over the bundled corpus
plus a folder of the learner's own documents, assembled from
the course's components: paragraph chunking, BM25 and vector
legs fused with reciprocal rank fusion, role filtering,
freshness handling, hybrid retrieval, the grounded extractive
answerer with citations, and the refusal rules. Its config
lives in Lesson 28's `capstone/system.json` and is read by
the Lesson 29 system, so the spec and the build cannot drift.

Acceptance gates, stated in advance and graded by Lesson 30's
harness on the bundled golden set:

| Gate | Threshold | Reference build (measured 2026-11-06) |
|------|-----------|---------------------------------------|
| Document recall at 5, answerable questions | at least 0.95 | 0.9808 |
| Fact recall at 5, answerable questions | at least 0.95 | 0.9808 |
| Citation coverage of composed answers | 100 percent | 26 of 26 |
| Grounding checker passes on composed answers | 100 percent | 26 of 26 |
| Refusals on refuse-expected questions | at least 5 of 6 | 5 of 6 |
| False refusals on answerable questions | 0 | 0 |
| Restricted chunks in public contexts | 0 | 0 |
| Mean latency per question, grading machine | under 50 ms | about 5 ms on the build machine |

The reference values are this build's measured outputs on the
build machine, printed by Lesson 30's harness; they are
reproducible by running the code, and they are not promises
about any other corpus. The one known miss is named in the
course: question q24 (price matching) draws a grounded but
non responsive sentence past the refusal rules, and Lesson 20
uses it to teach the threshold tradeoff explicitly.

## Visuals

Seven diagrams in the TechAurah Academy style (navy, light
blue, cyan, amber), generated by a committed script:
course map, the RAG pipeline, chunking strategies, hybrid
fusion, the evaluation loop, the agentic retrieval loop, and
the capstone flow. See assets/visuals/VISUALS.md.

## Offline versus install-required split

Canonical path: Python standard library only, offline, no
keys. Optional extras appear in Lessons 10 (sentence
transformers, FAISS, LlamaIndex, LangChain), 13 (learned
rerankers), 17 (model written HyDE passages), 20 (RAGAS), and
26 (provider pricing). Every extras section is headed as an
extra, dated 2026-11-06 where it names an API, and states
that the lesson's measured numbers come from the twin.
