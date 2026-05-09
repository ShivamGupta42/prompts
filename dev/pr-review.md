# `::R` — Review feature branch changes

> **Use this prompt:** copy the body below and paste it into any AI chat.
> Synced from a personal espanso text-expansion config on 2026-05-09.

---

Review all changes in this feature branch.

1. List modified files by category (code, tests, config, docs) and risk level.
2. Rate confidence you understand each change—investigate low-confidence areas first.
3. Check against project patterns—any lessons learned being violated?
4. Identify gaps: tests, docs, error handling.
5. Validation: verify each change against its acceptance criteria—what proves it works?
6. Flag concerns by priority: P0 (blocks merge), P1 (fix before merge), P2 (defer).
7. Rate overall PR readiness with specific blockers.

RULES:
- Confidence anchors: 1-3=guessing, 4-6=informed but unverified, 7-8=verified by reading code, 9-10=verified with test run or external source
- If a category has no real concerns, say "nothing found" with a one-line note on what you checked—don't fabricate issues
- Fix One Find All: for each concern, grep the codebase for the same pattern and report every occurrence
- Top 5-10 findings max, grouped by priority
