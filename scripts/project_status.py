#!/usr/bin/env python3
"""Summarize local Git author identity and repository status."""

import subprocess


def run(cmd: list[str]) -> str:
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout.strip() if res.returncode == 0 else f"ERR: {res.stderr.strip()}"


def main() -> int:
    print("Local Git Identity:")
    print(f"  user.name : {run(['git', 'config', '--global', 'user.name'])}")
    print(f"  user.email: {run(['git', 'config', '--global', 'user.email'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
