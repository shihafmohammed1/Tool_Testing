#!/usr/bin/env python3
"""Report subject_volume LOC for this tool folder."""
from __future__ import annotations

import sys
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = TOOL_ROOT.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from codegen.count_loc import report_tool  # noqa: E402

PROFILE = (TOOL_ROOT / ".codegen-profile").read_text(encoding="utf-8").strip()

if __name__ == "__main__":
    row = report_tool(PROFILE)
    print(f"Profile:   {row['profile']}")
    print(f"Folder:    {row['folder']}")
    print(f"Volume:    {row['volume_lines']:,} lines ({row['volume_files']} files)")
    print(f"Total:     {row['total_lines']:,} lines")
    print(f"Target 50k: {'YES' if row['target_met'] else 'no'}")
