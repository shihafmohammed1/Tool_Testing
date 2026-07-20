#!/usr/bin/env python3
"""Restore source tree after cosmic-ray (mutations can leave files on disk)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "testable_demo"


def main() -> int:
    if not SOURCE.exists():
        print(f"Nothing to restore: {SOURCE}", file=sys.stderr)
        return 1

    result = subprocess.run(
        ["git", "checkout", "--", "src/testable_demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return result.returncode

    print("Restored src/testable_demo from git HEAD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
