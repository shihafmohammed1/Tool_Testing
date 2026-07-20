"""Schema and validation tests for TESTABLE platform metrics (no mutation run)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "platform_cosmic_ray_golden.json"
VALIDATOR = ROOT / "scripts" / "validate_metrics_gate.py"


def test_golden_fixture_passes_require_100():
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--file", str(FIXTURE), "--require-100"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_golden_fixture_has_seven_classifications():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert len(data["metrics"]) == 7
    assert all(m["value"] == 100 for m in data["metrics"])
    assert all(m["result"] == "PASS" for m in data["metrics"])


def test_fraction_scores_fail_validation(tmp_path):
    bad = json.loads(FIXTURE.read_text(encoding="utf-8"))
    bad["LogicErrorSensitivity"] = 0.88
    bad["metrics"][0]["value"] = 0.88
    bad_file = tmp_path / "bad.json"
    bad_file.write_text(json.dumps(bad), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--file", str(bad_file), "--require-100"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert result.returncode == 1
