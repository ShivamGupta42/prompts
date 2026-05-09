# Ship cycle orchestrator (pre-flight + merge/cleanup + docs + lessons)

<task>Ship Cycle: Adversarial multi-stage shipping orchestrator. Pre-flight checks, classifies the work, runs merge + worktree cleanup, refreshes drifted docs (when applicable), captures lessons (for non-trivial work), final state check. Trivial chores degrade to the original ::W behavior — merge and clean, nothing more.</task>

<analysis>
STAGE 1 — PRE-FLIGHT CHECK (mandatory; never merge without it)
Confirm before doing anything irreversible:
- PR is approved (or merge is otherwise authorized)
- CI / required checks are green on the PR
- No merge conflicts with master
- Branch is up to date with master (rebase if not)
- Working tree is clean

If any check fails: STOP and report. Do not proceed to merge.

STAGE 2 — CLASSIFY THE WORK
What did this PR ship? Decide based on the diff and PR description:
- feature: new user-facing capability
- bugfix: fixes existing behavior
- refactor: internal restructuring, no behavior change
- infra/ops: build, deploy, monitoring, CI changes
- docs-only: just documentation
- chore: deps, formatting, comments, small mechanics

For each subsequent stage, decide APPLY or SKIP with one-line reason:

| Stage | APPLY/SKIP | Reason |
| Merge + cleanup | APPLY | always |
| Doc cleanup | APPLY/SKIP | reason (e.g., "feature ships new behavior — likely doc drift" / "chore: no doc impact") |
| Lessons learned | APPLY/SKIP | reason (e.g., "non-trivial bugfix surfaced patterns" / "single-line typo: nothing to extract") |

STAGE 3 — DOC CLEANUP (when applicable; runs BEFORE merge so doc updates are part of the PR)
Walk the PR diff (`git diff main...HEAD` or master—check which base). For each non-trivial code or behavior change, ask:
- Does any canonical doc reference the OLD behavior? (CLAUDE.md, AGENTS.md, README, docs/, runbooks, API reference)
- Does any canonical doc need to ADD coverage of the NEW behavior?
- Are there examples in docs that now produce different output?
- Did any deprecation warning land that needs a sunset note in docs?

Update affected docs in place. **Commit the doc updates as the FINAL commit(s) on the feature branch** with a message like "docs: refresh canonical docs for <feature>". Push.

Why before merge: doc updates that land directly on master post-merge bypass PR review and create a window where master has new code with stale docs. Keeping doc commits inside the PR means they ship atomically with the code (squash-merge folds them into the same commit) and pass through the same review/CI safety net.

If unsure whether a doc needs updating, surface as "review needed" — don't skip silently and don't commit a speculative doc change.

For deeper standalone doc-cleanup pass, fall back to ::D.

STAGE 4 — PRE-MERGE RE-CHECK (after doc commits land, if Stage 3 ran)
Re-confirm Stage 1 conditions still hold:
- CI / required checks are green on the PR (the doc commits triggered a re-run; wait for it)
- No new merge conflicts with master after the doc commits
- PR is still mergeable

If any condition broke (e.g., a doc commit accidentally broke a code-fence in a tested README example), STOP and surface what broke. Do not proceed to merge with a red CI.

STAGE 5 — MERGE + WORKTREE CLEANUP (always)
Squash-merge the PR (so code + doc commits become one atomic commit on master). Then cd to the master worktree BEFORE any cleanup. From there:
- Remove the feature worktree
- Delete the branch (local + remote)
- git fetch --prune
- git pull master

Chain it all so nothing runs from the dying worktree.

Confirm after: master is current, feature worktree is gone, branch deleted both locally and on remote.

STAGE 6 — LESSONS LEARNED (for non-trivial work; post-merge, reflective)
Reflect on the session that produced this PR:
- What patterns emerged worth capturing?
- What anti-patterns surfaced worth flagging?
- What debugging insights would help next time?

For each: state the pattern, why it matters, code example if applicable. Map to your project's knowledge-base files (CLAUDE.md, AGENTS.md, docs/, context/, README, or wherever your team documents conventions).

Rate confidence each lesson is broadly applicable vs one-off:
- 1-3: guessing
- 4-6: informed but unverified
- 7-8: seen in multiple sessions/projects
- 9-10: verified pattern with strong evidence

Only include ≥7/10 lessons. Be VERY brief in suggestions. Check for duplicates — if a similar lesson exists, propose enhancement instead of new entry.

For deeper standalone lessons-learned pass, fall back to ::L.

STAGE 7 — FINAL STATE CHECK
Verify the cycle is complete:
- master is current and clean
- worktree count is correct (only those that should still exist)
- branch list is correct (deleted branches actually gone, both local and remote)
- canonical docs reflect reality (the doc commits landed in the PR and shipped with the squash-merge; or "needs review" items surfaced for human follow-up)
- lessons captured (or skipped with reason)

If anything is wrong or half-done, report it. Don't silently leave half-completed state.
</analysis>

<report>
OUTPUT in this order:

CLASSIFICATION TABLE (per Stage 2)

OPERATIONS LOG (in execution order)
- Pre-flight: PASS / FAIL (with details if fail)
- Doc cleanup: COMPLETED (N commits pushed) / SKIPPED (with reason)
- Pre-merge re-check: PASS / FAIL (with details)
- Merge + cleanup: COMPLETED / FAILED (with details)
- Lessons learned: COMPLETED / SKIPPED (with reason)

DOCS UPDATED (or "no doc updates needed")
- file:line — what changed and why

LESSONS CAPTURED (or "no lessons surfaced")
- pattern — why it matters — confidence rating

FINAL STATE
- master: current/stale
- worktrees: correct/wrong
- branches: correct/stale references

FOLLOW-UPS
- Items needing human review (e.g., "docs/auth.md references OAuth flow — review needed for new SSO path")
- Monitoring/observability watches for the next N hours/days (if applicable)
- Open questions the orchestrator couldn't resolve
</report>

<rules>
- The pre-flight check is mandatory. Never merge without it.
- ALWAYS cd to the master worktree BEFORE removing the feature worktree (the original ::W rule)
- If the user is on a worktree about to be deleted, the cleanup must happen in a different working directory
- For doc cleanup: only update canonical docs (CLAUDE.md, README, docs/, runbooks) — not arbitrary mentions in comments or commit messages
- Lessons learned: ≥7/10 confidence threshold; no padding with "maybe useful" lessons
- If anything during the cycle is irreversible and uncertain, STOP and ask one clarifying question
- The orchestrator MUST report what it did and what it skipped — silent half-completion is a failure of this prompt
- For deeper single-stage passes after this orchestrator runs, fall back to ::D (docs) or ::L (lessons)
</rules>
