# Lesson 04: Structure aware chunking: sections and parent-child retrieval

**Time:** about 60 minutes · **Difficulty:** Beginner · **Prerequisites:** Lesson 03 · **You need:** A corpus document open, to see its sections.

Lesson 03's packing respected headings as break points but threw the structure away after cutting. This lesson uses the structure twice: first by making the section itself a chunking unit, and then with the pattern production systems call parent-child retrieval: search over small chunks for precision, but hand the generator the larger parent section each hit came from, so the answer is composed with the surrounding sentences that give a fact its conditions.

## Why structure is information

A paragraph that begins "It opens Monday to Saturday from 9:00 until 5:30" is ambiguous until you know it sits under the heading "Millfield store". The heading is not decoration; it is half the fact. Section chunking keeps heading and body together as one unit, and the index text for every chunker in this course includes the document title and section name, so retrieval can match on the heading's words too. When you design chunking for a real corpus, inventory its structure first (Lesson 02's audit counted the sections): headings, list items, table rows, FAQ pairs, and code blocks are all natural units, and each maps to a chunker.

## Parent-child, measured

The artifact retrieves with BM25 over paragraph children (top 5), then expands each hit to its parent section and remeasures. The measured result on this corpus is a tie, and the tie is the lesson: child fact recall at 5 is 0.9615, parent expanded fact recall at 5 is 0.9615, and average context is 118 words both ways. The reason is visible in Lesson 02's audit: Fernhill's sections are single paragraphs, so for most chunks the parent section IS the child, and expansion has nothing to add. Parent-child retrieval pays when sections are long and a fact's conditions live in a different paragraph of the same section than the fact itself (the classic case: "yes, guaranteed" retrieved without "hardy plants, 12 months", stated two paragraphs later). On a corpus like this one it is insurance you can measure and decline; on a corpus of long policy documents it is often the difference between an answer and a correct answer. The decision rule is the course's usual one: expand on your golden set, keep the expansion only if fact recall or answer correctness moves by more than the extra context costs.

## Where structure aware chunking breaks

Three honest limits. Sections vary in length: one Fernhill section is a sentence, another is half the document, and a chunker that trusts headings inherits the variance. Documents without headings (transcripts, emails, scanned text) offer no structure to exploit, and fall back to Lesson 03's packing. And structure can lie: a "miscellaneous" section is a junk drawer whose chunks retrieve against everything and mean nothing. The craft is matching the chunker to the corpus you audited, and the measurement habit from Lesson 03 is how you verify the match.

## Run it

Run `python3 structure_chunking.py`. `evaluate()` returns the child and section counts (84 and 84 here), fact recall at 5 for children alone and for parent expanded contexts (0.9615 both), and the average context words of each (118 both). Lesson 14's budgets revisit the expansion decision with a cost column attached.

## Common failures

- **Indexing the body but not the heading.** If the section name is not in the indexed text, "Millfield closing time" cannot match the section that answers it. Index title and section with the body.
- **Expanding to the whole document.** Parent means the section, not the document; whole document expansion is Lesson 01's bloat wearing a smarter name.
- **Trusting headings blindly.** Audit section length variance before adopting section chunking; a corpus whose sections run to 2,000 words needs packing inside sections, which is exactly the course's standard chunker with headings as break points.

## Recap checklist

- [ ] I can explain what a heading contributes to a chunk's meaning, with the Millfield example.
- [ ] I measured parent expansion on this corpus, can explain why it ties here, and can name the corpus property that would make it pay.
- [ ] I can name the three ways structure aware chunking breaks and the fallback for each.

## Resources

- [LlamaIndex documentation](https://docs.llamaindex.ai): node parsers and auto merging retrieval are this lesson's pattern in framework form (dated extra, Lesson 10)
- [Course glossary](../resources/glossary.md)
