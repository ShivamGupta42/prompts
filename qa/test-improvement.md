# `::QT` — Analyze test coverage and propose improvements

> **Use this prompt:** copy the body below and paste it into any AI chat.
> Synced from a personal espanso text-expansion config on 2026-05-09.

---

Test Improvement Analysis: Analyze the current test coverage for this feature and propose improvements. 1) INVENTORY: List existing tests by type (unit, integration, e2e). Rate coverage (1-10) per component. 2) GAPS: What code paths have no tests? What edge cases are untested? What failure modes are unverified? 3) UNIT TESTS: For each untested function/method—propose specific test cases with inputs and expected outputs. Focus on: boundary values, error conditions, state transitions. 4) INTEGRATION TESTS: What component interactions are untested? Propose tests for: API contracts, database operations, external service calls, event flows. 5) MOCKING STRATEGY: What should be mocked vs real? Identify flaky test risks. 6) TEST DATA: What fixtures or factories are needed? Propose reusable test helpers. 7) PRIORITIES: Rank proposed tests by: risk coverage (what breaks if untested), implementation effort (S/M/L), flakiness risk. 8) QUICK WINS: Which 3 tests would give the most coverage for least effort? Output as actionable checklist with specific test file locations and test case names.
