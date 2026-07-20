"""Parse Coverage.py JSON and XML reports."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class CoverageRecord:
    source_file: str
    executed_lines: list[int]
    missing_lines: list[int]
    covered_lines: int
    num_statements: int
    coverage_percentage: float
    branch_coverage: float | None


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").lstrip("./")


def parse_coverage_json(path: Path) -> list[CoverageRecord]:
    if not path.exists():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    records: list[CoverageRecord] = []
    files = raw.get("files", {})
    for file_path, meta in files.items():
        norm = normalize_path(file_path)
        if "src/" in norm:
            norm = "src/" + norm.split("src/", 1)[-1]
        summary = meta.get("summary", {})
        executed = sorted(meta.get("executed_lines", []))
        missing = sorted(meta.get("missing_lines", []))
        records.append(
            CoverageRecord(
                source_file=norm,
                executed_lines=executed,
                missing_lines=missing,
                covered_lines=int(summary.get("covered_lines", len(executed))),
                num_statements=int(summary.get("num_statements", len(executed) + len(missing))),
                coverage_percentage=float(summary.get("percent_covered", 0.0)) / 100.0
                if summary.get("percent_covered", 0) > 1
                else float(summary.get("percent_covered", 0.0)),
                branch_coverage=None,
            )
        )
    return records


def parse_coverage_xml(path: Path) -> dict[str, float | None]:
    if not path.exists():
        return {}
    root = ET.parse(path).getroot()
    branch_map: dict[str, float | None] = {}
    for package in root.findall(".//package"):
        for cls in package.findall("classes/class"):
            filename = normalize_path(cls.get("filename", ""))
            if "src/" in filename:
                filename = "src/" + filename.split("src/", 1)[-1]
            line_rate = float(cls.get("line-rate", "0") or 0)
            branch_rate = cls.get("branch-rate")
            branch_map[filename] = float(branch_rate) if branch_rate not in (None, "") else None
            branch_map.setdefault(filename + ":line_rate", line_rate)
    return branch_map


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    report_dir = root / "reports"
    records = parse_coverage_json(report_dir / "coverage.json")
    branch_data = parse_coverage_xml(report_dir / "coverage.xml")
    payload_records: list[dict[str, Any]] = []
    for record in records:
        item = asdict(record)
        if record.coverage_percentage > 1:
            item["coverage_percentage"] = record.coverage_percentage / 100.0
        item["branch_coverage"] = branch_data.get(record.source_file)
        payload_records.append(item)

    out = report_dir / "coverage_parsed.json"
    out.write_text(json.dumps({"records": payload_records}, indent=2), encoding="utf-8")
    print(f"Wrote {out} ({len(payload_records)} files)")


if __name__ == "__main__":
    main()
