# `::P5` — Adaptive plan critique (5 cycles)

> **Use this prompt:** copy the body below and paste it into any AI chat.
> Synced from a personal espanso text-expansion config on 2026-05-09.

---

Critique your plan with 5 full adaptive review cycles.

PER CYCLE (commit and push after each):
0. CLASSIFY: One sentence—user-facing, backend-only, infra, or mixed? State which lenses will run and which are skipped (one-line reason each). Re-classify per cycle—scope can shift as critique deepens.

1. ASSUMPTIONS (always): List every assumption. Spawn an agent per assumption group to verify—no agent limit. Rate confidence per assumption after investigation.

2. ARCHITECTURE (always): Flag risks, breaking changes, consistency issues, performance concerns. Pre-alpha = no migration debt, fix now not later.

3. USER IMPACT (only if user-facing or mixed; else skip with reason). Apply both evaluations—
   - JTBD: State the job (when [situation], a person wants to [motivation], so they can [outcome]). Rate four forces 1-10 (push/pull/anxiety/habit). Walk the journey, mark friction and anxiety per stage. Single highest-impact improvement with confidence rating.
   - UX critique: 8 categories—first impression, hierarchy, consistency, information completeness, copy clarity, mobile fit, accessibility, error/edge states. 5-10 issues max grouped P0/P1/P2 with specific fixes. Friction-to-fix walkthrough on the top item.

4. LOW-CONFIDENCE (always): Explore all <7/10 areas deeply. Read the actual code, don't guess.

5. VALIDATION CRITERIA (always): For every change, define observable "done"—exact inputs, expected outputs, where to look. Include edge cases (empty/null/boundary/concurrent/partial-failure/unicode), regression checks, integration contracts, rollback signal (observable threshold). Group P0/P1/P2. Mark each automated/manual/production-only. Rate criteria completeness (1-10).

6. REWRITE: Update plan with verified understanding, observations, questions surfaced, validation criteria refined.

7. COMMIT: `git add -A && git commit -m "critique cycle N/5: [key findings]" && git push`

RULES:
- Confidence anchors: 1-3=guessing, 4-6=informed but unverified, 7-8=verified by reading code, 9-10=verified with test run or external source
- If a lens doesn't apply, say "skipped: [one-line reason]"—never fabricate findings to fill a section
- NO implementation—planning only
- NO quick wins—optimize for long-term architecture growth
- NO deferring important changes (consistency, performance, correctness)
- MUST complete all 5 cycles before stopping
- Each cycle must go DEEPER than the last—surface new questions, challenge prior conclusions, refine validation criteria
- After final cycle: summarize remaining unknowns and recommended next steps
