# Lesson 02: Know your corpus: documents, metadata, and the manifest

**Time:** about 45 minutes · **Difficulty:** Introductory · **Prerequisites:** Lesson 00 · **You need:** The corpus folder open beside the lesson.

Retrieval quality is decided before any retriever runs, by what is in the corpus, how it is shaped, and what metadata travels with it. This lesson audits the Fernhill corpus the way you should audit any corpus you inherit: count it, read its manifest, check its metadata for completeness, and find its traps while they are still cheap.

## The manifest is the contract

`corpus/corpus.json` carries one entry per document: id, file, title, roles, updated date, and supersession links. Every later mechanism reads it: role filters enforce `roles` (Lesson 12), freshness handling follows `superseded_by` (Lesson 25), citations print `title` (Lesson 14). Metadata that is missing or wrong in the manifest cannot be recovered downstream; a document with no roles entry is a leak waiting for a question. The audit verifies the boring properties that everything else assumes: every document has roles, every document has an updated date, and the supersession links are recorded.

## What the audit finds

24 documents, 2,399 words in total, organised into titled sections: the audit counts 108 headings and sections across the corpus, which Lesson 04's structure aware chunker will use as cut points. The role split is the security story in miniature: 21 documents are public; the staff discount policy carries the staff and manager roles; and the supplier agreement and the trade account terms are manager only, so three documents in all are visible to managers and just one to staff. Two documents are superseded, the spring sale terms and the offers archive, both by the autumn sale terms. The vocabulary is small, 664 distinct content tokens, which is why Lesson 01's naive recall was perfect and why this course grades behaviour, not just recall.

## The traps, catalogued

Four traps are built into this corpus deliberately, because real corpora contain all four by accident. First, the FAQ: a public document that paraphrases policies vaguely ("delivery usually takes a few working days") and competes for rankings while carrying none of the exact facts; it will steal top ranks from precise documents all course long. Second, the offers archive: true statements about ended sales, indistinguishable from current terms by wording alone. Third, topical neighbours: three plant care documents (watering, pests, compost) plus a seasonal calendar and a beginners' guide that all mention each other's subjects, so plant questions must rank five plausible documents correctly. Fourth, the restricted pair, whose contents are exactly the kind of figures (a discount percentage, a trade margin) that questions will ask about by paraphrase.

## Corpus hygiene rules this course follows

Keep documents short and single purpose; the longest Fernhill document is a few hundred words, and each is about one subject, so a chunk is rarely about two. Keep metadata in the manifest, never only in prose: "this sale has ended" written inside the spring document helps a human reader and does nothing for a filter. Date everything. And when a document is replaced, link the supersession in the manifest and keep the old document: Lesson 25 needs it to teach the difference between deleting history and demoting it.

## Run it

Run `python3 corpus_audit.py`. `evaluate()` returns the counts above plus the golden set's type split (single 8, paraphrase 9, multi-hop 5, freshness 2, permission 3, unanswerable 5; one of the paraphrase questions, q20, is the public request for the staff discount figure and expects refusal). If any completeness check returns False, the corpus is broken and later lessons' numbers will not reproduce; fix the manifest first.

## Common failures

- **Metadata in prose instead of the manifest.** A filter cannot read a paragraph. If a property matters (role, date, status), it belongs in structured metadata.
- **Deleting superseded documents.** Deletion erases the answer to legitimate historical questions (golden q18 asks about the spring sale on purpose). Demote, do not delete.
- **One giant handbook document.** A single 200 page handbook makes chunking do all the work and citations useless ("the handbook, somewhere"). Single purpose documents repay their keep at every later stage.

## Recap checklist

- [ ] I can state the corpus's size, role split, and supersession pair without looking.
- [ ] I know the four built-in traps and which lessons they feed.
- [ ] The audit's completeness checks all pass on my copy.

## Resources

- [The corpus README](../corpus/README.md)
- [Course 1, Lesson 07: Working with data](https://github.com/techaurah/agentic-ai-for-beginners): the data handling habits this audit assumes
- [Course glossary](../resources/glossary.md)
