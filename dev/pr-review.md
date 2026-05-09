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

Brief inline specs for each APPLY lens:

- PR REVIEW: Walk diff against project patterns. Modified files by category (code/tests/config/docs) with risk level. Confidence per change. Lessons-learned violations. Coverage gaps (tests, docs, error handling). Top 5-10 findings.
- SECURITY GATE: Map new inputs/outputs. Per input: validation (try payloads `';DROP`, `<script>`, `../../`, oversized strings), auth/authz, data flow, secrets, dependency risks, race conditions. Concrete exploit scenarios with likelihood × severity.
- PERFORMANCE PROFILER: Hot-path classification. Triage relevant dimensions (algorithmic, DB, memory, I/O, concurrency, latency, resource exhaustion, frontend). Cascading effects, load projection, quick wins.
- UX CRITIQUE: 8 categories—first impression, hierarchy, consistency, information completeness, copy clarity, mobile fit, accessibility, error/edge states. 5-10 issues max P0/P1/P2 with specific fixes. Friction-to-fix on the top item.
- MIGRATION SAFETY: Change inventory (classify each), data risk (drops/narrowing/NOT NULL/UNIQUE/FK), lock behavior + duration, rollout order (expand-contract), rollback path (point of no return), contract/client impact, performance, exploit scenarios.
- QUALITY HUNT: Name root pattern of the bug. Search codebase for same pattern. List every occurrence with file:line and risk. Propose architectural prevention.

For deeper single-lens passes, fall back to standalone triggers (::QS, ::QP, ::UX, ::QM, ::QH) — each has the full standalone prompt.

If you have parallel-execution tools (like Task() in Claude Code), spawn one subagent per APPLY lens with fresh context, each fetching the full lens spec from https://raw.githubusercontent.com/ShivamGupta42/prompts/master/<folder>/<name>.md. Otherwise apply the inline specs above lens by lens.

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
