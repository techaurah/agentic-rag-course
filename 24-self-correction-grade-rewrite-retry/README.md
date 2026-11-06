# Lesson 24: Self-correction: grade, rewrite, retry

**Time:** about 75 minutes · **Difficulty:** Advanced · **Prerequisites:** Lessons 16, 20, and 21 · **You need:** The tool contract from Lesson 21; the agent now loops on it.

The agentic pattern that earns its name: retrieve narrowly, grade the evidence, and when the grade fails, act again (widen the search, rewrite the query, decompose) before answering. This lesson builds the simplest honest version: answer from the top 3, grade fact coverage, and on failure retry with the top 10. It works. Then it grades the grader, because the runtime grader cannot see the golden facts, and the gap between the grader you can run and the truth you can only measure offline is where self-correction systems quietly fail.

## The loop, measured

At top 3, exactly 1 of the 26 answerable questions fails fact coverage: q11 (gift card validity across dates), at 0.0. Widening to the top 10 recovers it to 1.0: the evidence was in the candidate pool, ranked 4 to 10, and the retry costs one extra retrieval on 1 of 26 questions, a retry rate of about 0.038. As far as retrieval goes, grade and widen is a clean win, and the production versions add the Lesson 16 move (rewrite or decompose on retry) behind the same grade gate.

## The grader problem

Offline, the grade is fact recall against gold facts. Online, there are no gold facts; the grader must proxy. The artifact's surface grader (a quantity question passes if any top chunk contains a digit; anything retrieved passes otherwise) is the kind of check real systems ship, and it passes the failing question: q11's top 3 chunks contain digits galore, none of them the right facts. A grader that cannot fail the cases the loop exists to fix converts self-correction into theatre: the loop runs, the grade passes, the wrong answer ships with a process story attached. The design consequences are concrete. Graders should test the composed answer against the evidence (does the answer sentence's fact appear in a cited chunk: Lesson 20's grounding check, which is runnable online), test coverage of the question's own concepts (the unseen concepts test, also runnable), and treat score shaped checks as hints, never gates. And the offline golden grading still runs in evaluation, because the online grader's false pass rate is itself a metric someone must own: here, 1 false pass on the only case that mattered.

## Loops need exits

Every retry policy in this lesson is bounded: widen once, then answer or refuse from the wider set. Unbounded grade-rewrite loops burn latency and money while oscillating (Lesson 17's PRF failure is a one step loop with the same disease). State the budget in the design (attempts, added latency, added cost per question) and grade the loop as a whole on the golden set, attempts included, not just its final answers.

## Run it

Run `python3 self_correction.py`. `evaluate()` returns the failing question, its recovery at 10 (1.0), the retry rate (0.0385), and the surface grader's false passes (1). The capstone's harness (Lesson 30) adopts the widen on fail policy with the grounding check as its online grade.

## Common failures

- **Graders that proxy the wrong thing.** Digits present is not facts present. Grade the answer against evidence, not the retrieval against vibes.
- **Retries without new information.** Re-running the identical retrieval and hoping is a loop, not a correction. Each attempt must change something: depth, query, strategy.
- **No attempt budget.** A loop without a stated maximum is a latency incident waiting for its question.

## Recap checklist

- [ ] I know the failing question at top 3 and its recovery at top 10.
- [ ] I can explain the surface grader's false pass and the design rule it implies.
- [ ] I can state a bounded retry policy with its budget in numbers.

## Resources

- [Course glossary](../resources/glossary.md): self-correction, grader, retry budget
- [Course 1, Lesson 25: Reflection and self-critique](https://github.com/techaurah/agentic-ai-for-beginners): the same loop at the reasoning layer
