# Lesson 12: Metadata filtering and permissions: never retrieve what you may not show

**Time:** about 60 minutes · **Difficulty:** Intermediate · **Prerequisites:** Lessons 02 and 11 · **You need:** The manifest's role assignments from Lesson 02.

Lesson 01's worst failure was the leak: restricted documents reaching readers who should never see them. The fix is architectural, and this lesson's title states it: filter before ranking, so a restricted chunk is not a low scored candidate but a non candidate. A generator cannot quote a document it was never handed, and a ranking cannot accidentally surface what the filter removed. Post hoc filtering (retrieve broadly, then delete restricted hits) leaks through counts, snippets, and the simple fact that the model's context window already saw the text in agentic loops. Pre-filtering is the only version that is actually a permission.

## The mechanism

Every chunk carries its document's roles from the manifest. `allowed_for(chunks, role)` returns the chunk indices a role may see, with the natural inheritance of this corpus: public sees 63 chunks, staff sees more (the discount policy joins), manager sees all 84. Both hybrid legs receive the allowed set and rank inside it only. Nothing else in the pipeline changes, which is the design's virtue: permissions live in exactly one place, auditable in a dozen lines.

## The measured verdict

Without the filter, the hybrid pipeline leaks: 6 of the 30 public role questions pull a restricted chunk into their top 5 (fewer than Lesson 01's whole document 11, because chunking concentrates rankings, but six is not a small number of incidents). With the filter, leaks are 0, by construction rather than by luck. The control experiment matters as much as the fix: the manager role must still reach its own documents, and it does: q19 (supplier margin) and q32 (settlement discount) score fact recall 1.0 as manager and 0.0 as public. A filter that "works" by hiding documents from everyone has traded a security bug for an availability bug; the golden set's permission questions exist to catch exactly that trade.

## Permissions are a corpus discipline

The filter is only as good as the manifest: a document uploaded without roles, or with roles copied from a public template, sails through. Production systems default deny (a document with no role metadata is visible to no one until classified), audit role assignments like code, and treat the golden set's permission questions as regression tests that run on every corpus change. Lesson 20 adds the second half of the behaviour: when a public reader asks for the staff figure directly, the correct response is a refusal that does not confirm the figure exists in the form asked, and Lesson 27's playbook covers the incident version.

## Run it

Run `python3 filtering.py`. `evaluate()` returns the leak counts before and after (6 and 0), the two permission checks in both roles (1.0 as manager, 0.0 as public), and the per role chunk counts. If `leaks_filtered` is ever nonzero in your fork, stop: nothing else in the course matters until it is zero again.

## Common failures

- **Filtering after ranking.** The restricted text has already influenced scores, snippets, and any agentic intermediate step. Filter the candidate set, not the output.
- **Default allow metadata.** A new document with missing roles must be invisible, not public. Default deny, and make the audit (Lesson 02) fail loudly on missing roles.
- **Testing only the denial.** Golden sets that check leaks but not legitimate access bless filters that hide everything. Test both directions, as q19 and q32 do.

## Recap checklist

- [ ] I can explain why pre-filtering is a permission and post-filtering is a hope.
- [ ] I verified leaks go 6 to 0 while manager access stays at fact recall 1.0.
- [ ] I know the chunk counts each role sees and where roles come from.

## Resources

- [Course 1, Lesson 20: Grounding and citations](https://github.com/techaurah/agentic-ai-for-beginners): the answer side discipline that pairs with this lesson's retrieval side
- [Course glossary](../resources/glossary.md)
