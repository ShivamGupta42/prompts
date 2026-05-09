# prompts

Prompts I use with AI assistants. They cover planning, code review, UX critique, validation, and a few other things I do repeatedly.

Each one is a markdown file. Copy the body into your AI chat (Claude, Codex, Gemini, ChatGPT all work fine). Nothing to install.

## How they're organized

The full list lives in [INDEX.md](INDEX.md). Or by category:

| Folder | What's in it |
|---|---|
| [planning/](planning/) | plan critiques, requirements interviews, multi-perspective reviews |
| [dev/](dev/) | PR review, fix issues, doc cleanup, ship work |
| [ux/](ux/) | jobs-to-be-done, UI/UX critique, friction-to-fix |
| [qa/](qa/) | manual test plans, security analysis, performance, finding similar bugs |
| [marketing/](marketing/) | distribution, GTM, campaign critique, audits |
| [learning/](learning/) | lessons learned after a session |
| [validation-criteria.md](validation-criteria.md) | how to know the work succeeded (used everywhere) |

## How to use them

The easiest way is to copy the body of any prompt and paste it into your chat alongside whatever you're working on. That's it.

If you have tooling that pulls prompts from URLs, the raw URL is `https://raw.githubusercontent.com/ShivamGupta42/prompts/master/<folder>/<name>.md`.

If you want to change them to match how you think, fork the repo and point your tools at your fork.

## Why these exist

Most AI critiques default to "will it work?" and skip the harder questions: will it matter to a user, and how will we know it's done? So I split those concerns into separate prompts. You can pull one (JTBD, UX, validation) on its own, or compose them. The `plan-critique-*` files in `planning/` show this — one trigger classifies the plan and pulls in the right pieces.

The prompts share a few traits:

**Adversarial by default.** They ask the model to push back, rate confidence, and STOP rather than guess when context is thin. Sycophantic output is what I'm trying to avoid.

**Explicit confidence scale.** Whenever a prompt asks for confidence, it's on a fixed scale (1–3 guessing, 4–6 informed but unverified, 7–8 verified by reading code, 9–10 verified with test or external source). Same anchor everywhere.

**P0/P1/P2 triage.** Findings get sorted into one of three buckets. Easy to scan.

**Skip with a reason; never fabricate.** When a section doesn't apply, the prompts say so instead of padding to look thorough. This catches a lot of slop.

If a prompt doesn't work for you, [open an issue](CONTRIBUTING.md).

## Where these come from

These are synced from my espanso config (a text-expansion tool). I edit the espanso file, run a small script, and the script writes each trigger to a file here. The espanso config is the source; this repo is the published copy.

Every commit goes through a safety check (pre-commit hook + GitHub Action + branch protection on master) that blocks personal info and credentials from leaking. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full setup.

## License

MIT. Use them however you want.
