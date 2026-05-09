# Safety stack — bait test proof

Phase 1 of the prompts-repo plan is complete. The Standard safety stack
(local pre-commit hook + GitHub Action mirror + branch protection on master)
was bait-tested on 2026-05-09 and confirmed to block all bait categories
at both the local and CI layers.

## Bait PR

- PR #1: `DO NOT MERGE: safety bait tests`
- Status: closed without merge, branch deleted
- Action run: https://github.com/ShivamGupta42/prompts/actions/runs/25592070130
- Action conclusion: **failure** (as required)

## Bait coverage

Five bait patterns were planted in the closed bait PR's `safety/bait.md`
(content not reproduced here — the safety hook would block this very file
if any literal bait strings appeared inline). Each pattern category below
was caught by the indicated layers.

| Bait category | Local hook (pre-commit) | GitHub Action (scan) |
|---|---|---|
| Real first name (case-insensitive, allowlists `ShivamGupta42` handle) | `forbidden-patterns` | `forbidden-patterns` |
| Personal Gmail address | `forbidden-patterns` | `forbidden-patterns` |
| Local macOS user path | `forbidden-patterns` (matched twice — name + path patterns) | `forbidden-patterns` |
| AWS access key format (`AKIA...`) | `gitleaks` rule `aws-access-token`, entropy 4.08 | `gitleaks-action` |
| GitHub PAT format (`ghp_...`) | scanned by `gitleaks` | scanned by `gitleaks-action` |

The local hook blocked the very first commit attempt. No bypass possible
without explicitly passing `--no-verify`. The Action layer caught the same
content when `--no-verify` was used and the bait branch was pushed; branch
protection (`scan` required) prevented the resulting PR from being merged.

### Bonus validation

When this very PROVEN.md file was first drafted with literal bait strings
in the table cells (the obvious thing to write), the local hook blocked
the commit. This is a third independent proof: the safety stack catches
even well-intentioned documentation that incidentally restates the patterns.
The cells above use category labels instead.

## Branch protection state on master

```
required_status_checks: ["scan"]
enforce_admins:         true
pr_required:            true
force_push_blocked:     true
deletion_blocked:       true
```

## Conclusion

Phase 1 is done. Safe to proceed to Phase 2 (lens markdown files in
`lenses/` and the `::P1/P3/P5` refactor in espanso).
