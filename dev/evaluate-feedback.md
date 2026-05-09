# Evaluate feedback deeply

Evaluate this feedback deeply.

1. List specific issues raised.
2. Rate confidence per issue—investigate low-confidence first.
3. VALIDITY CHECK: which issues are valid critiques worth fixing, which are wrong on inspection? Document the basis for each judgment. Subsequent steps split based on this.
4. Categorize VALID issues: P0 (blocks merge), P1 (fix before merge), P2 (defer).
5. Find root causes connecting multiple valid issues.
6. For each valid critique: define validation criteria (what proves it's fixed), propose fix, verify against criteria, note side effects.
7. For invalid critiques: counter with evidence.
8. Rate overall resolution confidence.

RULES:
- Confidence anchors: 1-3=guessing, 4-6=informed but unverified, 7-8=verified by reading code, 9-10=verified with test run or external source
- If an issue is invalid on inspection, say so with evidence—don't manufacture agreement
- Fix One Find All: for each valid critique, grep the codebase for the same pattern and report every occurrence
- Top 5-10 findings max, grouped by priority
