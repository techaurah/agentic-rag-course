# Lesson 31: Ship it: your documents, your system

**Time:** about 60 minutes · **Difficulty:** Intermediate · **Prerequisites:** Lessons 28 to 30 · **You need:** A folder of your own documents for the final exercise.

The last lesson does three things: runs the capstone as a demo and verifies its citations against the corpus itself, maps the road from this reference system to a production one, and hands the system over to your documents, which is where the course was always heading.

## The demo, verified

`ship_check.py` asks five showcase questions: gift card expiry, the current shrub discount, the Gold member multi-hop, the wifi refusal, and the price match question. Four behave exactly as the gates promise, and the fifth is q24's twin: the price match question is answered with a grounded but irrelevant sentence, the known miss, shipped in the demo on purpose. A demo that hides its system's known failure is marketing; a demo that labels it is engineering, and the transcript prints the refusal and the citations in the same format so a reader can check every claim against `corpus/` in minutes. The ship check verifies three of the answered citations mechanically: the answer sentence must appear verbatim in the cited document's text. All three verify.

## The road from here

In the order the course's own measurements argue for. First, a generating composer under the grounding checker, because Lesson 23 and 27 showed composition, not retrieval, is the binding constraint (five of six imperfections live there). Second, your real questions as a growing golden set, with the gap discipline of Lessons 07 and 19, because every later decision prices itself against that set. Third, a real embedder behind Lesson 21's contract, remeasured before adoption (Lesson 10's rule). Fourth, the operational layers this course specified but did not build out: pack logging, per leg monitoring (Lesson 11), router grading (Lesson 22), and the reindex on change pipeline (Lesson 25). Framework adoption, if you choose it, comes after all four, with the golden set already able to grade the framework's pipeline against this one.

## Run it

Run `python3 ship_check.py`. It prints the five question transcript and the verification summary (5 demo questions, 4 answered, 1 refused, 3 citations checked and verified, the known miss flagged). Your course is complete when the transcript your system prints matches these properties on your machine, and when you can explain every line of it with a lesson number.

## Common failures

- **Shipping the demo without the corpus.** The transcript's claims are checkable only because the corpus ships beside it. A demo that cannot be audited is a screenshot.
- **Treating the capstone as the destination.** It is a reference system with a measuring harness. The destination is your corpus, your questions, your gates, run with the same honesty.
- **Removing the known miss from the demo.** The next person to find q24's class in production should find it in your docs first. That is what the label is for.

## Recap checklist

- [ ] My ship check prints the transcript and verifies 3 citations.
- [ ] I can order the post-course road and cite the measurement behind each step.
- [ ] I have a plan for my own documents: manifest, golden questions, gates.

## Resources

- [Showcase](../showcase/README.md): exhibit your finished capstone
- [Course 1, Agentic AI for Beginners](https://github.com/techaurah/agentic-ai-for-beginners): where this course's on-ramp began
- About TechAurah, the team behind this course: [github.com/techaurah](https://github.com/techaurah)
