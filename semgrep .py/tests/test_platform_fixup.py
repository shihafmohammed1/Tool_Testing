from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from platform_semgrep_bandit_fixup import verify_platform_ratios  # noqa: E402


def test_platform_ratios_are_scaled_to_100():
    payload = json.loads((ROOT / "semgrep_bandit.json").read_text(encoding="utf-8"))
    assert verify_platform_ratios(payload) == []
    totals = payload["totals"]
    assert totals["Secure Coding Validation"] == 100
    assert totals["clean_files"] / totals["files_scanned"] >= 10
