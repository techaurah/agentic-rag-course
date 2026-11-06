# Contributing to Agentic RAG

Thank you for considering a contribution. This course stays useful because every lesson runs, every number reproduces, and every claim is checkable. Contributions that protect those properties are very welcome.

## The two-tier rule

- **Small fixes go straight to a pull request.** Typos, a broken link, a clearer sentence, a small code fix with its smoke test still passing: just open the PR.
- **Big changes start with an issue.** A new lesson, a rewritten lesson, a change to the corpus or the golden set, or a new translation language: open an issue first so a maintainer can agree the shape with you before you invest hours. Corpus and golden set changes are big by definition, because every lesson's quoted numbers derive from them.

## What a good contribution looks like

- **Run the code.** If you changed a Python artifact, run it top to bottom, run its lesson's `smoke_test.py`, and run `python3 tools/validate_course.py` and `python3 tools/check_links.py` from the repo root. CI runs the same checks.
- **Numbers come from code.** If your change alters any measured output, update the lesson text to the new output in the same PR, and say in the PR description which numbers moved and why. A PR whose text quotes numbers its code does not produce will be asked to reconcile them.
- **Respect the honesty rules.** No em dashes. No invented statistics. No claims that the stand-in embedder rivals real models. No certificates. New terms get defined or added to resources/glossary.md.
- **Keep the canonical path clean.** Standard library only, offline, no credentials. Library code belongs in a marked extra with its check date, never in a path a smoke test depends on.
- **Fictional data only.** Exercises, examples, and corpus additions use invented businesses and invented people.

## Lesson changes

If you change a lesson's title or folder, update README.md, llms.txt, and PROGRESS.md in the same PR; the three indexes must never disagree. If you change what a lesson teaches, update its exercise and solution to match.

## Translations

See [translations/README.md](translations/README.md). Small translation fixes go straight to a PR; a new language starts with an issue.

## Showcase

Finished capstone systems are added to [showcase/README.md](showcase/README.md) by PR, one row per learner, following the format there. That is a small fix under the two-tier rule; no issue needed.

## Code of conduct

This project follows the [code of conduct](CODE_OF_CONDUCT.md). Be kind, be specific, and assume the person across from you is learning in public, as the course asks everyone to.
