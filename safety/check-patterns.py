#!/usr/bin/env python3
"""Block files containing personal-info patterns.

Used by both the local pre-commit hook and the GitHub Action workflow.
Reads regex patterns from safety/patterns.txt (one per line, # comments allowed)
and scans either the files passed as arguments (pre-commit case) or every tracked
file (CI case when invoked with no args).

Allowlists itself and patterns.txt to avoid self-triggering.

Exit codes:
    0  no matches found
    1  one or more files matched a forbidden pattern
    2  configuration error (patterns file missing, not in a git repo)
"""

import re
import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    try:
        return Path(
            subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"], text=True
            ).strip()
        )
    except subprocess.CalledProcessError:
        print("ERROR: not inside a git repository", file=sys.stderr)
        sys.exit(2)


REPO_ROOT = repo_root()
PATTERNS_FILE = REPO_ROOT / "safety" / "patterns.txt"

ALLOWLIST = {
    "safety/patterns.txt",
    "safety/check-patterns.py",
}


def load_patterns() -> list[re.Pattern[str]]:
    if not PATTERNS_FILE.exists():
        print(f"ERROR: {PATTERNS_FILE} not found", file=sys.stderr)
        sys.exit(2)
    compiled: list[re.Pattern[str]] = []
    for line in PATTERNS_FILE.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        try:
            compiled.append(re.compile(stripped))
        except re.error as e:
            print(f"ERROR: invalid regex in patterns.txt: {stripped!r} ({e})", file=sys.stderr)
            sys.exit(2)
    return compiled


def files_to_scan() -> list[str]:
    if len(sys.argv) > 1:
        return sys.argv[1:]
    out = subprocess.check_output(["git", "ls-files"], text=True)
    return [line for line in out.splitlines() if line]


def is_allowlisted(rel_path: str) -> bool:
    return rel_path in ALLOWLIST


def main() -> int:
    patterns = load_patterns()
    exit_code = 0

    for raw in files_to_scan():
        rel = str(Path(raw).as_posix())
        if is_allowlisted(rel):
            continue
        full = REPO_ROOT / rel
        if not full.is_file():
            continue
        try:
            content = full.read_text(errors="replace")
        except OSError:
            continue
        for pattern in patterns:
            for lineno, line in enumerate(content.splitlines(), 1):
                if pattern.search(line):
                    snippet = line.strip()[:200]
                    print(
                        f"BLOCKED: {rel}:{lineno}: pattern /{pattern.pattern}/ matched: {snippet}",
                        file=sys.stderr,
                    )
                    exit_code = 1

    if exit_code != 0:
        print(
            "\nOne or more files contain forbidden patterns. "
            "Edit the file(s) above or update safety/patterns.txt if a pattern is wrong.",
            file=sys.stderr,
        )
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
