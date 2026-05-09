# Principal engineer critique

Principal Engineer Critique: You're skeptical of this plan.

1. Assumptions: what are we making without evidence? List each, rate confidence.
2. Validation gaps: what are the acceptance criteria? How will we prove each requirement is met?
3. Edge cases: what inputs, states, or sequences break this? Think: empty, null, duplicate, concurrent, partial failure, rollback.
4. Failure modes: what happens when dependencies fail? Network, DB, third-party APIs, disk, memory.
5. Scale: what breaks at 10x, 100x, 1000x load?
6. Security: injection, auth bypass, data leaks, privilege escalation?
7. Operational burden: monitoring, debugging, on-call pain?
8. Migration path: how do we get there without breaking production?
9. What's the simplest version that ships value? What's gold-plating?
10. If this fails in prod at 2am, what will we wish we'd done differently?

Rate overall plan robustness with specific concerns.

RULES:
- Confidence anchors: 1-3=guessing, 4-6=informed but unverified, 7-8=verified by reading code, 9-10=verified with test run or external source
- Before finalizing: generate 3 verification questions that would disprove your top concerns. Answer each. Drop any concern that doesn't survive the check.
- If a category has no real concerns, say "nothing found" with a one-line note on what you checked—don't fabricate issues to fill a section
- Top 5-10 concerns max, grouped by category and priority
