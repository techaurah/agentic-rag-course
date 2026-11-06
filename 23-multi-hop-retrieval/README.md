# Lesson 23: Multi-hop retrieval: questions that need two documents

**Time:** about 75 minutes · **Difficulty:** Intermediate · **Prerequisites:** Lessons 16 and 20 · **You need:** Lesson 16's subqueries, reused here as the worked decomposition.

Lesson 16 isolated the retrieval half of multi-hop. This lesson runs the full pipeline on the five multi-hop questions and grades two layers separately, because they tell opposite stories and the difference is the most instructive result in the agentic module: decomposition fixes retrieval completely and the composed answers get worse.

## Layer one: retrieval, solved

Document recall, single shot against decomposed union: 0.9 to 1.0. Every multi-hop question's gold documents are all found (q29 recovers its second document, the cafe locations, which single shot ranked below the cut). As a retrieval result this is clean and worth having: the evidence for every multi-hop answer is now in the room.

## Layer two: answers, not solved

Answer fact coverage (the fraction of gold facts present in the composer's single answer sentence): 0.5 single shot, 0.3 with union retrieval. Read the per question table in the artifact. q28 regresses from 1.0 to 0.0: single shot's top sentence happened to state the voucher rule whole, while the union's ranking promotes a gift card sentence that shares more question words but states only half the rule, and the composer, which picks one sentence, picks the half. q10 holds at 0.5 and q11 at 0.0 under both: their facts live in two sentences of two documents, and no single sentence contains both, so a one sentence composer has a hard ceiling on multi-hop questions regardless of retrieval. q09 is the exception that proves the shape: its answer sentence states the delivery rule with the Gold condition inside it, so coverage is 1.0 both ways.

## The architectural conclusion

Multi-hop questions need multi-sentence answers: a composer (in production, a generating model) that synthesises across the union's evidence, with citations per claim, graded by Lesson 20's grounding checker per sentence. Retrieval decomposition is necessary and insufficient; the failure moves up a layer, and the measurement discipline that found it (grade documents and answers separately) is what keeps a team from declaring victory at the retrieval layer while users read half answers. The capstone (Lessons 28 to 30) keeps the extractive composer and its ceiling visible in the gates rather than pretending the ceiling is not there; replacing the composer with a model is the first post-course upgrade this lesson argues for, with the checker kept on as its supervisor.

## Run it

Run `python3 multi_hop.py`. `evaluate()` returns the per question table and the four means (documents 0.9 to 1.0; coverage 0.5 to 0.3). Cover the coverage column, predict it from the document column, and note the prediction error: that gap is the lesson.

## Common failures

- **Declaring multi-hop solved at the retrieval layer.** Documents found is not answers given. Grade both layers, always, separately.
- **Union without a budget.** Union retrieval widens context; without Lesson 14's budget the generator drowns in the widened set and coverage falls further.
- **One sentence composers on two fact questions.** A structural ceiling, not a tuning problem. Match the composer's shape to the question's shape.

## Recap checklist

- [ ] I know both layers' numbers and can explain the divergence.
- [ ] I can name q28's regression mechanism (ranking promotes a half rule sentence).
- [ ] I can state the architectural fix and the supervisor it needs.

## Resources

- [Course 1, Lesson 19: RAG with a framework, and agentic RAG](https://github.com/techaurah/agentic-ai-for-beginners)
- [Course glossary](../resources/glossary.md)
