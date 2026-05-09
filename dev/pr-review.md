# Review everything (adaptive multi-lens orchestrator)

<task>Review Everything: Adversarial multi-lens review of a PR diff. Classifies the diff, applies the relevant adversarial lenses (pr-review + up to 5 specialized lenses), dedupes findings across lenses, and produces one unified P0/P1/P2 list. For trivial diffs, classification skips most lenses and the output is essentially a focused pr-review; for substantial diffs, you get the full battery.</task>

<analysis>
STAGE 1 — CLASSIFY THE DIFF (always)
Run `git diff main...HEAD` (or master—check which base). For each lens, decide APPLY or SKIP based on what's in the diff. Output a classification table.

Lens preconditions:
- pr-review: ALWAYS (every diff gets a structured pass against project patterns)
- security-gate: APPLY if diff touches inputs/outputs, auth, network, secrets, dependencies, or any user-controllable surface. SKIP if purely formatting/comments/internal-types/test-fixtures.
- performance-profiler: APPLY if diff touches per-request paths, per-user-action paths, DB queries, network calls, or hot loops. SKIP if build-config/docs/non-runtime.
- ux-critique: APPLY if any change is user-facing—UI, copy, navigation, error states. SKIP if backend-only or developer-tool-only.
- migration-safety: APPLY if any change touches DB schema, API contracts, config formats, or wire protocols. SKIP if no contracts change.
- quality-hunt: APPLY if the diff contains a bug fix. SKIP if purely additive feature work or mechanical refactor.

Output:
| Lens | APPLY/SKIP | Reason |
| pr-review | APPLY | always |
| security-gate | … | … |
| performance-profiler | … | … |
| ux-critique | … | … |
| migration-safety | … | … |
| quality-hunt | … | … |

STAGE 2 — APPLY LENSES (parallel where supported; otherwise sequential per lens)

For each APPLY lens, run its standard analysis on the diff. Each lens must produce: P0/P1/P2 findings with confidence (1-10) and specific fixes. The standalone triggers ::QS / ::QP / ::UX / ::QM / ::QH each have the full lens spec — use those when you want maximum rigor or when the lens is unfamiliar. The pr-review lens (always-applied structured project-pattern pass against project lessons-learned, file categories, coverage gaps) lives only in this orchestrator; it has no standalone trigger.

Distinguishing rules at the orchestrator's vantage point (the standalones may not emphasize these):
- SECURITY GATE: try concrete exploit payloads, not abstract category checklists
- PERFORMANCE PROFILER: triage which dimensions matter for THESE changes — don't list-check every dimension
- MIGRATION SAFETY: surface the point-of-no-return in the rollback path
- QUALITY HUNT: only fires when the diff contains a bug fix; the goal is finding the same root pattern elsewhere

If you have parallel-execution tools (Task() in Claude Code), spawn one subagent per APPLY lens with fresh context, each fetching the full lens spec from https://raw.githubusercontent.com/ShivamGupta42/prompts/master/<folder>/<name>.md. Otherwise sequential per lens.

STAGE 3 — DEDUPE FINDINGS (mandatory, not optional)
Walk all findings. Key by (file, line, semantic-fingerprint). Merge duplicates:
- Keep ALL lenses that flagged it as provenance (e.g., "security + performance")
- Take the highest severity reported (P0 from one beats P1 from another)
- Compatible fixes → merge into a unified fix
- Conflicting fixes → surface BOTH and explicitly note the conflict; don't silently pick one

STAGE 4 — CROSS-LENS PATTERNS
Look for what's only visible across lenses:
- Findings clustered in one module/file → flag as high-risk area
- Same root cause appearing as multiple symptoms → recommend fixing the cause, not each instance
- Lenses disagree on severity for the same finding → surface the disagreement
- Several lenses concerned about the same data flow → call it out as the riskiest part of the diff

0-3 patterns. Skip with "no cross-lens patterns surfaced" if none.

STAGE 5 — VERIFIER LOOP (max 3 iterations, confidence-gated early stop)
Adversarial check: "what did the lenses miss given this consolidated view?"
Verifier outputs: (a) new findings, (b) confidence (1-10) the review is now exhaustive.
Termination:
- Stop if confidence ≥ 8
- Stop if confidence < 8 BUT no new findings emerged this pass (diminishing returns)
- Otherwise iterate, with the expanded finding set as context, up to 3 total passes

Confidence is the verifier's honest judgment, not a cargo-cult 9. If unsure, rate ≤ 7 and let another pass run.

STAGE 6 — PROOF-OF-UNDERSTANDING FOR EVERY P0
For each P0, produce in your own words (not copy-pasted from a lens):
1. What the issue is (one plain sentence)
2. How it manifests as a concrete failure (specific scenario: input X causes output Y; deploy Z breaks)
3. What the structural fix is (concrete change, not "improve X" or "be more careful")

If you CANNOT produce all three coherently, downgrade the finding to P1 with note "needs human review" rather than ship a vague P0.
</analysis>

<report>
OUTPUT in this order:

CLASSIFICATION TABLE (per Stage 1)

VERIFIER LOOP TRACE
- Iteration 1: confidence X, N findings added (or none)
- (Iteration 2 if applicable)
- Stopped because: confidence reached / no new findings / 3-iteration cap

FINDINGS (deduped, grouped P0/P1/P2):
P0 (blocks merge):
[1] file:line — issue (lenses: a/b)
    Proof: What / Manifests as / Fix
    Confidence: N/10
P1 (fix before merge):
[2] …
P2 (defer or nice-to-have):
[3] …

CROSS-LENS PATTERNS (or "nothing surfaced")

OVERALL
- PR readiness rating: N/10
- Confidence anchor: [verified by reading code / verified with test / etc]
- Specific blockers if rating < 8

WHAT WAS SKIPPED
(each skipped lens + the classification reason — so you can spot misclassification and run that lens manually)
</report>

<rules>
- Confidence anchors: 1-3=guessing, 4-6=informed but unverified, 7-8=verified by reading code, 9-10=verified with test run or external source
- If a lens doesn't apply, say so with a one-line reason — never fabricate findings to fill it
- Run lenses fresh — don't let one lens's findings prejudice the next
- DEDUPE is mandatory. Concatenating per-lens outputs without dedup is a failure of this prompt.
- Two lenses with contradictory fixes → surface the contradiction explicitly; don't silently pick
- Top 10-15 deduped findings max; ruthlessly prioritize over completeness
- If important context is missing (no diff, unclear scope, mid-refactor state), STOP and ask one clarifying question rather than reviewing speculatively
- For deeper single-lens passes: ::QS / ::QP / ::UX / ::QM / ::QH (each is the full standalone lens)
</rules>
