# Find similar bugs and propose prevention


Quality Hunt: This bug exists elsewhere. 1) Name the root pattern—what made this possible? 2) Search codebase for same pattern. 3) List all occurrences with file:line and risk (P0/P1/P2). 4) Rate confidence you found all (1-3=guessing, 4-6=informed but unverified, 7-8=verified by reading code, 9-10=verified with exhaustive grep/AST search). 5) Propose prevention: architecture change, abstraction, type design, or coding practice that makes this bug class impossible—plus lint rule, test, type constraint, or pre-commit hook to catch escapes. 6) Validation: how will you prove each fix works and prevention is effective? 7) Prioritize by blast radius.
