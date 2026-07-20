"""Calculate QA Resource Allocation scores from parsed tool outputs."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


def normalize_path(path: str) -> str:
    return path.replace("\\", "/")


PRIORITY_THRESHOLDS = [
    (0.75, "Critical QA Priority"),
    (0.50, "High QA Priority"),
    (0.25, "Medium QA Priority"),
    (0.00, "Low QA Priority"),
]


def priority_label(score: float) -> str:
    for threshold, label in PRIORITY_THRESHOLDS:
        if score >= threshold:
            return label
    return "Low QA Priority"


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def file_level_affected_tests(file_path: str, file_to_tests: dict[str, list[str]]) -> list[str]:
    tests = set(file_to_tests.get(file_path, []))
    for mapped_file, mapped_tests in file_to_tests.items():
        if mapped_file == file_path:
            continue
        if mapped_file.endswith(file_path) or file_path.endswith(mapped_file):
            tests.update(mapped_tests)
    return sorted(tests)


def calculate_rows(root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    report_dir = root / "reports"
    complexity = load_json(report_dir / "complexity_parsed.json")
    coverage = load_json(report_dir / "coverage_parsed.json")
    testmon = load_json(report_dir / "testmon_parsed.json")

    records = complexity.get("records", [])
    coverage_by_file = {r["source_file"]: r for r in coverage.get("records", [])}
    dependency = testmon.get("dependency_data", {})
    file_to_tests: dict[str, list[str]] = dependency.get("file_to_tests", {})
    test_durations: dict[str, float] = {}
    for run in testmon.get("runs", {}).values():
        for test_id, duration in run.get("test_durations", {}).items():
            test_durations[test_id] = max(test_durations.get(test_id, 0.0), duration)
    db_durations = dependency.get("metadata", {}).get("test_durations", {})
    for test_id, duration in db_durations.items():
        test_durations[normalize_path(test_id)] = max(test_durations.get(normalize_path(test_id), 0.0), float(duration))

    total_tests = dependency.get("total_tests") or max(
        (run.get("total_collected", 0) for run in testmon.get("runs", {}).values()),
        default=0,
    )
    if not total_tests:
        total_tests = len(dependency.get("test_to_files", {}))

    max_complexity = max((int(r.get("cyclomatic_complexity", 0)) for r in records), default=1) or 1
    duration_available = bool(test_durations)
    max_duration = max(test_durations.values()) if test_durations else 0.0

    rows: list[dict[str, Any]] = []
    unmapped = 0

    for record in records:
        source_file = record["source_file"]
        affected_tests = file_level_affected_tests(source_file, file_to_tests)
        affected_count = len(affected_tests)
        cov = coverage_by_file.get(source_file)
        coverage_pct = float(cov["coverage_percentage"]) if cov else 0.0
        if coverage_pct > 1:
            coverage_pct /= 100.0
        coverage_gap = 1.0 - coverage_pct

        associated_duration = sum(test_durations.get(test_id, 0.0) for test_id in affected_tests)
        normalized_complexity = int(record.get("cyclomatic_complexity", 0)) / max_complexity
        affected_test_ratio = (affected_count / total_tests) if total_tests else 0.0
        normalized_test_cost = (associated_duration / max_duration) if max_duration else 0.0

        if duration_available and max_duration > 0:
            score = (
                0.35 * normalized_complexity
                + 0.30 * affected_test_ratio
                + 0.20 * coverage_gap
                + 0.15 * normalized_test_cost
            )
        else:
            score = (
                0.40 * normalized_complexity
                + 0.35 * affected_test_ratio
                + 0.25 * coverage_gap
            )

        derivation_status = "complete"
        if not cov:
            derivation_status = "missing_coverage"
        if total_tests and affected_count == 0:
            derivation_status = "missing_test_dependency"
        if derivation_status != "complete":
            unmapped += 1

        rows.append(
            {
                "source_file": source_file,
                "component_name": record.get("component_name", ""),
                "component_type": record.get("component_type", "function"),
                "start_line": record.get("start_line", 0),
                "end_line": record.get("end_line", 0),
                "cyclomatic_complexity": record.get("cyclomatic_complexity", 0),
                "complexity_rank": record.get("complexity_rank", ""),
                "normalized_complexity": round(normalized_complexity, 6),
                "total_tests": total_tests,
                "affected_tests": affected_count,
                "affected_test_ratio": round(affected_test_ratio, 6),
                "coverage_percentage": round(coverage_pct, 6),
                "coverage_gap": round(coverage_gap, 6),
                "associated_test_duration": round(associated_duration, 6),
                "normalized_test_cost": round(normalized_test_cost, 6),
                "qa_resource_priority_score": round(score, 6),
                "qa_priority": priority_label(score),
                "data_source": record.get("data_source", "radon/lizard"),
                "derivation_status": derivation_status,
            }
        )

    examples = {}
    for label in ["Low QA Priority", "Medium QA Priority", "High QA Priority", "Critical QA Priority"]:
        match = next((row for row in sorted(rows, key=lambda r: r["qa_resource_priority_score"], reverse=True) if row["qa_priority"] == label), None)
        if match:
            examples[label] = match

    meta = {
        "total_components": len(rows),
        "unmapped_or_partial": unmapped,
        "total_tests": total_tests,
        "max_complexity": max_complexity,
        "duration_available": duration_available,
        "dependency_files": len(file_to_tests),
        "examples": examples,
        "testmon_emits_metric": testmon.get("emits_qa_resource_allocation", False),
        "testmon_provides_dependencies": bool(file_to_tests),
    }
    return rows, meta


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    fieldnames = [
        "source_file",
        "component_name",
        "component_type",
        "start_line",
        "end_line",
        "cyclomatic_complexity",
        "complexity_rank",
        "normalized_complexity",
        "total_tests",
        "affected_tests",
        "affected_test_ratio",
        "coverage_percentage",
        "coverage_gap",
        "associated_test_duration",
        "normalized_test_cost",
        "qa_resource_priority_score",
        "qa_priority",
        "data_source",
        "derivation_status",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def assess_status(meta: dict[str, Any]) -> dict[str, str]:
    has_complexity = meta.get("total_components", 0) > 0
    has_dependencies = meta.get("testmon_provides_dependencies", False)
    has_total_tests = meta.get("total_tests", 0) > 0
    partial_count = meta.get("unmapped_or_partial", 0)
    total_components = meta.get("total_components", 1)
    has_coverage = partial_count < total_components

    direct = "PASS" if meta.get("testmon_emits_metric") else "FAIL"

    testmon_only = "FAIL"
    if has_dependencies and has_total_tests:
        testmon_only = "PARTIAL PASS"

    combined = "FAIL"
    if has_complexity and has_dependencies and has_total_tests and has_coverage:
        combined = "PARTIAL PASS"
        if meta.get("duration_available") and meta.get("dependency_files", 0) > 0:
            mapped_ratio = 1 - (partial_count / max(total_components, 1))
            if mapped_ratio > 0.8:
                combined = "PASS"
    elif has_complexity and has_dependencies and has_total_tests:
        combined = "PARTIAL PASS"

    overall = combined
    issue = "none"
    if not meta.get("testmon_emits_metric"):
        if combined == "PASS":
            issue = "none"
        elif combined == "PARTIAL PASS":
            issue = "integration"
        else:
            issue = "tool limitation"

    return {
        "direct_support": direct,
        "testmon_only": testmon_only,
        "combined": combined,
        "overall": overall,
        "primary_issue": issue,
    }


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    report_dir = root / "reports"
    rows, meta = calculate_rows(root)
    write_csv(rows, report_dir / "qa_resource_allocation.csv")
    status = assess_status(meta)
    payload = {"meta": meta, "status": status, "row_count": len(rows)}
    (report_dir / "qa_priority_meta.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {report_dir / 'qa_resource_allocation.csv'} ({len(rows)} rows)")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
