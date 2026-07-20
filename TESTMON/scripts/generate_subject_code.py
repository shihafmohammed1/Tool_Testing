#!/usr/bin/env python3
"""Delegate to TESTMON's existing generate_codebase.py (commerce platform ~50k LOC)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = TOOL_ROOT / "scripts" / "generate_codebase.py"

if __name__ == "__main__":
    cmd = [sys.executable, str(SCRIPT), *sys.argv[1:]]
    if "--target-lines" not in sys.argv:
        cmd.extend(["--target-lines", "50000"])
    raise SystemExit(subprocess.call(cmd, cwd=TOOL_ROOT))
