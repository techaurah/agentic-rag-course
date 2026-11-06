# Lesson 29: Build the capstone system

**Time:** about 90 minutes · **Difficulty:** Advanced · **Prerequisites:** Lesson 28 and the full course · **You need:** The spec file from Lesson 28, unmodified.

This lesson assembles everything into one system behind one function. `CapstoneSystem.answer(question, role)` returns a cited answer or a refusal, and every component inside it is a lesson you have already measured: paragraph chunking at the spec's target, BM25 and vector legs, RRF fusion, role filtering before ranking, freshness filtering at pack time, the extractive composer with the spec's refusal threshold. The system reads its parameters from Lesson 28's `system.json`, so the spec is not documentation about the system; it is part of the system.

## Assembly notes

Three decisions deserve attention while you build. First, state is built once: indexes, manifest, and document frequencies are construction costs paid at startup (Lesson 21's tool discipline), so `answer()` costs a ranking and a composition, nothing else. Second, role is a parameter of every call, never ambient state, because the same process serves public readers and managers and Lesson 12's guarantee depends on the filter receiving the caller's actual role every time. Third, the answer payload is the contract from Lessons 14 and 21 grown up: the sentence, its citation string, the doc_id for verification, or an explicit refusal marker. A caller never has to guess which of those it received.

## The smoke checks

The artifact's `evaluate()` runs five behavioural checks that preview Lesson 30's gates at unit scale: a delivery charge question answered with its figure; the shrub question answered with the current 25 percent (not the stale 20); the wifi question refused; the supplier margin answered for a manager and refused for the public role. Note the last pair particularly: same question, two roles, opposite correct behaviours, the whole permissions module in one assertion pair.

## Run it

Run `python3 capstone_system.py`. All five checks pass on the reference build. This module is imported by Lessons 30 and 31, so its interface (`CapstoneSystem`, `get_system`, `answer` payload shape) is now frozen; change it and the harness changes with it, in the open, in the same commit.

## Common failures

- **Parameters drifting from the spec.** If the code hardcodes what the spec file states, the spec becomes fiction. Read the file; the harness in Lesson 30 checks gates against the same file, so drift fails loudly there.
- **Ambient role state.** A system object that "remembers" the last role will eventually answer a public question with a manager's context. Role per call, always.
- **Rebuilding indexes per answer.** Construction is startup work. If `answer()` feels slow, profile before optimising; on this stack it will not be the ranking.

## Recap checklist

- [ ] The system answers, cites, and refuses through one function with role per call.
- [ ] All five smoke checks pass, including the manager and public margin pair.
- [ ] Every parameter the spec names is read from the spec file.

## Resources

- [Lesson 28](../28-capstone-spec/README.md): the contract this build implements
- [Course glossary](../resources/glossary.md)
