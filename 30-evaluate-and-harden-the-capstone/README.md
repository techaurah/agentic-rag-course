# Lesson 30: Evaluate and harden the capstone

**Time:** about 75 minutes · **Difficulty:** Advanced · **Prerequisites:** Lessons 28 and 29 · **You need:** The built system; this lesson is its examination.

The harness imports Lesson 29's system as a black box, runs the entire golden set through its public interface, and compares every measurement against Lesson 28's gates. Nothing here reaches inside the system: retrieval is graded through `retrieve`, answers through `answer`, latency around the calls. That black box discipline is the point: the gates certify the behaviour a caller receives, not the implementation a builder admires.

## The gate table

On the reference build, every gate passes. Document recall at 5: 0.9808 against a 0.95 floor. Fact recall at 5: 0.9808 against 0.95. Citation coverage: 1.0. Grounded sentences: 1.0. Refusal correct: 5 of 6 against a floor of 5, with the miss being q24, named in the harness output as the known miss rather than absorbed silently. False refusals: 0. Restricted leaks: 0. Mean latency: single digit milliseconds per question on the build machine against the 50 ms ceiling (Lesson 26's margin principle: the gate sits far above the measurement, so machine noise cannot flip it). The hardening work this lesson represents is not the passing; it is the wiring that makes any future change (a new document, a threshold tweak, an embedder swap) rerun this table and fail loudly, which is why the course's CI runs this harness's smoke test on every change.

## Hardening beyond the gates

Three checks the gates do not carry, worth adding in your own deployments: run the gap set through the same harness and report it beside the golden table (the reference system inherits Lesson 15's rewriting only if you add it; the capstone as specified does not include the synonym table, and its gap performance is correspondingly the unrewritten one, a deliberate spec decision to keep the capstone minimal and its limits visible); probe refusal with fresh unanswerable questions written after the system froze, because a refusal rate measured only on known questions flatters; and rerun the table with the roles permuted (every question asked as every role) to prove the permission gates are structural, not coincidental.

## Run it

Run `python3 evaluate_capstone.py`. `evaluate()` returns the values, the per gate pass map, and `all_gates_pass`. If any gate fails in your fork, the failure names its lesson: recall points at Modules 1 to 5, refusal at Lesson 20, leaks at Lesson 12, latency at Lesson 26. That traceability, from a red gate to the lesson that teaches its fix, is the course's design closing on itself.

## Common failures

- **Grading through internals.** A harness that imports the system's private pieces certifies a snapshot of the code, not the behaviour. Grade through the public interface.
- **Absorbing known misses.** A gate floor set at the measured value with the miss unnamed invites the next maintainer to "fix" the floor. Name the miss in the output, as here.
- **One machine's latency as a promise.** The gate is a ceiling with headroom, and the value printed is this run's. Report both, promise only the ceiling.

## Recap checklist

- [ ] I have the full gate table with values and floors.
- [ ] I can trace each gate to its lesson.
- [ ] I know the three hardening checks beyond the gates, and why the capstone omits the synonym table by spec.

## Resources

- [Lesson 28](../28-capstone-spec/README.md): the gates' source
- [Showcase](../showcase/README.md): where passing capstones are exhibited
