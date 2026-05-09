# Validation criteria lens

Apply this lens to define **how we know the work succeeded**. Always run on plans that involve any code, config, or content change. Even pure docs work has a "did this make the docs more accurate" criterion.

Output a structured checklist grouped by priority (P0/P1/P2). Every criterion must be observable — describe what behavior, output, or state proves the work is done.

## 1. Inventory the changes

List every change in scope by category: feature / bugfix / refactor / config / test / docs / infra. For each, one sentence on what it does. This becomes the spine of the rest of the lens.

## 2. Per-change "done"

For each change, define done concretely:

- What observable behavior proves it works?
- What inputs to feed in?
- What outputs or state changes to verify?
- Where to look (file, log, UI element, DB row, metric)?

## 3. Happy path

For the primary use case, write a step-by-step verification with **concrete test data**. No `<placeholder>` syntax — actual values someone can paste and run. Include the expected result at each step.

Example shape:
```
Step 1: POST /api/orders with body {"sku":"SKU-12345","qty":2}
Expected: 201, body contains "order_id" matching ^[a-f0-9-]{36}$
Step 2: GET /api/orders/<order_id>
Expected: 200, status="confirmed", line_items length 1
```

## 4. Edge cases

For each user-facing or boundary-touching change, list edge cases:

- Empty / null / missing inputs
- Boundary values (0, 1, max-int, max-string-length, negative)
- Invalid input (wrong type, malformed, oversized, encoding edge cases)
- Concurrent access / race conditions
- Partial failure (network drop mid-request, retry storms, half-written state)
- Unicode and i18n where relevant (RTL, combining chars, zero-width, emoji)

## 5. Integration points

What upstream systems feed this code? What downstream systems consume it? For each:

- What contract must hold (request/response shape, event ordering, idempotency)?
- How to verify it still holds after this change?

If the change adds a new integration, also list: what happens when the integration is unavailable?

## 6. Regression check

What existing behavior must NOT change? List specific scenarios. For UI work, list pages or flows that should look unchanged. For backend, list endpoints whose response shape must remain stable. For shared utilities, list the existing callers.

## 7. Performance criteria (if relevant)

Latency, throughput, memory targets. State acceptable bounds and how to measure. Skip with a one-line reason if the change is performance-neutral.

## 8. Security validation (if relevant)

Auth gates, input sanitization, data exposure paths, secret handling. What to verify? Skip with reason if no security surface touched. If unsure whether security is touched, say so and recommend running a security-focused review separately.

## 9. Rollback signal

What observable signal would say "revert immediately"? Error rate spike (above what threshold?), p99 latency over X, customer complaints in Y channel, alert from Z dashboard? State the threshold, not just the channel.

## 10. Manual vs automated

For each criterion above, mark whether it's verifiable by:

- **Automated** — covered (or to-be-covered) by a test in CI
- **Manual** — requires a human to click, read, or observe
- **Production-only** — only verifiable after deploy (e.g., real-traffic patterns, real-user devices)

## 11. Environment requirements

What setup is needed to run validation? Specific seed data, env vars, feature flags, accounts, fixtures? List exact setup steps a fresh contributor could follow without prior context.

---

## Output format

Group everything as a checklist:

```
P0 — blocks release
[ ] <criterion>
    Test: <concrete test data and expected result>
    Where: <file / endpoint / UI / log>
    How: automated | manual | production-only

P1 — should verify before release
[ ] <criterion>
    Test: <…>
    …

P2 — nice to verify
[ ] <criterion>
    …

Rollback signal: <observable threshold>
Environment setup: <specific commands or steps>
```

## Confidence rating

After writing the criteria, rate (1–10) how confident you are they're complete:

- 1–3: guessing at requirements
- 4–6: informed but unverified
- 7–8: verified by reading code or spec
- 9–10: verified with stakeholder sign-off

If confidence is below 7, name what's missing and what would lift it.

## Rules for this lens

- Every criterion is observable. "User can log in" is a criterion. "Login works" is not.
- No `<placeholder>` test data in the output. Use real strings, numbers, IDs that someone can paste and run.
- If a section genuinely doesn't apply, skip it with a one-line reason. Don't fabricate criteria to fill sections.
- Adversarial gut-check before finishing: would a hostile QA find a P0 you missed? If yes, add it. If unsure whether the criteria are exhaustive, say so and recommend a separate adversarial QA pass.
