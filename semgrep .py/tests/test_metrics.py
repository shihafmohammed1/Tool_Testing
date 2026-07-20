from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from semgrep_bandit_metrics import compute_metrics, compute_normalized_scores  # noqa: E402


def test_training_subject_scores_100():
    bandit = ROOT / "artifacts" / "training" / "bandit_report.json"
    semgrep = ROOT / "artifacts" / "training" / "semgrep_report.json"
    requirements = ROOT / "sample_subject" / "requirements.txt"
    metrics = compute_metrics(bandit, semgrep, requirements_path=requirements)
    scores = compute_normalized_scores(metrics)
    assert metrics.total_findings == 0
    assert len(scores) == 7
    assert all(score == 100.0 for score in scores.values())


def test_platform_json_has_root_scores():
    payload = json.loads((ROOT / "semgrep_bandit.json").read_text(encoding="utf-8"))
    assert payload["metric_coverage_complete"] is True
    assert payload["metrics_covered"] == 7
    assert payload["Secure Coding Validation"] == 100
    assert payload["Security Vulnerability Detection"] == 100
