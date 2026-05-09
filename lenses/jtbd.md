# JTBD lens

Apply this lens to evaluate the **user job** that the work in front of you is hired to do. Use it on user-facing plans (features, flows, UI changes) — skip for pure backend or infra work.

## The job

State the job in this form:

> When [situation], a person wants to [motivation], so they can [outcome].

Be concrete. "When I'm trying to recall a decision from last week" is a job; "when I'm using the app" is not.

## Four forces (rate each 1–10)

For the persona this work targets:

- **Push** (away from current solution): what frustration drives them to look for something new? What broke their patience?
- **Pull** (toward this solution): what specifically about this approach attracts them? What's the magnetic promise?
- **Anxiety** (about switching): what uncertainty or fear makes them hesitate? Setup cost, learning curve, lock-in, social risk?
- **Habit** (with current solution): what inertia keeps them where they are? Even if it's worse, what's familiar about it?

A great solution stacks push + pull above anxiety + habit. If push and pull are weak, the work won't get hired no matter how good the implementation is.

## Competing solutions

List 3–5 alternatives the persona might hire instead — including non-obvious ones:

- Direct competitors (the obvious)
- Indirect substitutes (a spreadsheet, a Slack channel, a notebook, a sticky note)
- Doing nothing (the most-hired competitor in most categories)
- Hiring a person (assistant, agency, freelancer)

For each, name the trade-off the user accepts to choose it. That trade-off is what your work has to beat.

## Journey friction

Walk through the persona's full path from problem-awareness → trying → adopting → habituated. Mark friction and anxiety at each stage:

| Stage | What happens | Friction (1–10) | Anxiety (1–10) |
|---|---|---|---|
| Problem awareness | | | |
| Solution search | | | |
| Evaluation | | | |
| First use | | | |
| Repeat use | | | |

## Communication at critical moments

For each moment that triggers anxiety, doubt, or decision (first error, paywall, account creation, abandonment risk), rate 1–10 how well the system communicates *right now*. Concrete examples beat generic principles. Quote real copy where possible.

## Hiring vs firing

- **Hiring**: what gets this solution hired? What's the moment of decision?
- **Firing**: what would get it fired? The fire conditions are usually more specific and more painful than the hire conditions — name them. Most products lose users for one or two specific reasons, not vague dissatisfaction.

## Success metric

What single observable behavior would prove this work succeeded for the job? Not vanity metrics (signups, MAUs, page views) — behavior that maps to the job being done well. Examples: "user returns within 7 days for the same task", "user completes the flow without contacting support".

## Single highest-impact improvement

Pick ONE change that would most move the needle on the job. Rate confidence:

- 1–3: guessing
- 4–6: informed but unverified
- 7–8: verified via user evidence (interviews, usage data)
- 9–10: verified with data or controlled testing

What specific evidence would lift confidence to 9+?

## Rules for this lens

- Concrete beats abstract. "When the user is between meetings" beats "in their daily flow."
- If you can't picture one specific person doing this job, the persona is too vague — fix that before continuing.
- Skip sections that genuinely don't apply with a one-line reason. Don't fabricate force ratings or journey stages to fill the structure.
- This lens is about *demand* (does the job exist, is it strong enough?) — not *supply* (can we build it?). Architecture concerns belong in a different lens.
