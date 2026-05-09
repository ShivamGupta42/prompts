# Live browser QA via automation


Live Browser QA: The server is already running at the URL provided above. Use your browser automation tools to test all feature branch changes through the actual browser and database.

1. DIFF ANALYSIS: Run `git diff main...HEAD` (or master—check which base branch exists). List every user-facing change. Categorize: new pages/routes, modified UI components, API changes, data model changes. This is your test plan—every change needs verification.

2. DB SETUP: Read `.env*` files for database connection details (DATABASE_URL, DB_HOST, DB_PORT, DB_NAME, POSTGRES_*, etc.). Connect via `psql` or equivalent CLI. Seed any test data needed to exercise the changes—users, records, relationships, edge-case states. Document every record you create (table, id, purpose) for cleanup.

3. BROWSER TESTING: For each user-facing change from step 1:
   a. Navigate to the affected page at the server URL
   b. Screenshot the page BEFORE interacting (baseline)
   c. Happy path: interact with realistic data—click buttons, fill forms, submit, navigate. Complete the full user flow, don't stop at the first screen.
   d. Screenshot AFTER key interactions (evidence of result)
   e. Edge cases: empty inputs, invalid data, boundary values, rapid double-clicks, back button after submit
   f. Error checking: run JS in the page to check for console errors, broken images, failed network requests
   g. Data verification: after form submissions or actions, verify the DB state changed as expected

4. REGRESSION: Navigate to 2-3 pages NOT modified by this branch. Screenshot them. Any layout breaks, missing data, console errors? Compare behavior to what you'd expect from a working app.

5. REPORT:
   - Per change: PASS/FAIL with screenshot evidence and what you observed
   - Bugs found: exact steps to reproduce, expected vs actual, severity (P0=broken, P1=degraded, P2=cosmetic)
   - Test data created: table, id, purpose (for cleanup)
   - Overall branch readiness score (1-10) with specific blockers if <8

RULES:
- Screenshot BEFORE and AFTER every interaction—visual evidence is mandatory
- Actually USE the UI—fill forms with real values, click through flows, don't just check elements exist
- If a page errors or looks wrong, run JS in the page to investigate before reporting
- Create test data as needed during testing—always document what you created
- Don't try to start or restart the server—it's already running
- If the feature requires auth, look for test credentials in .env or seed a test user
