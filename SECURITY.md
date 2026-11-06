# Security policy

## Reporting a vulnerability

If you find a security problem in this repository, for example a lesson that teaches an unsafe retrieval pattern, example code that leaks credentials, or a template that invites learners to paste real customer data or API keys into a public fork, please do not open a public issue with the details.

Report it privately through the contact form at [techaurah.com](https://techaurah.com), with "Agentic RAG course security" in the message. We aim to acknowledge reports within three working days and to fix or annotate confirmed problems in the affected lesson.

## Scope notes

- This is a teaching repository. Every example business is fictional, every dataset is invented for the lesson, and learners are told repeatedly never to put real customer data in a fork.
- Never commit real API keys, tokens, customer lists, or personal data to your fork. If you accidentally commit a secret, rotate it immediately; deleting the commit is not enough.
- Lesson 12 teaches permissions aware retrieval as a design discipline: role filters are enforced in code before ranking, never by prompt wording. A lesson or PR that moves a permission check into a prompt will be treated as a security problem, not a style choice.
