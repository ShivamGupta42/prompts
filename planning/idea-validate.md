# Idea validation orchestrator (GO/NO-GO with v1 scope)

<task>Idea Validate: Adversarial multi-lens evaluation of an idea BEFORE any code or specs exist. Classifies the idea, applies relevant lenses (JTBD, requirements interview, competitor scan, risk surface, resource fit), dedupes concerns, runs a verifier loop, and produces a GO / NO-GO / GO-WITH-MODIFICATIONS verdict with v1 scope or kill criteria. Use this before you commit time to building.</task>

<analysis>
STAGE 1 — CLASSIFY THE IDEA (always)
What kind of work is this?
- new-product: standalone thing for users (full lifecycle commitment)
- new-feature-in-existing-product: integrates with what we ship today (capacity + integration risk)
- internal-tool: lower bar; ROI is "team productivity", not market fit
- research-or-experiment: success = learning, not shipping
- something-else: state what

For each lens, decide APPLY or SKIP with one-line reason. Output a classification table.

Lens preconditions:
- JTBD (always): every idea has a user, even internal tools. Skip only if work is purely scratching the builder's curiosity.
- Requirements interview (when scope is ambiguous): apply if the idea has multiple plausible interpretations. Skip if scope is concrete.
- Competitor scan (always for new-product / new-feature; skip for research-or-experiment): what's already out there?
- Risk surface (deep for new-product; lighter for features; skip for research): legal, security, ethical, operational, brand
- Resource fit (always): time/people/money cost vs. expected value

Output:
| Lens | APPLY/SKIP | Reason |

STAGE 2 — APPLY LENSES (with dependency-aware ordering, NOT free-for-all parallel)

The lenses have real dependencies. Each subsequent lens often uses the output of an earlier one. Run them in three substages:

STAGE 2a — REQUIREMENTS INTERVIEW (only if scope ambiguous; STOP and ask before continuing)
If the idea has multiple plausible interpretations, clarify the scope FIRST so other lenses operate on the right target. Ask one clarifying question at a time. For each: present concrete options with a recommended pick. Cover both functional (behaviors, edge cases, validation rules, permissions) and non-functional (performance, scale, security, accessibility, observability). STOP and wait for answers before proceeding to Stage 2b.
If scope is concrete enough to skip this lens, say so with a one-line reason and proceed.
Full spec: https://raw.githubusercontent.com/ShivamGupta42/prompts/master/planning/requirements-interview.md

STAGE 2b — JTBD (always; defines the job that Stage 2c reasons about)
Apply the JTBD framework (per ::J): job statement template "When [situation], a person wants to [motivation], so they can [outcome]." Rate four forces 1-10 (push/pull/anxiety/habit). Journey friction. Single highest-impact improvement with confidence.
The job statement from this stage is INPUT to Stage 2c's competitor scan.

STAGE 2c — COMPETITOR SCAN + RISK SURFACE + RESOURCE FIT (parallel; all depend on 2b)

COMPETITOR SCAN: List 3-7 alternatives the user might hire INSTEAD to do the same job (from 2b). Include direct competitors, indirect substitutes (spreadsheet, Slack channel, notebook), DOING NOTHING (the most-hired competitor in most categories — always include this), and hiring a person. For each: trade-off accepted, gap THIS idea fills.

RISK SURFACE: For each applicable risk family (legal, security, ethical, operational, brand), name 1-3 concrete risks. Skip families that don't apply with a one-line reason.

RESOURCE FIT: Estimate cost (time / capacity / money — be honest about planning fallacy). Estimate value (who gets what; how confident 1-10). Does the ratio pencil?

For deeper standalone passes: ::J (JTBD), ::PR (requirements interview).

STAGE 3 — DEDUPE AND SYNTHESIZE
Walk all lens outputs. Merge overlapping concerns:
- JTBD says the job is weak + competitor scan says incumbents own it well → consolidated "demand exists but is well-served"
- Risk surface flags legal exposure + resource fit shows high cost → consolidated "high-cost-low-confidence-on-clearance"
Surface trade-offs that emerge across lenses, not just within them.

STAGE 4 — CROSS-LENS DECISION POINTS
What binary or trade-off choices does the team need to make explicitly?
- Build vs buy (use the competitor) — when this is a legitimate choice
- v1 minimum vs comprehensive — what's the smallest thing that proves the concept?
- Solo build vs team alignment — does this need stakeholder buy-in before starting?
- Now vs later — is this the right time given other priorities?

STAGE 5 — VERIFIER LOOP (max 3, confidence-gated)
Adversarial check. The verifier asks the hardest questions:
- What's the strongest case AGAINST building this? Who would argue we shouldn't?
- Did we miss a competing solution that would obviate this idea?
- Is the user job real (someone will pay/use repeatedly) or imagined (sounds plausible but unconfirmed)?
- What evidence would convince us we're wrong? Have we sought it?

Outputs: (a) new findings, (b) confidence (1-10) that the evaluation is exhaustive.
Termination:
- Stop if confidence ≥ 8
- Stop if confidence < 8 BUT no new findings emerged this pass (diminishing returns)
- Otherwise iterate up to 3 total

STAGE 6 — VERDICT (must commit; no "it depends" without naming what depends on what)

Output one of three verdicts with confidence (1-10):

GO — proceed to planning. Include:
- Proposed v1 scope (smallest version that proves the concept)
- Success metric (how we'll know v1 worked)
- Kill criteria (what would make us stop)
- Estimated cost of v1 (time/people/money)
- Top 3 risks accepted

GO-WITH-MODIFICATIONS — proceed but change something material first. Include:
- What modifications, why, and who decides
- Then the GO bullets above

NO-GO — don't build it. Include:
- Which constraint binds: no demand / no differentiation / wrong time / too costly / risk too high
- What would change to make it GO (concrete trigger)
- What to do instead with the same time/capacity
</analysis>

<report>
OUTPUT in this order:

CLASSIFICATION TABLE (per Stage 1)

VERIFIER LOOP TRACE
- Iteration 1: confidence X, N new findings (or none)
- (Iteration 2 if applicable)
- Stopped because: confidence reached / no new findings / 3-iteration cap

LENS FINDINGS (synthesized)
- JTBD: synthesized job statement, key forces, top friction
- Requirements: ambiguities resolved + open questions
- Competitor scan: gap THIS idea fills (or "competitors own this")
- Risk surface: top 3 risks with severity (or "skipped: research project")
- Resource fit: cost vs value with confidence

CROSS-LENS DECISION POINTS (or "no major decision points")

VERDICT
- GO / GO-WITH-MODIFICATIONS / NO-GO
- Confidence: N/10
- (Required content per Stage 6)

WHAT WAS SKIPPED (each skipped lens + reason)
</report>

<rules>
- Confidence anchors: 1-3=guessing, 4-6=informed but unverified, 7-8=verified by reading research/data, 9-10=verified with primary user evidence
- If a lens doesn't apply, say so with a one-line reason — never fabricate findings
- The DEDUPE step is mandatory; don't just concatenate lens outputs
- "Doing nothing" is always a competitor — if the user is currently doing nothing about this problem, that's a signal the demand might be weak
- The verdict MUST commit. Don't return "it depends" — if it depends, name what it depends on and ask one clarifying question, then return a verdict.
- For deeper single-lens passes after this orchestrator runs, fall back to ::J (JTBD), or fetch the full lens specs from the URLs above.
- If important context is missing (vague idea, no target user, no concrete value prop), STOP and ask one clarifying question rather than running the full evaluation on air
</rules>
