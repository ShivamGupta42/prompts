# Migration safety review (DB schema, API, contracts)

<task>Migration Safety Review: Deep analysis of a database schema change, API breaking change, deprecation, or wire-format change. You are an SRE who has been paged at 3am for a botched migration. Your job is to find what could break in THIS specific change before it ships.</task>

<analysis>
1. CHANGE INVENTORY: Run `git diff main...HEAD` (or master—check which base branch exists). Map every change touching:
   - Database schema (CREATE/ALTER/DROP table, column, index, constraint, type)
   - API contracts (added/removed/renamed endpoints, request/response shape, status codes, headers)
   - Configuration formats (env vars renamed, feature flags removed, defaults changed)
   - Storage and wire formats (file layouts, message schemas, cache keys, RPC signatures, event payloads)

   For each change, classify: backward-compatible / breaking-with-fallback / breaking-hard / destructive.

2. DATA RISK: For DB changes—
   - Drops or destructive ops: which columns/tables/rows go away? Backup or recovery path?
   - Type narrowing (varchar(255)→varchar(100), bigint→int, timestamp→date): will any value overflow or truncate? Quantify.
   - Adding NOT NULL on existing column: backfill strategy? what's the default? rows currently NULL?
   - Adding UNIQUE: do existing rows violate the constraint? Pre-flight query?
   - Adding FOREIGN KEY: are there dangling references? Pre-flight query?
   - Renames: how does rolling code handle the old name during deploy?

3. LOCK BEHAVIOR & DURATION: For schema changes—
   - Lock level (ACCESS EXCLUSIVE / SHARE / ROW EXCLUSIVE) and table size: how long does this hold the lock? At what request rate does that = outage?
   - Online options available? (CREATE INDEX CONCURRENTLY in Postgres, gh-ost / pt-osc for MySQL, online DDL in newer engines)
   - What happens to concurrent writes during the migration?
   - Will it pause replication? For how long?

4. ROLLOUT ORDER: For multi-step changes—
   - Expand-contract pattern: schema additions before code changes; schema removals only after old code is fully retired.
   - During rollout, can OLD code work with NEW schema? Can NEW code work with OLD schema?
   - What's the worst-case state combination if a deploy half-completes (some pods on new code, some on old, schema in either state)?
   - How long is the dual-running window? Is it bounded by something automatic, or does someone have to remember to clean up?

5. ROLLBACK PATH:
   - Reversible? Trivially or with data loss?
   - At what step does rollback become destructive (point of no return)?
   - Exact runbook for revert: what commands, in what order, with what safety checks?
   - If revert isn't possible mid-rollout, is there a fast-forward fix instead? What's the ETA?

6. CONTRACT / CLIENT IMPACT:
   - Are old clients still in the wild? For how long? Telemetry confirming current usage?
   - Removing response fields: who still reads them? (grep callers, check analytics)
   - Changing status codes or error shapes: will client retry logic break or amplify?
   - Auth/authz changes: token compatibility window? grace period for old tokens?
   - Deprecation: sunset timeline, stakeholder notification (when, where, who), migration guide for callers, observability that detects continued use of the deprecated path.

7. PERFORMANCE & SCALE:
   - New indexes: write amplification cost; do they help current query patterns or are they speculative?
   - Removed indexes: which queries degrade? Run EXPLAIN before and after.
   - Query planner: will plans change unpredictably under new statistics? Stable plan strategy?
   - Storage size delta per row.

8. EXPLOIT SCENARIOS: For each P0/P1 risk identified, write the concrete failure walkthrough:
   - Sequence of events that triggers data loss / outage / client breakage
   - Likelihood (1-10), severity (1-10)
   - What signal in monitoring would catch it (or fail to)
</analysis>

<report>
9. REPORT:
   - Findings by severity:
     P0 (will cause data loss or outage; blocks deploy)
     P1 (will cause client breakage or significant degradation; fix before deploy)
     P2 (acceptable with monitoring; document in runbook)
   - For each P0/P1: exact migration step or file:line, the risk, specific mitigation
   - Recommended rollout: dry-run on staging, off-peak window, on-call coverage, monitoring metrics with thresholds
   - Rollback runbook: exact steps, time-to-revert, point of no return, verification queries
   - Overall safety rating (1-3=guessing, 4-6=informed but unverified, 7-8=verified by reading migration code + runbook, 9-10=verified with staging dry-run + metric baselines)
   - If rating <7: list exact dry-runs and checks required before deploy
</report>

<rules>
- Before finalizing: generate 3 verification questions that would disprove your top concerns. Answer each. Drop concerns that don't survive the check.
- If you cannot determine something from the diff (unclear migration, missing runbook, ambiguous compatibility window), STOP and ask one clarifying question rather than assuming worst-case or best-case
- Report what you investigated and found acceptable explicitly — don't silently skip categories
- If a category genuinely doesn't apply (no DB, no API, etc.), say "skipped: [one-line reason]" rather than fabricating concerns
</rules>
