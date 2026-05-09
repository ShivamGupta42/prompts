# prompts

Reusable prompt fragments for AI planning workflows. Loaded on demand by espanso triggers and AI agents (Claude Code, Codex CLI, Gemini CLI) via raw GitHub URLs.

## Structure

- `lenses/` — composable prompt fragments fetched dynamically by orchestrator triggers (e.g., the `::P1/P3/P5` plan critique cycles in [ofc_dotfiles](https://github.com/ShivamGupta42) espanso config)
- `safety/` — patterns and the check script for the privacy-protection safety stack
- `.github/workflows/` — server-side mirror of the local pre-commit safety scan

## Loading a lens (for AI agents)

Lenses are fetched at the raw URL pattern:

```
https://raw.githubusercontent.com/ShivamGupta42/prompts/master/lenses/<name>.md
```

Example invocation inside an orchestrator trigger:

```
3. USER IMPACT (only if user-facing or mixed):
   - Fetch and apply: https://raw.githubusercontent.com/ShivamGupta42/prompts/master/lenses/jtbd.md
   - Fetch and apply: https://raw.githubusercontent.com/ShivamGupta42/prompts/master/lenses/ux-critique.md
```

## Safety

This is a public repo with branch protection. Every commit must pass three independent layers:

1. **Local pre-commit hook** — gitleaks (API keys, tokens, AWS/GCP credentials, JWT, PEM blocks) + custom regex for personal patterns + `detect-private-key`
2. **GitHub Action** — server-side mirror of the same scans on every PR (catches `--no-verify` bypass attempts)
3. **Branch protection on master** — no direct push, PR + passing checks required

See `safety/PROVEN.md` for bait test proofs that each layer blocks what it must.

### Contributing or editing lenses

Clone, install hooks, branch, PR:

```sh
git clone git@github.com:ShivamGupta42/prompts.git
cd prompts
brew install pre-commit gitleaks   # one-time
pre-commit install                 # one-time
git checkout -b add-new-lens
# edit files
git commit -m "..."                # hooks run automatically
git push -u origin add-new-lens
gh pr create
```

## License

MIT — see `LICENSE`.
