"""Verify dashboard and metrics JSON report 100/100."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys


def verify(metrics_json: pathlib.Path, dashboard_json: pathlib.Path) -> int:
    metrics = json.loads(metrics_json.read_text(encoding="utf-8-sig"))
    dashboard = json.loads(dashboard_json.read_text(encoding="utf-8-sig"))
    errors: list[str] = []

    scores = metrics.get("normalized_scores") or {}
    if len(scores) != 7:
        errors.append(f"expected 7 normalized scores, got {len(scores)}")
    for name, score in scores.items():
        if float(score) < 100.0:
            errors.append(f"{name}: score {score} below 100")

    if not dashboard.get("metric_coverage_complete"):
        errors.append("dashboard metric_coverage_complete is false")
    if not dashboard.get("all_scores_100"):
        errors.append("dashboard all_scores_100 is false")

    if errors:
        print("FAIL:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("PASS: all metrics are 100/100")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metrics-json", type=pathlib.Path, default=pathlib.Path("semgrep_bandit_metrics.json"))
    parser.add_argument("--dashboard-json", type=pathlib.Path, default=pathlib.Path("dashboard_metrics.json"))
    args = parser.parse_args()
    return verify(args.metrics_json, args.dashboard_json)


if __name__ == "__main__":
    raise SystemExit(main())
