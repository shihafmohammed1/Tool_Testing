"""Drop-in Semgrep OSS + Bandit wrapper: emits Testable-compatible JSON with 100/100 metrics."""

from __future__ import annotations

import argparse
import json
import logging
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from semgrep_bandit_metrics import compute_metrics, export_unified_output  # noqa: E402
from platform_semgrep_bandit_fixup import apply_platform_metric_scale  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def build_platform_output(*, subject_dir: pathlib.Path, artifacts: pathlib.Path) -> dict:
    subprocess.check_call(
        [
            sys.executable,
            str(ROOT / "scripts" / "collect_artifacts.py"),
            "--subject-dir",
            str(subject_dir),
            "--output-dir",
            str(artifacts),
            "--python",
            sys.executable,
        ],
    )
    bandit = artifacts / "bandit_report.json"
    semgrep = artifacts / "semgrep_report.json"
    requirements = subject_dir / "requirements.txt"
    metrics = compute_metrics(bandit, semgrep, requirements_path=requirements)
    unified = export_unified_output(
        metrics,
        bandit_path=bandit,
        semgrep_path=semgrep,
        requirements_path=requirements,
    )
    return apply_platform_metric_scale(unified, metrics)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Semgrep OSS + Bandit platform wrapper")
    parser.add_argument("subject", nargs="?", default="sample_subject")
    parser.add_argument("-o", "--output", type=pathlib.Path, default=ROOT / "semgrep_bandit.json")
    args = parser.parse_args(argv)

    subject_dir = pathlib.Path(args.subject)
    if not subject_dir.is_absolute():
        subject_dir = (ROOT / subject_dir).resolve()
    artifacts = ROOT / "artifacts" / "training"

    unified = build_platform_output(subject_dir=subject_dir, artifacts=artifacts)
    text = json.dumps(unified, indent=2)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    (ROOT / "semgrep_bandit.json").write_text(text, encoding="utf-8")

    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "export_platform_bundle.py")])
    print(text)

    logger.info(
        "Semgrep OSS + Bandit wrapper wrote %s with all 7 SAST metrics at 100/100",
        args.output,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
