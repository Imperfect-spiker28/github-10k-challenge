#!/usr/bin/env python3
"""Audit all GitHub repositories for Imperfect-spiker28 via GitHub CLI."""

import json
import subprocess
import sys


def main() -> int:
    cmd = [
        "gh",
        "repo",
        "list",
        "Imperfect-spiker28",
        "--limit",
        "100",
        "--json",
        "name,visibility,isArchived,defaultBranchRef,pushedAt,primaryLanguage,description",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running gh CLI: {result.stderr}", file=sys.stderr)
        return 1

    repos = json.loads(result.stdout)
    print(f"Total repositories audited: {len(repos)}\n")
    for r in repos:
        branch = (r.get("defaultBranchRef") or {}).get("name", "unknown")
        lang = (r.get("primaryLanguage") or {}).get("name", "N/A")
        archived = " [ARCHIVED]" if r.get("isArchived") else ""
        print(
            f"- {r['name']} ({r['visibility']}, branch={branch}, lang={lang}, pushed={r['pushedAt']}){archived}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
