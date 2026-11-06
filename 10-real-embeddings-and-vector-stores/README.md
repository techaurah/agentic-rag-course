# Lesson 10: Real embeddings and vector stores (optional extras)

**Time:** about 60 minutes reading, plus install time if you run the extras · **Difficulty:** Intermediate · **Prerequisites:** Lessons 08 and 09 · **You need:** Nothing for the canonical path. The extras need pip installs and, for model downloads, network access.

> **The split, stated once and true for the whole course.** The canonical path is the stdlib stack you have been building: it runs offline, needs no installs, and every number in this course comes from it. This lesson's extras replace the stand-in embedder and the brute force index with real libraries. They are optional, they are dated (written 2026-11-06), and framework APIs change fast enough that you should check the library's own docs before trusting any snippet here. Nothing later in the course depends on them.

## Extra A: a real embedding model

The stand-in's gap is semantics, and a small local model closes much of it. With sentence-transformers installed (`pip install sentence-transformers`), a widely used small model encodes text to dense vectors:

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")  # downloads the model on first use
vectors = model.encode(texts, normalize_embeddings=True)
```

With normalised vectors, cosine similarity is a dot product, and the course's `VectorIndex` interface (embed everything once, rank by similarity) carries over unchanged: only the embedder object is swapped. What changes measurably is exactly Lesson 09's blind spot: paraphrases and synonyms move near each other, so expect the vector leg's paraphrase and gap performance to rise, and verify that expectation on the golden and gap sets rather than believing it. Hosted embedding APIs (from the major model providers) follow the same shape with a key, a bill, and network latency; the swap point in your code should be identical.

## Extra B: a real vector index

Brute force cosine is exact and, at 84 chunks, instant. At a million chunks it is a latency problem, and approximate indexes (FAISS, hnswlib, or a managed vector database) trade a little recall for orders of magnitude of speed:

```python
import faiss
index = faiss.IndexFlatIP(dim)       # exact inner product; HNSW/IVF variants trade recall for speed
index.add(vectors)                   # vectors as float32, normalised for cosine
scores, ids = index.search(query_vector, 5)
```

The professional habit this course wants installed: whichever index you adopt, measure its recall against brute force on your own golden set. An approximate index that loses your gold documents has not saved time; it has moved the cost into answer quality where nobody graphs it.

## Extra C: the framework paths

LlamaIndex and LangChain both wrap this lesson's whole stack (loaders, splitters, embedders, indexes, retrievers, query engines) in a few lines:

```python
# LlamaIndex shape (llama-index-core 0.14.x, checked 2026-11-06)
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
index = VectorStoreIndex.from_documents(SimpleDirectoryReader("corpus").load_data())
answer = index.as_query_engine().query("When does the Millfield cafe open?")
```

```python
# LangChain shape (LangChain 1.x, checked 2026-11-06; LCEL lives in langchain-core)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
# retriever | prompt | model | parser, composed with pipes
```

Frameworks buy speed of assembly and integrations; they cost you visibility. Every failure Lesson 07 taught you to classify still occurs inside them, now behind abstractions you did not write. The course's position: learn the stack bare first (you are doing that), then adopt a framework with your golden set already in hand, and rerun it against the framework pipeline before trusting the swap. RESEARCH.md records how the major platform courses teach framework first, and the churn (LangChain 1.x reorganised its packages; llama-index split into modular distributions) that makes their code samples rot.

## Run it

Run `python3 embeddings_extras.py`. It never imports the extras; it reports which are importable on your machine (`extras_available`), restates that none are required, and returns the canonical stand-in's measured numbers (document recall at 5 of 1.0, fact recall at 5 of 0.9615) as the baseline any extra must beat on this corpus to earn its install.

## Common failures

- **Swapping the embedder without remeasuring.** A real model changes every downstream number, including fusion balance. Rerun the golden set; keep the swap only if the table improves where your users' questions live.
- **Mixing vectors from two models in one index.** Embeddings from different models live in different spaces; cosine across them is meaningless. Reindex fully on any model change (Lesson 25's reindexing discipline).
- **Trusting dated framework snippets.** This lesson's framework code is a shape, checked on 2026-11-06. The library's current docs outrank it, always.

## Recap checklist

- [ ] I can state the offline versus install-required split without notes.
- [ ] I know the baseline an extra must beat on this corpus, and the harness I would prove it with.
- [ ] I understand why the course teaches the bare stack before any framework.

## Resources

- [Sentence Transformers documentation](https://www.sbert.net)
- [FAISS documentation](https://faiss.ai)
- [LlamaIndex documentation](https://docs.llamaindex.ai) and [LangChain documentation](https://docs.langchain.com): current API truth, outranking this lesson's dated snippets
