# prompts

A small library of reusable prompts for working with AI assistants.

These are the prompts I actually use, every day, to plan work, critique my own thinking, evaluate user impact, and ship with some confidence that I haven't missed something obvious.

Each one is a self-contained markdown file. Copy the body, paste it into your AI chat (Claude, Codex, Gemini, ChatGPT — they all work), and the prompt does the work. No setup, no library to install, no API key.

## How they're organized

Browse the [INDEX](INDEX.md) for everything in one list, or look in the folder that matches what you're trying to do:

| Folder | Use when you're… |
|---|---|
| [planning/](planning/) | designing what to build, critiquing a plan, running a multi-perspective review, or interviewing yourself for clearer requirements |
| [dev/](dev/) | reviewing a PR, fixing issues, evaluating feedback, refreshing docs, shipping work |
| [ux/](ux/) | evaluating user impact — JTBD framing, UI/UX critique, friction-to-fix walkthroughs |
| [qa/](qa/) | building manual test plans, deep security analysis, performance profiling, finding similar bugs |
| [marketing/](marketing/) | distribution strategy, GTM, campaign critique, marketing audits |
| [learning/](learning/) | extracting generalizable lessons after a session |
| [validation-criteria.md](validation-criteria.md) | (cross-cutting) defining how you'll know the work succeeded |

## Use them three ways

1. **Paste inline** — copy the prompt body, paste into any AI chat alongside your work. Done.
2. **Fetch via raw URL** — point your own orchestrator at `https://raw.githubusercontent.com/ShivamGupta42/prompts/master/<folder>/<name>.md` and let your tooling pull it.
3. **Fork and adapt** — clone the repo, edit prompts to match how you think, point your tools at your fork.

## Why these prompts exist

Most AI critiques default to technical lenses — *will it work?* — and skip the harder questions: *will it matter to a user?* and *how will we know it's done?* The prompts here are organized so you can pull a single lens (JTBD, UX, validation) standalone, or compose them into bigger orchestrators (the `plan-critique-*` files in `planning/` do this — one trigger that classifies a plan and applies the right lenses).

A few design choices worth naming:

- **Adversarial by default.** Most prompts ask the model to push back, find what's missing, rate confidence, and STOP rather than guess when context is thin. Sycophantic AI output is the failure mode these are designed against.
- **Confidence anchors are explicit.** Every prompt that asks for confidence rates it on a fixed scale (1–3 guessing, 4–6 informed but unverified, 7–8 verified by reading code, 9–10 verified with test or external source). Same anchor everywhere — no ambiguity.
- **Prioritize as P0/P1/P2.** Findings, issues, validation criteria — all triaged into the same three buckets. Easy to scan, easy to act on.
- **Skip with a reason; never fabricate.** When a section doesn't apply, the prompts say "skip with a one-line reason" — not "fill it in to look thorough." This catches a lot of low-quality AI output that pads to fill structure.

If you find a prompt that doesn't work the way you think, [contributions are welcome](CONTRIBUTING.md).

## Provenance and trust

These prompts are synced from a personal espanso text-expansion config. The espanso config is the source of truth; this repo is the published mirror. A small sync script extracts each trigger and writes it here.

Every commit goes through a safety stack (pre-commit hook + GitHub Action + branch protection on master) that blocks personal info, credentials, and accidental leaks. See [CONTRIBUTING.md](CONTRIBUTING.md) for details. Your contributions will go through the same gates.

## License

MIT — see [LICENSE](LICENSE). Use them, fork them, adapt them, ship them.
