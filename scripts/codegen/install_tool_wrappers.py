#!/usr/bin/env python3
"""Install per-tool generate_subject_code.py wrappers and .codegen-profile markers."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

TOOL_PROFILES: dict[str, str] = {
    "coverage .py": "coverage-py",
    "coverage + beniget .py": "coverage-beniget",
    "Pip Audit.py": "pip-audit",
    "semgrep .py": "semgrep-bandit",
    "pymcdc.py": "pymcdc",
    "randon-lizard": "randon-lizard",
    "Git_Churn": "git-churn",
    "cosmic-ray": "cosmic-ray",
    "JSCPD": "jscpd",
    "crosshair": "crosshair",
    "Beniget": "beniget",
    "Coverage.py": "coverage-py-stub",
}

GENERATE_SUBJECT = '''#!/usr/bin/env python3
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
'''

COUNT_LINES = '''#!/usr/bin/env python3
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
'''


def main() -> None:
    for folder, profile_id in TOOL_PROFILES.items():
        tool_root = REPO_ROOT / folder
        if not tool_root.is_dir():
            print(f"SKIP missing folder: {folder}")
            continue
        (tool_root / ".codegen-profile").write_text(profile_id + "\n", encoding="utf-8")
        scripts_dir = tool_root / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        (scripts_dir / "generate_subject_code.py").write_text(GENERATE_SUBJECT, encoding="utf-8")
        (scripts_dir / "count_subject_lines.py").write_text(COUNT_LINES, encoding="utf-8")
        print(f"Installed wrappers in {folder} -> {profile_id}")


if __name__ == "__main__":
    main()
