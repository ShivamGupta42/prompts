# Ship cycle orchestrator (pre-flight + merge/cleanup + docs + lessons)

<task>Ship Cycle: Adversarial multi-stage shipping orchestrator. Pre-flight checks, classifies the work, runs merge + worktree cleanup, refreshes drifted docs (when applicable), captures lessons (for non-trivial work), final state check. Trivial chores degrade to the original ::W behavior — merge and clean, nothing more.</task>

<analysis>
STAGE 1 — PRE-FLIGHT (mandatory; STOP and report on any fail)
PR approved? CI green? No merge conflicts? Branch up to date with master? Working tree clean?

STAGE 2 — CLASSIFY THE WORK
Decide kind: feature / bugfix / refactor / infra / docs-only / chore. Then for each subsequent stage, mark APPLY/SKIP with one-line reason. Output a small table (merge+cleanup always; doc cleanup and lessons depend on kind).

STAGE 3 — DOC CLEANUP (when applicable; BEFORE merge, inside the PR)
Apply the doc-cleanup pass (per ::D) against the PR diff. **Commit doc updates as the FINAL commit(s) on the feature branch** ("docs: refresh canonical docs for <feature>"). Push.

Why BEFORE merge (load-bearing): post-merge doc commits on master bypass PR review and create a drift window. Inside the PR, doc commits ship atomically with code (squash-merge folds them in) and pass the same review/CI gates.

If unsure whether a doc needs updating, surface as "review needed" — don't skip silently, don't commit a speculative doc change.

STAGE 4 — PRE-MERGE RE-CHECK (if Stage 3 ran)
After doc commits land: CI re-run still green? No new conflicts? PR still mergeable? STOP if anything broke (e.g., a doc commit broke a tested code fence). Don't merge red CI.

STAGE 5 — MERGE + WORKTREE CLEANUP (always)
Squash-merge (code + doc commits become one atomic commit). Then cd to the master worktree BEFORE removing anything. From there: remove feature worktree, delete branch local+remote, git fetch --prune, git pull master. Chain it so nothing runs from the dying worktree.

STAGE 6 — LESSONS LEARNED (for non-trivial work; post-merge, reflective)
Apply the lessons-learned pass (per ::L). ≥7/10 confidence threshold. Check for duplicates against existing knowledge-base files; propose enhancement rather than new entry if similar exists.

STAGE 7 — FINAL STATE CHECK
Confirm: master current and clean, worktree count correct, branches deleted (local + remote), docs reflect reality (or "needs review" surfaced), lessons captured (or skipped with reason). Report any half-done state explicitly.
</analysis>

<report>
Output in order:
1. Classification table (per Stage 2)
2. Operations log: Pre-flight / Doc cleanup / Pre-merge re-check / Merge+cleanup / Lessons learned — each PASS/FAIL/COMPLETED/SKIPPED with reason
3. Docs updated (file → what changed) or "none needed"
4. Lessons captured (pattern → why → confidence) or "none surfaced"
5. Final state: master / worktrees / branches
6. Follow-ups: items needing human review, monitoring watches, unresolved questions
</report>

<rules>
- Pre-flight is mandatory; never merge without it
- ALWAYS cd to master worktree BEFORE removing the feature worktree (load-bearing safety rule)
- Doc cleanup only updates canonical docs (CLAUDE.md, AGENTS.md, README, docs/, runbooks)
- Lessons ≥7/10 confidence; no "maybe useful" padding
- If anything is irreversible and uncertain, STOP and ask one clarifying question
- Half-completion must be reported explicitly; silent half-done is a failure of this prompt
- Confidence anchors: 1-3=guessing, 4-6=informed but unverified, 7-8=verified, 9-10=verified with test/external source
- For deeper single-stage passes: ::D (docs) or ::L (lessons)
</rules>
