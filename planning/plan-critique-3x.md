# Adaptive plan critique (3 cycles)

Critique your plan with 3 full adaptive review cycles.

PER CYCLE (commit and push after each):
0. CLASSIFY: One sentence—user-facing, backend-only, infra, or mixed? State which lenses will run and which are skipped (one-line reason each). Re-classify per cycle—scope can shift as critique deepens.

1. ASSUMPTIONS (always): List every assumption. Spawn an agent per assumption group to verify—no agent limit. Rate confidence per assumption (1-10).

2. LOW-CONFIDENCE RESOLUTION (always): For every assumption rated <7/10 in Stage 1, read the actual code to verify or refute. Don't guess. Subsequent stages may also read code if they surface new low-confidence areas.

3. ARCHITECTURE (always): Flag risks, breaking changes, consistency issues, performance concerns. Pre-alpha = no migration debt, fix now not later.

4. USER IMPACT (only if user-facing or mixed; else skip with reason). Apply both:
   - JTBD pass (per ::J): job statement, four forces (1-10), journey friction, highest-impact improvement
   - UX critique pass (per ::UX): 8-category review with P0/P1/P2 fixes; friction-to-fix on the top item

5. VALIDATION CRITERIA (always): apply per ::QV. P0/P1/P2 grouping with rollback signal. Each criterion marked automated/manual/production-only. Rate completeness (1-10).

6. REWRITE: Update plan with verified understanding, observations, questions surfaced, validation criteria refined.

7. COMMIT: `git add -A && git commit -m "critique cycle N/3: [key findings]" && git push`

RULES:
- Confidence anchors: 1-3=guessing, 4-6=informed but unverified, 7-8=verified by reading code, 9-10=verified with test run or external source
- If a lens doesn't apply, say "skipped: [one-line reason]"—never fabricate findings to fill a section
- NO implementation—planning only
- NO quick wins—optimize for long-term architecture growth
- NO deferring important changes (consistency, performance, correctness)
- MUST complete all 3 cycles before stopping
- Each cycle must go DEEPER than the last—surface new questions, challenge prior conclusions, refine validation criteria
- After final cycle: summarize remaining unknowns and recommended next steps
