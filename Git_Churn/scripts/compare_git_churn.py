"""Compare Testable git_churn.json raw output with our tool snapshot."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.file_filters import is_production_file, is_test_path
from src.metrics_engine import compute_all_metrics
from src.repo_loader import load_repo_snapshot


def short_name(path: str) -> str:
    return path.replace("\\", "/").split("/")[-1]


def main() -> int:
    raw_path = Path(r"c:\Users\SAKTHI SUDHARSHAN\Downloads\git_churn.json")
    raw = json.loads(raw_path.read_text(encoding="utf-8"))

    since = datetime(2020, 1, 1, tzinfo=timezone.utc)
    to = datetime.now(timezone.utc)
    snap = load_repo_snapshot(str(ROOT), since, to, ["test", "tests"], ["_test.py"])
    metrics = compute_all_metrics(snap, {"time_window_days": 30, "high_churn_threshold_pct": 30, "stale_churn_threshold_pct": 20})

    tool_churn = {path: stats.churn for path, stats in snap.file_stats.items()}
    raw_by_short = {short_name(k): v for k, v in raw["files"].items()}
    tool_by_short = {short_name(k): v for k, v in tool_churn.items()}

    tool_prod = {p for p in snap.prod_files_changed if is_production_file(p)}
    tool_test = {p for p in snap.test_files_changed if is_test_path(p)}
    tool_total = sum(s.churn for s in snap.file_stats.values())

    print("=== AGGREGATE: git_churn.json vs TOOL ===")
    rows = [
        ("commits", raw["commits"], snap.total_commits),
        ("lines_total", raw["lines_total"], tool_total),
        ("test_files_changed", raw["test_files_changed"], len(tool_test)),
        ("prod_files_changed", raw["prod_files_changed"], len(tool_prod)),
        ("side_effect_scope", raw["side_effect_scope"], len(snap.co_change_pairs)),
        ("test_lines", raw["test_lines"], sum(tool_churn.get(p, 0) for p in tool_test)),
        ("prod_lines", raw["prod_lines"], sum(tool_churn.get(p, 0) for p in tool_prod)),
    ]
    for name, raw_val, tool_val in rows:
        match = "MATCH" if raw_val == tool_val else "DIFF"
        print(f"  {name:22} raw={raw_val:5}  tool={tool_val:5}  [{match}]")

    mismatches = []
    for key in sorted(set(raw_by_short) | set(tool_by_short)):
        if raw_by_short.get(key) != tool_by_short.get(key):
            mismatches.append((key, raw_by_short.get(key), tool_by_short.get(key)))

    print(f"\n=== PER-FILE CHURN: {len(mismatches)} mismatches / {len(set(raw_by_short)|set(tool_by_short))} files ===")
    for key, raw_val, tool_val in mismatches[:20]:
        print(f"  {key:30} raw={raw_val}  tool={tool_val}")

    print("\n=== METRICS DERIVED FROM RAW DATA (tool output) ===")
    for m in metrics:
        print(f"  [{m['status']}] {m['classification']:40} score={m['score']}")

    print("\n=== CAN git_churn.json ALONE PRODUCE THESE METRICS? ===")
    coverage = {
        "Audit Trail Verification": "commits + author/hash/date (NOT in git_churn.json — needs commit objects)",
        "Code Churn Score": "files{} per-file churn — YES present",
        "Impact-Driven Verification": "files{} + test_files_changed — PARTIAL (needs regression mapping)",
        "Fault Probability Modeling": "files{} + commits — PARTIAL (needs commit_count per file)",
        "Validation Suite Updates": "test_files_changed + prod_files_changed — YES present",
        "Side Effect Mapping": "side_effect_scope — YES present (124 co-change pairs)",
    }
    for metric, note in coverage.items():
        print(f"  {metric}: {note}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
