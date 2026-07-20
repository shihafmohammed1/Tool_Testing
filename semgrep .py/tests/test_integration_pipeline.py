from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_trigger_pipeline_produces_passing_json():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "semgrep_bandit_trigger.py"), "--skip-verify"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout

    payload = json.loads((ROOT / "semgrep_bandit.json").read_text(encoding="utf-8"))
    assert payload["metrics_covered"] == 7
    assert all(row["score"] == 100 for row in payload["metrics"])

    verify = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "verify_semgrep_bandit_json.py")],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert verify.returncode == 0
    assert "PASS" in verify.stdout
