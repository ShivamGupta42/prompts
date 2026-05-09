# Post-mortem template for incidents

<task>Post-Mortem: Structured analysis of an incident that already happened. You are an SRE writing the public post-mortem for an outage. Your job is to surface what actually went wrong (not the easy story), identify specific actions that would prevent recurrence, and do it without blaming individuals.</task>

<context>
Provide before starting:
- Incident name / ID / date
- Severity (SEV1/2/3 or equivalent)
- Detection: how was it first noticed? At what time?
- Mitigation: what action restored service? At what time?
- Resolution: when was the incident fully closed? Final fix landed when?
- Available artifacts: logs, metrics, alerts, chat transcripts, code diffs from the incident window
</context>

<analysis>
1. INCIDENT SUMMARY: One paragraph. What happened, who was affected, how long, what was the user-facing impact.

2. TIMELINE: Minute-by-minute (or hour-by-hour for longer incidents). Timestamps required. Capture:
   - First signal (alert fired, customer report, dashboard anomaly)
   - Acknowledgement (paging, on-call response)
   - Investigation steps (what was tried, what was ruled out, what was assumed)
   - Mitigation attempts (what was done, what worked, what didn't)
   - Resolution and rollback (final fix)
   - Decision points: who decided what, with what info available at the time
   Note where time was lost (waiting for someone, looking at the wrong dashboard, retrying the wrong thing). Lost time is usually where the next action items live.

3. IMPACT:
   - Users affected (count or %)
   - Duration of full outage / degraded service (with timestamps)
   - SLO/SLA impact (error budget burned; breach if applicable)
   - Financial impact if quantifiable
   - Trust/reputation impact (customer complaints, public discussion, support volume)

4. ROOT CAUSE — 5 whys or similar:
   - The proximate cause (what immediately broke)
   - The mechanism (why was that broken thing exposed/triggered now? what changed?)
   - The contributing systems (what allowed this to happen at all?)
   - Don't stop at "human error" or "edge case"—those are gaps in the system that produced the error, not root causes.
   - Rate confidence the root cause is correct (1-10). If <8, what investigation would lift it?

5. CONTRIBUTING FACTORS: What made it worse than it had to be? Examples:
   - Detection latency (alert thresholds too lenient, missing observability, wrong signal)
   - Response latency (wrong on-call paged, paging silent, runbook out of date)
   - Mitigation latency (rollback unclear, dependencies not isolatable, fix risky)
   - Communication (incident channel late, status page delayed, customer comms missing)
   - Decision-making (escalation threshold unclear, too few or too many people in the room)

6. WHAT WENT WELL: Real strengths exposed by the incident—what worked. (Not optional padding; this captures process patterns worth keeping.) Examples:
   - Quick alerting on metric X
   - Clear runbook for system Y
   - Effective rollback path
   - Good incident-channel etiquette and handoffs

7. WHAT DIDN'T GO WELL: The other side. Be specific.

8. WHERE WE GOT LUCKY: What could have been worse but wasn't? Near misses noticed during the incident. These often reveal the next incident's seed.

9. COUNTERFACTUALS: For each major decision in the timeline, what's the world where the decision went differently? Would the incident have been shorter, longer, or about the same? This is where the highest-leverage action items hide.

10. ACTION ITEMS: Specific, owned, prioritized. Not "improve X" or "we'll be more careful." Each must have:
    - What concrete change (a code PR, a runbook update, an alert added, a process change, a doc clarified)
    - Owner (a specific person, not a team)
    - Target date (a specific deadline)
    - How we'll verify it landed (the observable evidence)
    Group as P0 (must ship to prevent recurrence) / P1 (should ship to reduce blast radius) / P2 (improvements that came up but aren't urgent).

11. PATTERN HUNT: Has this kind of incident happened before? Same root cause, similar mechanism, related system? If yes—what changed since the last time, and why didn't the previous fix prevent this? If no—what family of incidents does this belong to, and what other systems share the underlying weakness?
</analysis>

<report>
12. REPORT: Output the post-mortem in this structure:
    - Title / Severity / Date
    - Incident summary (one paragraph)
    - Timeline (table or numbered list with timestamps)
    - Impact
    - Root cause (with confidence rating)
    - Contributing factors
    - What went well
    - What didn't go well
    - Where we got lucky
    - Counterfactuals
    - Action items (P0/P1/P2 with owner + date + verification)
    - Pattern hunt note

    Keep tone factual. No blame on individuals. Systems and processes only.
</report>

<rules>
- This is BLAMELESS. Replace "X did Y wrong" with "the system allowed Y to happen." If a person made a decision, ask why the system rewarded or permitted that decision—don't ask whether the person was good.
- "Edge case" is not a root cause. "Human error" is not a root cause. Both are gaps in the system that produced the error.
- Action items must be specific enough that a different team could execute them. "Improve monitoring" is not specific. "Add alert on metric X with threshold Y, owner Z, by date W, verified by triggering condition in staging" is.
- Rate confidence on the root cause. If <8, propose what investigation would raise it before publishing.
- If important context is missing (logs unavailable, decisions made off-channel, no one wrote down the timeline), STOP and ask for the missing artifacts rather than inventing them.
</rules>
