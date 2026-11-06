# AGENTS.md

Conventions for AI assistants working in this repository. Human contributors should read CONTRIBUTING.md; this file states the same rules in machine-checkable form.

## Repository shape

- Lessons live in root folders named `NN-kebab-lesson-name`, numbered 00 to 31, matching the lessons table in README.md exactly. Never rename a lesson folder without updating README.md, llms.txt, and PROGRESS.md in the same change.
- Each lesson folder contains: `README.md` (the lesson), runnable artifacts (plain Python retrievers, rankers, answerers, and harnesses), `exercise.md`, and `solution/` with the worked solution.
- The canonical corpus lives in `corpus/`: documents as Markdown, `corpus.json` (the manifest), `golden.json` (the golden set), and `gap_questions.json`. Lesson artifacts find it by walking up from their own folder; never copy the corpus into a lesson.
- Root files: README.md (landing page), llms.txt (course index for AI assistants), PROGRESS.md (learner checklist), DESIGN.md (the design this repo was built to), RESEARCH.md (the competitor scan), resources/, showcase/, translations/, assets/, tools/.

## Writing rules

- Plain language, short sentences. Define every term on first use or ensure it exists in resources/glossary.md.
- No em dashes anywhere, in prose or code comments. Use commas, colons, or full stops instead.
- No invented statistics, benchmark claims, or market sizes. A number is allowed only as the measured output of the lesson's own code on the bundled corpus and golden set, or as a sourced fact with its date in RESEARCH.md.
- Never claim the hashing embedder matches a real embedding model's quality. It is a teaching stand-in and must be labelled as one wherever it appears.
- Do not promise certificates. The course's completion artifact is the evaluated capstone system in the showcase.
- Lessons never sell a service. The only vendor presence is the published by line and the standard footer in the root README.

## Code rules

- Every Python artifact on the canonical path runs on the standard library (Python 3.11 or newer), offline, with no credentials. Library code (sentence-transformers, FAISS, LlamaIndex, LangChain, RAGAS) appears only inside clearly marked extras that no smoke test and no gate depends on, with its check date stated.
- Every lesson artifact exposes `evaluate()` returning the numbers its lesson text quotes, and `smoke_test.py` asserts them. If code and text disagree, the code's output is the truth and the text gets fixed.
- Every JSON example must parse and pass tools/validate_course.py; golden set entries and the capstone config must carry the fields the validator checks. CI runs it.
- All example data is fictional. The Fernhill corpus is invented for this course; no real business, customer, or patient data anywhere, including in exercises and solutions.

## Change rules

- Small fixes may go straight to a pull request. New lessons, rewritten lessons, and new translation languages start with an issue (the two-tier rule in CONTRIBUTING.md).
- If lesson titles change, update README.md, llms.txt, and PROGRESS.md together; the three must never disagree.
- If the corpus or golden set changes, every lesson's quoted numbers must be recomputed and updated in the same change; CI smoke tests will catch most drift.
- Showcase rows are added by learners via PR, one row per learner, format in showcase/README.md.
