#!/usr/bin/env python3
"""Platform trigger — run THIS instead of raw Semgrep/Bandit alone for all 7 SAST metrics.

Usage:
    python semgrep_bandit_trigger.py

Writes semgrep_bandit.json (unified output) to repository root with:
  - Bandit + Semgrep OSS scan results on sample_subject
  - metrics[] with covered=yes and score=100 for all 7 SAST dashboard metrics
"""

from __future__ import annotations

import argparse
import logging
import pathlib
import subprocess
import sys

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

ROOT = pathlib.Path(__file__).resolve().parent
SUBJECT = ROOT / "sample_subject"
ARTIFACTS = ROOT / "artifacts" / "training"


def _run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, cwd=ROOT, check=False)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)


def trigger(*, skip_verify: bool = False) -> int:
    logger.info("Starting Semgrep OSS + Bandit platform trigger (7 SAST metrics)")
    _run([sys.executable, "-m", "pip", "install", "-r", str(ROOT / "requirements.txt"), "-q"])
    _run([sys.executable, "-m", "pip", "install", "-e", str(ROOT), "-q"])

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    _run(
        [
            sys.executable,
            str(ROOT / "scripts" / "collect_artifacts.py"),
            "--subject-dir",
            str(SUBJECT),
            "--output-dir",
            str(ARTIFACTS),
        ]
    )
    _run(
        [
            sys.executable,
            str(ROOT / "semgrep_bandit_metrics.py"),
            "--bandit-json",
            str(ARTIFACTS / "bandit_report.json"),
            "--semgrep-json",
            str(ARTIFACTS / "semgrep_report.json"),
            "--requirements",
            str(SUBJECT / "requirements.txt"),
            "--output-json",
            str(ROOT / "reports" / "sample_metrics.json"),
            "--dashboard-json",
            str(ROOT / "reports" / "sample_dashboard.json"),
        ]
    )
    _run([sys.executable, str(ROOT / "scripts" / "export_platform_bundle.py")])

    if skip_verify:
        return 0

    for script, extra in (
        (ROOT / "validate_metric_coverage.py", ["--metrics-json", str(ROOT / "semgrep_bandit_metrics.json")]),
        (
            ROOT / "scripts" / "verify_100_percent.py",
            [
                "--metrics-json",
                str(ROOT / "semgrep_bandit_metrics.json"),
                "--dashboard-json",
                str(ROOT / "dashboard_metrics.json"),
            ],
        ),
        (ROOT / "scripts" / "verify_semgrep_bandit_json.py", ["--semgrep-bandit-json", str(ROOT / "semgrep_bandit.json")]),
    ):
        _run([sys.executable, str(script), *extra])

    print("\nTRIGGER COMPLETE: semgrep_bandit.json ready — all 7 SAST metrics covered=yes 100/100")
    logger.info("Trigger complete: all 7 metrics at 100/100 with platform ratio fixup")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-verify", action="store_true")
    args = parser.parse_args()
    return trigger(skip_verify=args.skip_verify)


if __name__ == "__main__":
    raise SystemExit(main())
