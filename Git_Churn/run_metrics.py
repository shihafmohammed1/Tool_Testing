"""CLI entry point for Testable PyDriller metrics."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.excel_loader import load_metric_definitions
from src.metrics_engine import compute_all_metrics
from src.repo_loader import load_repo_snapshot
from src.report.markdown import write_markdown_report
from src.scoring import parse_date


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract Testable strategy metrics from a Git repository using PyDriller."
    )
    parser.add_argument("--repo", required=True, help="Path to the target Git repository.")
    parser.add_argument(
        "--excel",
        default=r"c:\Users\SAKTHI SUDHARSHAN\Downloads\Testable_Strategy_Metrics_Mapping_v0.2 (1).xlsx",
        help="Path to Testable Strategy Metrics Mapping Excel file.",
    )
    parser.add_argument("--since", help="Start date (YYYY-MM-DD). Default: 30 days ago.")
    parser.add_argument("--to", help="End date (YYYY-MM-DD). Default: today.")
    parser.add_argument("--output-dir", default="reports", help="Directory for JSON/Markdown reports.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 if any metric score is below 100.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    now = datetime.now(timezone.utc)
    since = parse_date(args.since, now - timedelta(days=30))
    to = parse_date(args.to, now)

    config = load_metric_definitions(excel_path=args.excel)
    defaults = config["defaults"]

    snapshot = load_repo_snapshot(
        repo_path=args.repo,
        since=since,
        to=to,
        test_path_patterns=defaults.get("test_path_patterns", ["test", "tests"]),
        test_file_suffixes=defaults.get("test_file_suffixes", ["_test.py"]),
    )

    metrics = compute_all_metrics(snapshot, defaults)
    report = {
        "repository": snapshot.repo_path,
        "analysis_window": {
            "since": since.date().isoformat(),
            "to": to.date().isoformat(),
            "total_commits": snapshot.total_commits,
        },
        "excel_source": config.get("excel_source"),
        "yaml_source": config.get("yaml_source"),
        "metric_definitions": config["metrics"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "metrics": metrics,
    }

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = output_dir / f"pydriller_metrics_{timestamp}.json"
    md_path = output_dir / f"pydriller_metrics_{timestamp}.md"

    json_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    write_markdown_report(report, md_path)

    print(f"Repository analyzed: {snapshot.repo_path}")
    print(f"Commits in window: {snapshot.total_commits}")
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {md_path}")
    print("\nMetric Status:")
    all_pass = True
    for item in metrics:
        score = item.get("score", 0)
        if score is None or score < 100 or item["status"] != "PASS":
            all_pass = False
        print(f"  [{item['status']}] {item['technique']} / {item['metric']} (score={score})")

    if args.strict and not all_pass:
        print("\nSTRICT GATE FAILED: One or more metrics are below 100/100.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
