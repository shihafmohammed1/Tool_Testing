"""Parse Testmon console output and dependency database."""

from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class TestmonRunSummary:
    run_label: str
    output_file: str
    total_collected: int = 0
    selected_count: int = 0
    deselected_count: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    selected_tests: list[str] = field(default_factory=list)
    deselected_tests: list[str] = field(default_factory=list)
    test_durations: dict[str, float] = field(default_factory=dict)
    raw_excerpt: str = ""


@dataclass
class TestmonDependencyData:
    database_path: str | None
    database_tables: list[str] = field(default_factory=list)
    test_to_files: dict[str, list[str]] = field(default_factory=dict)
    file_to_tests: dict[str, list[str]] = field(default_factory=dict)
    total_tests: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


COLLECTED_RE = re.compile(r"collected\s+(\d+)\s+items?", re.I)
DESELECTED_RE = re.compile(r"(\d+)\s+deselected", re.I)
SELECTED_RE = re.compile(r"(\d+)\s+selected", re.I)
TEST_RESULT_RE = re.compile(
    r"^(?P<path>tests[/\\][^\s]+)::(?P<name>[^\s]+)\s+(?P<status>PASSED|FAILED|SKIPPED|XPASS|XFAIL)",
    re.M,
)
DURATION_RE = re.compile(
    r"^(?P<path>tests[/\\][^\s]+)::(?P<name>[^\s]+)\s+.*?\[(?P<duration>[0-9.]+)s\]",
    re.M,
)


def normalize_path(path: str) -> str:
    return path.replace("\\", "/")


def parse_console_output(text: str, run_label: str, output_file: str) -> TestmonRunSummary:
    summary = TestmonRunSummary(run_label=run_label, output_file=output_file, raw_excerpt=text[:4000])

    collected = COLLECTED_RE.search(text)
    if collected:
        summary.total_collected = int(collected.group(1))

    deselected = DESELECTED_RE.search(text)
    if deselected:
        summary.deselected_count = int(deselected.group(1))

    selected = SELECTED_RE.search(text)
    if selected:
        summary.selected_count = int(selected.group(1))
    elif summary.total_collected and summary.deselected_count:
        summary.selected_count = summary.total_collected - summary.deselected_count
    elif summary.total_collected:
        summary.selected_count = summary.total_collected

    for match in TEST_RESULT_RE.finditer(text):
        test_id = f"{normalize_path(match.group('path'))}::{match.group('name')}"
        status = match.group("status")
        if status == "PASSED":
            summary.passed += 1
            if test_id not in summary.selected_tests:
                summary.selected_tests.append(test_id)
        elif status == "FAILED":
            summary.failed += 1
            if test_id not in summary.selected_tests:
                summary.selected_tests.append(test_id)
        elif status == "SKIPPED":
            summary.skipped += 1

    for match in DURATION_RE.finditer(text):
        test_id = f"{normalize_path(match.group('path'))}::{match.group('name')}"
        summary.test_durations[test_id] = float(match.group("duration"))

    if not summary.deselected_count and summary.total_collected and summary.selected_tests:
        executed = len(summary.selected_tests)
        if executed < summary.total_collected:
            summary.deselected_count = summary.total_collected - executed

    return summary


def find_testmon_database(root: Path) -> Path | None:
    candidates = [
        root / ".testmondata",
        root / ".testmon" / "data",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    for path in root.rglob(".testmondata"):
        return path
    return None


def parse_sqlite_dependencies(db_path: Path) -> TestmonDependencyData:
    data = TestmonDependencyData(database_path=str(db_path.resolve()))
    conn = sqlite3.connect(db_path)
    try:
        tables = [
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            ).fetchall()
        ]
        data.database_tables = tables

        if {"test_execution", "file_fp", "test_execution_file_fp"}.issubset(set(tables)):
            rows = conn.execute(
                """
                SELECT te.test_name, te.duration, ff.filename
                FROM test_execution te
                JOIN test_execution_file_fp tef ON te.id = tef.test_execution_id
                JOIN file_fp ff ON ff.id = tef.fingerprint_id
                """
            ).fetchall()
            test_to_files: dict[str, set[str]] = {}
            file_to_tests: dict[str, set[str]] = {}
            durations: dict[str, float] = {}
            for test_name, duration, filename in rows:
                norm_test = normalize_path(test_name)
                norm_file = normalize_path(filename)
                durations[norm_test] = float(duration or 0.0)
                if not norm_file.startswith("src/"):
                    continue
                test_to_files.setdefault(norm_test, set()).add(norm_file)
                file_to_tests.setdefault(norm_file, set()).add(norm_test)
            data.test_to_files = {k: sorted(v) for k, v in test_to_files.items()}
            data.file_to_tests = {k: sorted(v) for k, v in file_to_tests.items()}
            data.total_tests = len(data.test_to_files)
            data.metadata["dependency_rows"] = len(rows)
            data.metadata["test_durations"] = durations
        elif "node" in tables and "dependency" in tables:
            dep_rows = conn.execute("SELECT source_node_id, dependency_node_id FROM dependency").fetchall()
            node_files = {
                row[0]: normalize_path(row[3]) if row[3] else ""
                for row in conn.execute("SELECT id, type, name, file FROM node").fetchall()
            }
            node_tests = {
                row[0]: normalize_path(row[2])
                for row in conn.execute("SELECT id, type, name, file FROM node WHERE type='test'").fetchall()
            }
            test_to_files: dict[str, set[str]] = {}
            file_to_tests: dict[str, set[str]] = {}
            for src, dep in dep_rows:
                test_name = node_tests.get(src)
                file_name = node_files.get(dep)
                if test_name and file_name and file_name.startswith("src/"):
                    test_to_files.setdefault(test_name, set()).add(file_name)
                    file_to_tests.setdefault(file_name, set()).add(test_name)
            data.test_to_files = {k: sorted(v) for k, v in test_to_files.items()}
            data.file_to_tests = {k: sorted(v) for k, v in file_to_tests.items()}
            data.total_tests = len(data.test_to_files)
            data.metadata["dependency_rows"] = len(dep_rows)
    finally:
        conn.close()
    return data


def load_all_runs(report_dir: Path) -> dict[str, Any]:
    files = {
        "initial": "testmon_initial_run.txt",
        "unchanged": "testmon_unchanged_run.txt",
        "low_complexity": "testmon_low_complexity_change.txt",
        "high_complexity": "testmon_high_complexity_change.txt",
        "shared_module": "testmon_shared_module_change.txt",
    }
    runs = {}
    for key, filename in files.items():
        path = report_dir / filename
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        runs[key] = asdict(parse_console_output(text, key, str(path)))
    return runs


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    report_dir = root / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    db_path = find_testmon_database(root)
    dependency_data = (
        asdict(parse_sqlite_dependencies(db_path)) if db_path else {"database_path": None}
    )

    payload = {
        "runs": load_all_runs(report_dir),
        "dependency_data": dependency_data,
        "emits_qa_resource_allocation": False,
        "provides_test_impact_data": bool(dependency_data.get("file_to_tests")),
    }
    out = report_dir / "testmon_parsed.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
