# prompts

Most AI prompts ask for output. These ones also ask the model to rate its confidence and flag what it can't actually determine, so you can tell which parts are solid and which are guesswork.

Plan critique, PR review, UX evaluation, validation, security analysis, and a few more. Copy any body into Claude, Codex, Gemini, or ChatGPT. Nothing to install.

## How they're organized

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

Click into [planning/](planning/), [dev/](dev/), [ux/](ux/), [qa/](qa/), [marketing/](marketing/), [learning/](learning/), or browse the full file-level list in [INDEX.md](INDEX.md).

## How to use them

The easiest way is to copy the body of any prompt and paste it into your chat alongside whatever you're working on. That's it.

If you have tooling that pulls prompts from URLs, the raw URL is `https://raw.githubusercontent.com/ShivamGupta42/prompts/master/<folder>/<name>.md`.

If you want to change them to match how you think, fork the repo and point your tools at your fork.

## How the prompts compose

The prompts split into two layers. Layer 1 is single-purpose: each file applies one perspective (a JTBD evaluation, a UX critique, a validation-criteria pass). Layer 2 is orchestrators: prompts that classify the work in front of them and pull in the right Layer-1 perspectives.

```
       plan-critique-3x          <- Layer 2: orchestrator
             │
             │  classifies the plan, then pulls:
             ▼
   ┌─────────┴─────────┬───────────────────────┐
   ▼                   ▼                       ▼
   jtbd          ux-critique         validation-criteria   <- Layer 1: lenses
   (skip if          (skip if              (always)
    backend)         backend)
```

You can use any Layer-1 prompt on its own when you want one perspective. Use the orchestrators when you want a structured multi-perspective review that adapts to whatever you throw at it.

## Why these exist

Most AI critiques default to *"will it work?"* and skip the harder questions: will it matter to a user, and how will we know it's done? Splitting those concerns into separate prompts (and then composing them) is what lets a single trigger like `plan-critique-3x` produce a critique that's technical, user-focused, *and* shippable instead of just one of those.

The prompts share a few traits:

**Adversarial by default.** They ask the model to push back, rate confidence, and STOP rather than guess when context is thin. Sycophantic output is what I'm trying to avoid.

**Explicit confidence scale.** Whenever a prompt asks for confidence, it's on a fixed scale (1–3 guessing, 4–6 informed but unverified, 7–8 verified by reading code, 9–10 verified with test or external source). Same anchor everywhere.

**P0/P1/P2 triage.** Findings get sorted into one of three buckets. Easy to scan, easy to act on.

**Skip with a reason; never fabricate.** When a section doesn't apply, the prompts say so instead of padding to look thorough. This catches a lot of slop.

If a prompt doesn't work for you, [open an issue](CONTRIBUTING.md).

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
