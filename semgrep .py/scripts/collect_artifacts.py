"""Collect Semgrep OSS + Bandit raw artifacts from the training subject."""

from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _find_semgrep() -> str:
    scripts = pathlib.Path(sys.executable).parent / "Scripts" / "semgrep.exe"
    if scripts.exists():
        return str(scripts)
    found = shutil.which("semgrep")
    if found:
        return found
    raise FileNotFoundError("semgrep executable not found; install with: pip install semgrep")


def collect(*, subject_dir: pathlib.Path, output_dir: pathlib.Path, python_exe: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    bandit_out = output_dir / "bandit_report.json"
    semgrep_out = output_dir / "semgrep_report.json"

    subprocess.check_call(
        [
            python_exe,
            "-m",
            "pip",
            "install",
            "bandit>=1.7",
            "semgrep>=1.69",
            "-q",
        ]
    )

    subprocess.check_call(
        [
            python_exe,
            "-m",
            "bandit",
            "-r",
            str(subject_dir),
            "-f",
            "json",
            "-o",
            str(bandit_out),
            "--exit-zero",
        ]
    )

    semgrep = _find_semgrep()
    configs = [
        "auto",
        "p/python",
        "p/owasp-top-ten",
        "p/security-audit",
        "p/supply-chain",
    ]
    cmd = [semgrep, "scan", "--json", "--quiet", "-o", str(semgrep_out)]
    for cfg in configs:
        cmd.extend(["--config", cfg])
    cmd.append(str(subject_dir))

    proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if proc.returncode not in (0, 1):
        raise RuntimeError(f"semgrep failed: {proc.stderr or proc.stdout}")

    print(f"Collected SAST artifacts in {output_dir}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--subject-dir",
        type=pathlib.Path,
        default=ROOT / "sample_subject",
    )
    parser.add_argument(
        "--output-dir",
        type=pathlib.Path,
        default=ROOT / "artifacts" / "training",
    )
    parser.add_argument("--python", default=sys.executable)
    args = parser.parse_args()
    collect(subject_dir=args.subject_dir, output_dir=args.output_dir, python_exe=args.python)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
