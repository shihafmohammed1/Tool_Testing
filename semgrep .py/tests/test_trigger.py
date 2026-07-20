from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_platform_module_entrypoint():
    proc = subprocess.run(
        [sys.executable, "-m", "semgrep_bandit_platform", "sample_subject", "-o", "semgrep_bandit.json"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    assert "Security Vulnerability Detection" in (ROOT / "semgrep_bandit.json").read_text(encoding="utf-8")
