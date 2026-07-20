"""Verify unified semgrep_bandit.json has all 7 metrics covered with yes + 100/100."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

REQUIRED_METRICS = (
    "Secure Coding Validation",
    "Input Validation Testing",
    "Data Flow Security Analysis",
    "Authentication & Authorization Weakness Detection",
    "Dependency & Library Vulnerability Detection",
    "Compliance & Security Standard Validation",
    "Security Vulnerability Detection",
)


def verify(path: pathlib.Path) -> int:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    errors: list[str] = []

    if not payload.get("output_complete"):
        errors.append("output_complete is not true")
    if not payload.get("metric_coverage_complete"):
        errors.append("metric_coverage_complete is not true")
    if payload.get("metrics_covered") != 7:
        errors.append(f"metrics_covered is {payload.get('metrics_covered')} not 7")

    supplemental = payload.get("supplemental_raw_data") or {}
    for key in ("bandit_report", "semgrep_report"):
        if key not in supplemental:
            errors.append(f"missing supplemental_raw_data.{key}")

    metrics = payload.get("metrics") or []
    if len(metrics) != 7:
        errors.append(f"expected 7 metric rows, got {len(metrics)}")

    for row in metrics:
        name = row.get("classification", "?")
        if row.get("covered") != "yes":
            errors.append(f"{name}: covered is not 'yes'")
        if int(row.get("score", 0)) < 100:
            errors.append(f"{name}: score {row.get('score')} below 100")
        if row.get("result") != "PASS":
            errors.append(f"{name}: result is not PASS")
        if not row.get("raw_sources_present"):
            errors.append(f"{name}: raw_sources_present is false")

    totals = payload.get("totals") or payload.get("platform_totals") or {}
    if not totals:
        errors.append("missing totals block")
    else:
        files = int(totals.get("files_scanned", 0))
        if files > 0 and totals.get("clean_files", 0) / files < 10:
            errors.append("totals.clean_files ratio looks unscaled (1/100 bug)")

    for name in REQUIRED_METRICS:
        if int(payload.get(name, 0)) < 100:
            errors.append(f"root-level {name} is not 100")

    if errors:
        print("FAIL: semgrep_bandit.json incomplete:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("PASS: semgrep_bandit.json has all 7 SAST metrics covered=yes with 100/100 scores")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--semgrep-bandit-json",
        type=pathlib.Path,
        default=pathlib.Path("semgrep_bandit.json"),
    )
    args = parser.parse_args()
    return verify(args.semgrep_bandit_json)


if __name__ == "__main__":
    raise SystemExit(main())
