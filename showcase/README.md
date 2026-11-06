# Capstone showcase

Finished, evaluated RAG systems from learners of Agentic RAG.
This table is the course's completion artifact: no
certificates, just systems anyone can clone, run, and grade
against the same gates.

## How to get your system indexed

1. Finish the capstone (Lessons 28 to 31). Your system must be in a public repository of your own, read its config from a file like Lesson 28's `system.json`, and publish its Lesson 30 gate table in its README: every gate, its threshold, and its measured value, including the gates you miss.
2. Fork this repository and add **one row** to the table below: your name or GitHub handle, a link to your system repository, your headline gate results (document recall at 5, fact recall at 5, refusals), and one line on the corpus you ran it on.
3. Open a pull request titled `Showcase: <your handle>`. Small, single-purpose PRs like this merge directly under the course's [two-tier contribution rule](../CONTRIBUTING.md); you do not need to open an issue first.
4. A maintainer checks that the link works, the gate table is present and complete, and the numbers are the harness's output rather than aspirations. A system that reports a missed gate honestly ranks above one that reports only passes.

One row per learner. If you improve the system and rerun the harness, update your row with a second PR.

## Showcase

| Learner | System | Gate results (doc recall@5, fact recall@5, refusals) | Corpus |
|---------|--------|--------------------------------------------------------|--------|
| _Your name here_ | _Your repository link here_ | _Your measured results here_ | _Be the first row in this table_ |
