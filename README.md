# prompts

Prompts I use when building software with coding agents (Claude Code, Codex, Cursor, Gemini, Aider). Each one produces a structured review with confidence ratings and P0/P1/P2 findings.

### Starting an idea

Before code or specs exist, figure out if it's worth building.

- [`ux/jtbd.md`](ux/jtbd.md) — name the actual job a user is hiring this for. *Most plans skip "is anyone going to want this?"*
- [`planning/requirements-interview.md`](planning/requirements-interview.md) — clarify ambiguous asks one question at a time. *Vague specs produce vague code.*
- [`marketing/distribution-strategy.md`](marketing/distribution-strategy.md), [`marketing/go-to-market.md`](marketing/go-to-market.md) — channel and GTM thinking. *If no one finds it, it doesn't matter that it works.*

### Planning

Once you have a plan, pressure-test it.

- [`planning/plan-critique-1x.md`](planning/plan-critique-1x.md), [`planning/plan-critique-3x.md`](planning/plan-critique-3x.md), [`planning/plan-critique-5x.md`](planning/plan-critique-5x.md) — adaptive cycle that classifies the plan and pulls in JTBD/UX/validation. *Plans look reasonable until you stress them.*
- [`planning/principal-critique.md`](planning/principal-critique.md) — adversarial senior-engineer pass. *Someone needs to be the skeptic on every plan.*
- [`planning/team-assembly-1r.md`](planning/team-assembly-1r.md), [`planning/team-assembly-2r.md`](planning/team-assembly-2r.md), [`planning/team-assembly-3r.md`](planning/team-assembly-3r.md), [`planning/team-assembly-5r.md`](planning/team-assembly-5r.md) — assemble personas, run multi-round discussion. *Solo plans miss what a domain expert would catch.*
- [`validation-criteria.md`](validation-criteria.md) — define observable "done" before starting. *"Make it work" isn't a test.*

### Reviewing

Once code is written (by you or an agent), verify it.

- [`dev/pr-review.md`](dev/pr-review.md) — structured pass against project patterns. *"LGTM" misses real bugs.*
- [`qa/security-gate.md`](qa/security-gate.md) — paranoid attack-surface analysis on the diff. *Every input is potentially hostile.*
- [`qa/performance-profiler.md`](qa/performance-profiler.md) — find what breaks under load. *Big-O matters at 100x.*
- [`qa/quality-hunt.md`](qa/quality-hunt.md) — find similar bugs elsewhere. *The bug you fixed is rarely the only instance.*
- [`qa/manual-qa-checklist.md`](qa/manual-qa-checklist.md), [`qa/quick-smoke-test.md`](qa/quick-smoke-test.md), [`qa/browser-qa.md`](qa/browser-qa.md) — testing at three depths. *"Did you test it?" needs concrete steps.*
- [`ux/ux-critique.md`](ux/ux-critique.md) — UI/UX review. *Confident-looking UIs ship with broken affordances.*
- [`dev/evaluate-feedback.md`](dev/evaluate-feedback.md), [`dev/fix-issues.md`](dev/fix-issues.md) — work through feedback and fix. *Feedback without triage turns into a TODO graveyard.*

### After shipping

Close the loop.

- [`dev/ship-and-cleanup.md`](dev/ship-and-cleanup.md) — merge PR, remove worktree, delete branch. *Branch detritus accumulates fast.*
- [`dev/doc-cleanup.md`](dev/doc-cleanup.md) — refresh canonical docs against the changes. *Drifted docs are worse than missing ones.*
- [`learning/lessons-learned.md`](learning/lessons-learned.md) — extract generalizable patterns. *Same mistake twice is a process failure.*

Copy any body into your AI chat. Nothing to install. Full file-level list in [INDEX.md](INDEX.md).

## Folder layout

```
prompts/
├── planning/                  plan critiques, requirements, team reviews
├── dev/                       PR review, fix issues, doc cleanup, ship
├── ux/                        JTBD, UI/UX critique, friction-to-fix
├── qa/                        security, performance, manual tests, smoke
├── marketing/                 distribution, GTM, campaigns, audits
├── learning/                  lessons learned
└── validation-criteria.md     cross-cutting (used by most plans)
```

## How to use them

Copy the body of any prompt and paste it into your chat. That's the simplest path.

If you have tooling that pulls prompts from URLs, the raw URL is `https://raw.githubusercontent.com/ShivamGupta42/prompts/master/<folder>/<name>.md`.

If you want to change them to match how you think, fork the repo and point your tools at your fork.

## Chains and gaps

Most prompts are run manually today — pick one, paste, run. A few are already orchestrators that compose others on demand:

- `plan-critique-3x` classifies the plan, then pulls JTBD + UX + validation as needed
- `team-assembly-3r` proposes 3–5 personas, runs N rounds of discussion, outputs sequenced tasks

```
       plan-critique-3x          <- orchestrator
             │
             │  classifies the plan, then pulls:
             ▼
   ┌─────────┴─────────┬────────────────────┐
   ▼                   ▼                    ▼
   jtbd          ux-critique         validation-criteria
   (skip if      (skip if            (always)
    backend)     backend)
```

Chains worth building next:

- **idea-validate** — `jtbd` + `requirements-interview` + a competitor scan. Output: should we build this, and what's v1?
- **review-everything** — `pr-review` + `security-gate` + `performance-profiler` + `ux-critique` + `quality-hunt` in parallel, combined into one P0/P1/P2 list
- **ship-cycle** — `ship-and-cleanup` + `doc-cleanup` + `lessons-learned` after merge

Gaps I notice when actually using these on real projects:

- **Post-mortem template** for when something breaks in prod
- **Migration safety review** for DB schema changes, breaking API changes, deprecations
- **Observability review** — does the new code emit useful logs, metrics, traces?
- **Architecture decision record** — capture why X over Y in the moment, not after the fact
- **Estimation prompt** — bound the work realistically before committing
- **Rollback plan review** — what's the fast revert when the rollback signal fires?

Issues and PRs welcome.

## Design choices

The prompts share four traits:

**Adversarial by default.** They ask the model to push back, rate confidence, and STOP rather than guess when context is thin. Sycophantic output is what I'm trying to avoid.

**Explicit confidence scale.** Whenever a prompt asks for confidence, it's on a fixed scale (1–3 guessing, 4–6 informed but unverified, 7–8 verified by reading code, 9–10 verified with test or external source). Same anchor everywhere.

**P0/P1/P2 triage.** Findings get sorted into one of three buckets. Easy to scan, easy to act on.

**Skip with a reason; never fabricate.** When a section doesn't apply, the prompts say so instead of padding to look thorough. Catches a lot of slop.

## Where these come from

These are synced from my espanso config (a text-expansion tool I use locally). I edit the espanso file, run a small script, and the script writes each trigger to a file here.

```
   espanso config (private)              this repo (public)
   ────────────────────────              ──────────────────
   base.yml                              planning/*.md
     ::P1, ::P3, ::J, ::QV, ...   ──►   dev/*.md
                                  sync   ux/*.md
                                         qa/*.md
                                         ...
   (source of truth)                     (published mirror)
```

Every commit through this repo goes through a safety check (pre-commit hook + GitHub Action + branch protection on master) that blocks personal info and credentials from leaking. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full setup.

## License

MIT. Use them however you want.
