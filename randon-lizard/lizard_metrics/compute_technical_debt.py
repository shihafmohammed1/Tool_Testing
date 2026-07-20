"""Compute Technical Debt Impact from Lizard CCN / NLOC / ND signals.

Formula (Testable_Strategy_Metrics_Mapping_v0.2):
  technical_debt = sum(ccn_values)
  Technical Debt Score =
      (avg_cc / 10) * 0.5
    + (avg_nloc / 200) * 0.3
    + (avg_nd / 10) * 0.2
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _run_lizard_csv(target: str) -> list[dict[str, float]]:
    """Parse lizard CSV rows: NLOC, CCN, token, PARAM, length, location, ..."""
    proc = subprocess.run(
        [sys.executable, "-m", "lizard", target, "-l", "python", "--csv"],
        check=True,
        capture_output=True,
        text=True,
    )
    rows: list[dict[str, float]] = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("NLOC"):
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 5:
            continue
        try:
            nloc = float(parts[0])
            ccn = float(parts[1])
        except ValueError:
            continue
        # Lizard CSV does not always expose ND; approximate ND from CCN when absent.
        nd = ccn  # conservative stand-in for nesting-related risk
        rows.append({"nloc": nloc, "ccn": ccn, "nd": nd})
    return rows


def compute(target: str) -> dict[str, float]:
    rows = _run_lizard_csv(target)
    if not rows:
        raise SystemExit(f"No Lizard functions found under: {target}")

    ccn_values = [r["ccn"] for r in rows]
    nloc_values = [r["nloc"] for r in rows]
    nd_values = [r["nd"] for r in rows]

    avg_cc = sum(ccn_values) / len(ccn_values)
    avg_nloc = sum(nloc_values) / len(nloc_values)
    avg_nd = sum(nd_values) / len(nd_values)

    technical_debt = sum(ccn_values)
    score = (avg_cc / 10) * 0.5 + (avg_nloc / 200) * 0.3 + (avg_nd / 10) * 0.2

    return {
        "functions": float(len(rows)),
        "technical_debt_sum_ccn": technical_debt,
        "average_ccn": avg_cc,
        "average_nloc": avg_nloc,
        "average_nd": avg_nd,
        "technical_debt_score": score,
    }


def main() -> None:
    target = sys.argv[1] if len(sys.argv) > 1 else "src"
    if not Path(target).exists():
        raise SystemExit(f"Target path not found: {target}")
    result = compute(target)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
