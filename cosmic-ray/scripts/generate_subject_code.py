#!/usr/bin/env python3
"""Generate ~50k LOC subject volume for this tool folder."""
from __future__ import annotations

import sys
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = TOOL_ROOT.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from codegen.cli import main  # noqa: E402

PROFILE = (TOOL_ROOT / ".codegen-profile").read_text(encoding="utf-8").strip()

if __name__ == "__main__":
    main(["--profile", PROFILE, "--tool-root", str(TOOL_ROOT), *sys.argv[1:]])
