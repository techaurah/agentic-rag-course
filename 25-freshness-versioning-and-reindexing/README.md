# Lesson 25: Freshness, versioning, and reindexing

**Time:** about 60 minutes · **Difficulty:** Intermediate · **Prerequisites:** Lessons 02 and 14 · **You need:** The manifest's supersession links from Lesson 02.

Documents change. Prices move, sales end, policies are revised, and a retrieval system that cannot tell current from stale will quote last season's terms with this season's confidence. This lesson builds the freshness layer: supersession metadata in the manifest, a filter that keeps superseded chunks out of contexts unless the question names their period, and a reindexing discipline priced by an actual edit.

## The filter, measured

Across the 26 answerable questions' top 5 contexts, chunks from superseded documents (the spring sale terms and the offers archive) appear 10 times with no freshness handling. With the filter, that falls to 3, and the remaining 3 are the lesson's precision point: all belong to q18, which asks about the spring sale by name, and for that question the spring document is not stale, it is the answer. Freshness is therefore not deletion and not a global demotion; it is a question relative rule (superseded documents answer questions about their own period and no others), implemented where Lesson 14 assembles the pack. The alternative designs fail characteristically: deleting the spring document makes q18 unanswerable (history questions are legitimate), and date boosting alone still lets a strongly worded stale chunk outrank the current one on non date questions.

## Versioning and the reindex

Every document carries an updated date in the manifest, printed in every citation label (Lesson 14), so an answer's evidence is versioned in the open. When a document changes, the index must change exactly as much as the document did: the artifact simulates the delivery charge moving from 6.95 to 7.50 and diffs the chunk sets. Exactly 1 of 84 chunks changes (the chunk carrying the charge), so an incremental reindex re-embeds and re-posts 1 chunk, not the corpus. The discipline that makes this safe: chunks are content addressed by document and position, unchanged chunks keep their ids, and the golden set reruns after every reindex, because an index change is a retrieval change and Lesson 18's harness is the only thing that can say whether it was a safe one. Full reindexes remain necessary on chunker or embedder changes (Lesson 10's warning about mixing embedding spaces), and the version stamp to record is the triple: corpus version, chunker version, embedder identity.

## Run it

Run `python3 freshness.py`. `evaluate()` returns the stale counts (10 to 3), the simulated edit's blast radius (1 chunk), and the corpus size it was priced against (84). Try the same diff with a chunk target change instead of a text edit and watch the blast radius become the whole corpus: that contrast is the versioning policy in one experiment.

## Common failures

- **Deleting superseded documents.** History questions exist, audits exist, and "what were the terms in spring" is a fair question. Demote by default, serve on request, never delete.
- **Freshness by date alone.** The newest document is not always the governing one (a future dated announcement should not displace current terms). Supersession is an explicit relation, not a timestamp race.
- **Reindexing without regrading.** Any index change can move rankings. The golden set runs after the reindex, before users do.

## Recap checklist

- [ ] I know the stale counts (10 to 3) and why the remaining 3 are correct.
- [ ] I can price a one fact edit's reindex (1 of 84 chunks) and name the change that costs a full reindex.
- [ ] I can state the version triple worth recording.

## Resources

- [Course glossary](../resources/glossary.md)
- [Lesson 02](../02-know-your-corpus/README.md): where the supersession metadata is born
