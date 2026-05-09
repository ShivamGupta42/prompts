# Adaptive plan critique (1 cycle)

Critique your plan with 1 adaptive review cycle.

0. CLASSIFY: One sentence—is this plan user-facing, backend-only, infra, or mixed? State which lenses will run and which are skipped (one-line reason each).

1. ASSUMPTIONS (always): List every assumption. Spawn an agent per assumption group to verify—no agent limit. Rate confidence per assumption (1-10).

2. LOW-CONFIDENCE RESOLUTION (always): For every assumption rated <7/10 in Stage 1, read the actual code to verify or refute. Don't guess. The goal is to enter Stage 3 with grounded understanding so the analyses below report on reality, not on the agent's prior assumptions. Subsequent stages may also read code if they surface new low-confidence areas.

3. ARCHITECTURE (always): Flag risks, breaking changes, consistency issues, performance concerns. Pre-alpha = no migration debt, fix now not later. Findings should reference confidence anchors (verified by reading code in Stage 2 = 7-8; verified with test run = 9-10).

4. USER IMPACT (only if user-facing or mixed; else skip with reason). Apply both:
   - JTBD pass (per ::J): job statement, four forces (1-10), journey friction, highest-impact improvement
   - UX critique pass (per ::UX): 8-category review with P0/P1/P2 fixes; friction-to-fix on the top item

5. VALIDATION CRITERIA (always): apply per ::QV. Per change: observable "done" with edge cases / regression checks / integration contracts / rollback signal. Group P0 (blocks release) / P1 (should verify) / P2 (nice). Mark each automated/manual/production-only. Rate criteria completeness (1-10).

6. REWRITE: Update plan with verified understanding, observations, questions surfaced, validation criteria appended.

RULES:
- Confidence anchors: 1-3=guessing, 4-6=informed but unverified, 7-8=verified by reading code, 9-10=verified with test run or external source
- If you cannot determine something from available context (unclear scope, missing code, ambiguous requirement), STOP and ask one clarifying question rather than guessing
- If a lens doesn't apply, say "skipped: [one-line reason]"—never fabricate findings to fill a section
- NO implementation—planning only
- NO quick wins—optimize for long-term architecture growth
- NO deferring important changes (consistency, performance, correctness)
- Summarize remaining unknowns and recommended next steps
