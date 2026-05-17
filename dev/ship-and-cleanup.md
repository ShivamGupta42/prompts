# Ship cleanup (prepare branch, squash-merge, clean worktree)

<task>Ship and cleanup. Get the current branch shippable, then squash-merge and remove the feature worktree safely. Prefer doing mechanical prep over stopping: commit dirty work, push missing remotes, open/update the PR. Hard-stop only on true merge blockers.</task>

<workflow>
1. Orient: identify repo root, current branch/worktree, base branch (master/main), matching PR if any, and dirty/untracked changes.
2. Make shippable: if dirty, review diff, commit coherent work, push. If no remote branch or PR exists, push and open/update the PR. If a non-trivial behavior change obviously drifts canonical docs (CLAUDE.md, AGENTS.md, README, docs/, runbooks), update docs before final merge and commit/push them.
3. Merge gate: confirm PR exists, target branch is correct, approval/authorization is satisfied, required checks are green, no conflicts, and platform merge is allowed. If any fail, stop with the next concrete action.
4. Merge + cleanup: squash-merge the PR. Then cd to the master/main worktree BEFORE cleanup. From there remove the feature worktree, delete local+remote branch, git fetch --prune, and git pull. Chain it so nothing runs from the dying worktree.
5. Final check: base worktree clean/current, feature worktree gone, branch gone local+remote, docs/lessons done or intentionally skipped.
</workflow>

<rules>
- Old ::W behavior is the happy path: squash merge, cd to base worktree, remove worktree, delete branch, prune, pull.
- Dirty worktree / missing remote / missing PR are prep tasks, not pre-flight failures.
- Do not merge red CI, conflicts, wrong base, missing required approval, or uncertain irreversible cleanup.
- Lessons are optional and brief; capture only reusable lessons with >=7/10 confidence, never padding.
- Ask one concise question only when blocked by a decision you cannot infer.
</rules>

<report>
Keep output short:
1. Prep done (commits/push/PR/docs) or skipped
2. Merge gate PASS/FAIL with reason
3. Cleanup done or blocked
4. Final state and next action
</report>
