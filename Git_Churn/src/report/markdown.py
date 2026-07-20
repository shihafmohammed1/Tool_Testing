"""Markdown report writer for Testable metrics output."""

from __future__ import annotations

import json
from pathlib import Path


def write_markdown_report(report: dict, output_path: Path) -> None:
    lines = [
        "# Testable PyDriller Metrics Report",
        "",
        f"- **Repository:** `{report['repository']}`",
        f"- **Window:** {report['analysis_window']['since']} → {report['analysis_window']['to']}",
        f"- **Excel Source:** {report.get('excel_source', 'N/A')}",
        f"- **Generated:** {report['generated_at']}",
        "",
        "## Metrics Summary",
        "",
        "| Technique | Classification | Metric | Score | Status |",
        "|-----------|----------------|--------|-------|--------|",
    ]

    for item in report["metrics"]:
        score = item.get("score", "N/A")
        lines.append(
            f"| {item['technique']} | {item['classification']} | {item['metric']} | {score} | {item['status']} |"
        )

    lines.extend(["", "## Details", ""])
    for item in report["metrics"]:
        lines.append(f"### {item['metric']} (`{item['metric_id']}`)")
        lines.append(f"- **Formula:** {item['details'].get('formula', 'N/A')}")
        lines.append(f"- **Threshold:** {item['details'].get('threshold', 'N/A')}")
        lines.append(f"- **Value:** `{json.dumps(item['value'], default=str)}`")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
