"""Parse Radon and Lizard cyclomatic complexity reports."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class ComplexityRecord:
    source_file: str
    component_name: str
    component_type: str
    start_line: int
    end_line: int
    cyclomatic_complexity: int
    complexity_rank: str
    lines_of_code: int
    function_length: int
    parameter_count: int | None
    data_source: str


RANK_MAP = [
    (1, "A"),
    (6, "B"),
    (11, "C"),
    (21, "D"),
    (31, "E"),
    (51, "F"),
]


def rank_from_cc(cc: int) -> str:
    result = "F"
    for threshold, rank in RANK_MAP:
        if cc < threshold:
            return result
        result = rank
    return result


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").lstrip("./")


def parse_radon_json(path: Path) -> list[ComplexityRecord]:
    if not path.exists():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    records: list[ComplexityRecord] = []
    for file_path, items in raw.items():
        norm_file = normalize_path(file_path)
        if not norm_file.startswith("src/"):
            norm_file = f"src/{norm_file.split('src/', 1)[-1]}" if "src/" in norm_file else norm_file
        for item in items:
            records.append(
                ComplexityRecord(
                    source_file=norm_file,
                    component_name=item.get("name", ""),
                    component_type=item.get("type", "function"),
                    start_line=int(item.get("lineno", 0)),
                    end_line=int(item.get("endline", item.get("lineno", 0))),
                    cyclomatic_complexity=int(item.get("complexity", 0)),
                    complexity_rank=item.get("rank", rank_from_cc(int(item.get("complexity", 0)))),
                    lines_of_code=int(item.get("endline", 0) - item.get("lineno", 0) + 1),
                    function_length=int(item.get("endline", 0) - item.get("lineno", 0) + 1),
                    parameter_count=None,
                    data_source="radon",
                )
            )
    return records


def parse_lizard_xml(path: Path) -> list[ComplexityRecord]:
    if not path.exists():
        return []
    root = ET.parse(path).getroot()
    records: list[ComplexityRecord] = []
    for measure in root.findall("measure"):
        if measure.get("type") != "Function":
            continue
        for item in measure.findall("item"):
            raw_name = item.get("name", "")
            file_path = ""
            component_name = raw_name
            start_line = 0
            if " at " in raw_name:
                component_name, location = raw_name.rsplit(" at ", 1)
                if ":" in location:
                    file_path, line_str = location.rsplit(":", 1)
                    start_line = int(line_str)
                else:
                    file_path = location
            file_path = normalize_path(file_path)
            if "src/" in file_path:
                file_path = "src/" + file_path.split("src/", 1)[-1]
            values = [int(v.text or "0") for v in item.findall("value")]
            cc = values[2] if len(values) >= 3 else (values[1] if len(values) >= 2 else 0)
            ncss = values[1] if len(values) >= 2 else 0
            component_name = component_name.split("(")[0].strip()
            records.append(
                ComplexityRecord(
                    source_file=file_path,
                    component_name=component_name,
                    component_type="function",
                    start_line=start_line,
                    end_line=start_line + max(ncss, 1) - 1,
                    cyclomatic_complexity=cc,
                    complexity_rank=rank_from_cc(cc),
                    lines_of_code=ncss,
                    function_length=ncss,
                    parameter_count=None,
                    data_source="lizard",
                )
            )
    return records


def merge_records(radon_records: list[ComplexityRecord], lizard_records: list[ComplexityRecord]) -> list[dict[str, Any]]:
    merged: dict[tuple[str, str, int], dict[str, Any]] = {}
    for record in radon_records:
        key = (record.source_file, record.component_name, record.start_line)
        merged[key] = asdict(record)
    for record in lizard_records:
        key = (record.source_file, record.component_name, record.start_line)
        existing = merged.get(key)
        payload = asdict(record)
        if existing:
            payload["parameter_count"] = record.parameter_count or existing.get("parameter_count")
            payload["data_source"] = "radon+lizard"
        merged[key] = payload
    return list(merged.values())


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    report_dir = root / "reports"
    radon_records = parse_radon_json(report_dir / "radon_cc.json")
    lizard_records = parse_lizard_xml(report_dir / "lizard.xml")
    payload = {
        "records": merge_records(radon_records, lizard_records),
        "radon_count": len(radon_records),
        "lizard_count": len(lizard_records),
    }
    out = report_dir / "complexity_parsed.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {out} ({len(payload['records'])} records)")


if __name__ == "__main__":
    main()
