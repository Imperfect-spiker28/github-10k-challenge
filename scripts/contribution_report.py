#!/usr/bin/env python3
"""Fetch authoritative GitHub contribution calendar count via GraphQL."""

import json
import subprocess
import sys


QUERY = """
query {
  viewer {
    login
    contributionsCollection {
      contributionCalendar {
        totalContributions
      }
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
    }
  }
}
""".strip()


def main() -> int:
    cmd = ["gh", "api", "graphql", "-f", f"query={QUERY}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error querying GitHub GraphQL: {result.stderr}", file=sys.stderr)
        return 1

    data = json.loads(result.stdout)
    viewer = data.get("data", {}).get("viewer", {})
    cc = viewer.get("contributionsCollection", {})
    cal_total = cc.get("contributionCalendar", {}).get("totalContributions", 0)

    print(f"GitHub User: {viewer.get('login')}")
    print(f"Calendar Total Contributions: {cal_total}")
    print(f"  - Commits:  {cc.get('totalCommitContributions', 0)}")
    print(f"  - PRs:      {cc.get('totalPullRequestContributions', 0)}")
    print(f"  - Reviews:  {cc.get('totalPullRequestReviewContributions', 0)}")
    print(f"  - Issues:   {cc.get('totalIssueContributions', 0)}")
    print(f"Remaining to 10,000 stretch target: {max(0, 10000 - cal_total)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
