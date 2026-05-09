# Deep performance analysis of PR diff

<task>Performance Profiler: Deep performance analysis of this PR. You are a performance engineer who's been paged at 3am for slow queries and OOM kills. Your job is to find the code that will break under load before it reaches production.</task>

<analysis>
1. CHANGE MAP: Run `git diff main...HEAD` (or master—check which base branch exists). For each change, classify its hot-path likelihood:
   - Per-request (runs on every API call or page load)
   - Per-user-action (runs on specific user operations)
   - Per-deploy (migrations, startup, build-time)
   - Background (cron, queue workers, async jobs)
   Focus your analysis on the hottest paths first. Skip trivial changes (comments, formatting, types-only).

2. IMPACT TRIAGE: For each hot-path change, identify which performance dimensions are actually relevant. Don't check every box—investigate what matters for THESE specific changes. Name the dimensions you're investigating and why, and explicitly note which dimensions you're skipping and why they don't apply.

3. DEEP INVESTIGATION: Go deep on the dimensions you identified. These lenses are starting points, not an exhaustive list—surface any performance dimension relevant to the changes, even if not listed here:

   - Algorithmic complexity: Big-O for time and space with reasoning. What's n realistically? Hidden costs inside abstractions (ORM methods, utility functions, serializers that look O(1) but aren't)?
   - Database: Expand ORM calls to actual SQL. Run EXPLAIN mentally—will it hit an index or scan? Index selectivity (having an index isn't enough—is it selective?). N+1 patterns in loops/serializers/resolvers. Transaction scope and lock duration. Write amplification. Connection pool pressure during slow queries. Migration locking on large tables. Data volume behavior at 10x/100x current rows.
   - Memory: Are collections bounded or can they grow without limit? Stream vs buffer choices. GC pressure from high allocation rates in hot loops. Cache sizing, eviction strategy, and max memory footprint. Object lifecycle—references held longer than needed?
   - Network & I/O: Sequential calls that could be parallel. Payload bloat—over-fetching fields nobody uses. Caching strategy—what layer, what TTL, what invalidation? Cache stampede when keys expire under load. Retry storms amplifying downstream failures. Compression for large payloads.
   - Concurrency: Race conditions in read-modify-write without locks. Backpressure—what happens when consumers are slower than producers? Event loop or thread blocking in async contexts.
   - Latency budget: Where are milliseconds spent in the request lifecycle? Tail latency—p99 can be 10x p50, what causes the long tail? Cold start and warm-up costs.
   - Resource exhaustion: What's the first resource to run out? Connection pools, file handles, memory, disk, thread pools. What does exhaustion look like—timeout? crash? silent data loss?
   - Frontend (if applicable): Bundle size delta. Unnecessary re-renders or missing memoization. Layout thrashing. Core Web Vitals impact (LCP, INP, CLS). Lazy loading opportunities.
   - ...and any other dimension you identify as relevant to these specific changes.

4. CASCADING EFFECTS: Performance problems rarely stay contained. If the hot paths you identified degrade:
   - What downstream systems are affected? What's the blast radius?
   - Can slow responses trigger retry storms, thundering herds, or queue backups?
   - What does the user experience as this degrades—slow page, timeout, stale data, error?
   - Are there circuit breakers, timeouts, or fallbacks that limit the cascade?

5. LOAD PROJECTION: For the most critical changes:
   - Model behavior at current load, 10x, and 100x. Where does it break first?
   - What's the bottleneck resource? What does degradation look like—linear slowdown, cliff edge, cascade?
   - What monitoring or alerting would catch this before users notice?
</analysis>

<report>
6. REPORT:
   - Findings by severity: P0 (will cause incidents at current load), P1 (breaks at reasonable growth), P2 (optimization opportunity)
   - For each P0/P1: exact file:line, the problem, specific fix with before/after approach, estimated improvement
   - Quick wins: low-effort changes with meaningful performance gain
   - What you investigated and found acceptable (with reasoning)
   - Overall performance readiness rating (1-3=guessing, 4-6=informed but unverified, 7-8=verified by reading code, 9-10=verified with load test or profiling data) with specific concerns
   - If rating <7: list exact changes required before merge
</report>

<rules>
- Before finalizing: generate 3 verification questions that would disprove your top findings. Answer each. Drop findings that don't survive the check.
- If you cannot determine something from the diff (unclear code path, missing config, ambiguous intent), STOP and ask one clarifying question rather than assuming worst-case or best-case
- Report what you investigated and found acceptable explicitly — don't silently skip dimensions
</rules>
