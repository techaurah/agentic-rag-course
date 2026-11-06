# The Fernhill corpus

The canonical corpus for Agentic RAG: 24 short documents for
Fernhill Garden Centres, a fictional three store garden centre
chain, plus the question sets every lesson is graded on.

## Files

- The documents themselves, one Markdown file each, with
  section headings (Lesson 04 uses the structure).
- `corpus.json`: the manifest. One entry per document: id,
  file, title, roles (who may read it: public, staff,
  manager), updated date, and supersession links. The spring
  sale terms and the offers archive are superseded by the
  autumn sale terms.
- `golden.json`: the golden set, 32 questions. Each entry has
  an id, a type (single, paraphrase, multi-hop, freshness,
  permission, unanswerable), the role asking, the question,
  the gold documents a correct retrieval must find, and the
  fact strings a correct answer must contain. Six entries are
  marked `expect: refuse`: five ask about things the corpus
  does not contain, and one (q20) asks a public reader for a
  staff only figure.
- `gap_questions.json`: six purpose built vocabulary gap
  questions, used by Lessons 07, 15, and 17. Their wording
  deliberately avoids the documents' vocabulary (receipt for
  proof of purchase, greenfly for aphids, flagship for
  Fernbrook).

## Rules for changing this folder

The corpus and the golden set are the course's measuring
instrument. Changing a document changes measured numbers in
many lessons at once. Any change here is a big change under
the contribution rules: it starts with an issue, and the same
pull request must recompute and update every quoted number
it moves. CI smoke tests assert the headline numbers and
will fail until the texts agree with the code again.

Everything here is fictional. No real business, customer, or
employee is described, and the figures (prices, margins,
discounts) were invented for the lessons.
