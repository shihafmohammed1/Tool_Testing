#!/usr/bin/env python3
"""Validate TESTABLE Mutation Score Gate output for the testing team.

Checks cosmic-ray/0/cosmic_ray.json (and optional reports) for:
  - All 7 required classifications present
  - Each metric value/coverage at 100 (default) or meeting gate thresholds
  - Zero surviving mutants
  - Platform fields on 0-100 scale (not 0-1 fractions)

Usage:
  python scripts/validate_metrics_gate.py
  python scripts/validate_metrics_gate.py --require-100
  python scripts/validate_metrics_gate.py --file cosmic-ray/0/cosmic_ray.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_CLASSIFICATIONS = (
    "Fault Detection Capability",
    "Test Coverage Quality Validation",
    "Test Case Improvement Identification",
    "Edge Case Detection",
    "Regression Testing Validation",
    "Code Logic Validation",
    "Test Suite Effectiveness Evaluation",
)

PLATFORM_SCORE_KEYS = (
    "LogicErrorSensitivity",
    "TestRigorAssessment",
    "WeakSpotLocalization",
    "BoundaryMutantAnalysis",
    "ChangeResilienceTesting",
    "SemanticIntegrityCheck",
    "MutationKillRatePercent",
)


def validate_platform_json(
    data: dict,
    *,
    require_perfect: bool,
) -> list[str]:
    errors: list[str] = []

    if data.get("exit") != 0:
        errors.append(f"exit must be 0, got {data.get('exit')!r}")
    if data.get("dump_ok") is not True:
        errors.append("dump_ok must be true")

    survived = data.get("survivedMutants", data.get("survived_mutants"))
    if survived != 0:
        errors.append(f"survivedMutants must be 0, got {survived!r}")

    for key in PLATFORM_SCORE_KEYS:
        if key not in data:
            errors.append(f"missing platform score key: {key}")
            continue
        value = data[key]
        if not isinstance(value, (int, float)):
            errors.append(f"{key} must be numeric, got {type(value).__name__}")
            continue
        if value <= 1.0 and key != "WeakSpotLocalization":
            errors.append(
                f"{key}={value} looks like a 0-1 fraction; TESTABLE expects 0-100 scale"
            )
        min_score = 100 if require_perfect else 70
        if key == "BoundaryMutantAnalysis":
            min_score = 100 if require_perfect else 80
        if value < min_score:
            errors.append(f"{key}={value} below required minimum {min_score}")

    metrics = data.get("metrics")
    if not isinstance(metrics, list):
        errors.append("metrics array missing from platform JSON")
        return errors

    by_name = {m.get("classification"): m for m in metrics if isinstance(m, dict)}
    for name in REQUIRED_CLASSIFICATIONS:
        if name not in by_name:
            errors.append(f"missing classification in metrics[]: {name}")
            continue
        metric = by_name[name]
        value = metric.get("value")
        coverage = metric.get("coverage")
        result = metric.get("result")
        if result != "PASS":
            errors.append(f"{name}: result must be PASS, got {result!r}")
        min_value = 100 if require_perfect else 70
        if name == "Edge Case Detection":
            min_value = 100 if require_perfect else 80
        if not isinstance(value, (int, float)) or value < min_value:
            errors.append(f"{name}: value={value!r} below {min_value}")
        if not isinstance(coverage, (int, float)) or coverage < min_value:
            errors.append(f"{name}: coverage={coverage!r} below {min_value}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--file",
        default="cosmic-ray/0/cosmic_ray.json",
        help="Path to TESTABLE platform cosmic_ray.json",
    )
    parser.add_argument(
        "--require-100",
        action="store_true",
        help="Require every metric at 100/100 (testing team standard)",
    )
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"FAIL: platform file not found: {path}", file=sys.stderr)
        print("Run: python scripts/export_testable_cosmic_ray.py", file=sys.stderr)
        return 2

    data = json.loads(path.read_text(encoding="utf-8"))
    errors = validate_platform_json(data, require_perfect=args.require_100)

    if errors:
        print("METRICS GATE VALIDATION: FAIL")
        for err in errors:
            print(f"  - {err}")
        return 1

    mode = "100/100" if args.require_100 else "gate thresholds"
    print(f"METRICS GATE VALIDATION: PASS ({mode})")
    print(f"  File: {path}")
    print(f"  Mutation Kill Rate: {data.get('MutationKillRatePercent')}%")
    print(f"  Survived mutants: {data.get('survivedMutants', 0)}")
    print(f"  Classifications: {len(REQUIRED_CLASSIFICATIONS)}/7 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
