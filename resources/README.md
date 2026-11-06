# Resources

Curated resources for Agentic RAG, grouped by theme. Lessons
link to the items they use; this page is the full shelf.
Official documentation first, because it ages best, with the
check date where a page describes a fast moving API. If a
link here breaks, that is a lesson problem: please open an
issue so it gets fixed for everyone.

New to a word? The [glossary](glossary.md) defines every term
this course uses, in plain language.

## The companion shelf (this programme)

- [Agentic AI for Beginners](https://github.com/techaurah/agentic-ai-for-beginners): Course 1. How agents work inside: loops, tools, memory, evaluation, MCP. Its Lessons 18 to 20 are this course's on ramp.
- [AI Automation with n8n](https://github.com/techaurah/ai-automation-with-n8n): Course 2. Workflow automation with validated, forkable workflows.
- [Build MCP Servers](https://github.com/techaurah/build-mcp-servers): Course 3. The tool layer agents use; Lesson 21 of this course treats retrieval as exactly such a tool.
- [AI Agents for Business](https://github.com/techaurah/ai-agents-for-business): Course 4. The commissioning side: choosing, piloting, and supervising agents, for owners and operators.

## Courses and collections surveyed in RESEARCH.md

- [Retrieval Augmented Generation (RAG), DeepLearning.AI on Coursera](https://www.coursera.org/learn/retrieval-augmented-generation-rag): the complete platform course, five modules, graded assignments.
- [DeepLearning.AI short courses](https://learn.deeplearning.ai): LangChain Chat with Your Data; Building and Evaluating Advanced RAG (LlamaIndex and TruEra); Advanced Retrieval for AI with Chroma; Building Agentic RAG with LlamaIndex.
- [RAG_Techniques, by NirDiamant](https://github.com/NirDiamant/RAG_Techniques): 42 or more technique notebooks; a catalogue to mine after this course gives you the measuring habits. Note its custom non-commercial licence.
- [rag-from-scratch, by LangChain](https://github.com/langchain-ai/rag-from-scratch): Lance Martin's notebooks on indexing, query translation, and routing.

## Primary sources

- [Introducing Contextual Retrieval, Anthropic](https://www.anthropic.com/news/contextual-retrieval): the 2024 writeup behind Lessons 13 and 14, with its measured failure reductions (5.7 to 3.7 to 2.9 to 1.9 percent at top 20) on Anthropic's data.
- [RAGAS documentation](https://docs.ragas.io): the reference evaluation framework: faithfulness, answer relevancy, context precision, context recall. Lesson 20 names it as the graduation path from this course's deterministic harness.
- [Python documentation](https://docs.python.org/3/): the standard library every artifact in this course is built on.

## Frameworks, in their own words (APIs checked 2026-11-06; expect drift)

- [LlamaIndex documentation](https://docs.llamaindex.ai): the data first framework; VectorStoreIndex and query engines are Lesson 10's extras.
- [LangChain documentation](https://docs.langchain.com): the composition first framework; LCEL and retriever tools are Lesson 10's extras.
- [Sentence Transformers documentation](https://www.sbert.net): the usual way to run real embedding models locally, Lesson 10's extras.
- [FAISS](https://github.com/facebookresearch/faiss): the vector index library behind many production stores, Lesson 10's extras.

## Going further in this repo

- [resources/glossary.md](glossary.md): every course term, defined plainly.
- The capstone [showcase](../showcase/): finished, evaluated systems from learners, with their gate results.
