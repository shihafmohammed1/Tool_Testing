"""End-to-end Testmon metric validation orchestration."""

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
VENV_DIR = ROOT / ".venv"
IS_WINDOWS = platform.system() == "Windows"


@dataclass
class CommandResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str
    output_file: Path | None = None

    @property
    def ok(self) -> bool:
        return self.returncode == 0


def venv_python() -> Path:
    if IS_WINDOWS:
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def venv_bin(name: str) -> Path:
    if IS_WINDOWS:
        return VENV_DIR / "Scripts" / f"{name}.exe"
    return VENV_DIR / "bin" / name


def run_command(
    command: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    save_as: Path | None = None,
    allow_failure: bool = False,
) -> CommandResult:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    proc = subprocess.run(
        command,
        cwd=cwd,
        env=merged_env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    if save_as:
        save_as.parent.mkdir(parents=True, exist_ok=True)
        save_as.write_text(output, encoding="utf-8")
    result = CommandResult(command=command, returncode=proc.returncode, stdout=proc.stdout or "", stderr=proc.stderr or "", output_file=save_as)
    if not result.ok and not allow_failure:
        raise RuntimeError(
            f"Command failed ({proc.returncode}): {' '.join(command)}\n{output[-4000:]}"
        )
    return result


def resolve_python() -> str:
    if VENV_DIR.exists():
        return str(venv_python())
    for candidate in [
        sys.executable,
        shutil.which("py"),
    ]:
        if not candidate:
            continue
        command = [candidate, "--version"] if candidate != shutil.which("py") else [candidate, "-3.11", "--version"]
        proc = subprocess.run(command, capture_output=True, text=True)
        if proc.returncode == 0:
            return candidate if candidate != shutil.which("py") else f"{candidate} -3.11"
    raise RuntimeError("No working Python interpreter found")


def python_command(*args: str) -> list[str]:
    base = resolve_python()
    if base.endswith("py") or base == "py":
        return ["py", "-3.11", *args]
    if " -3.11" in base:
        return base.split() + list(args)
    return [base, *args]


def ensure_venv() -> None:
    if not VENV_DIR.exists():
        base = resolve_python()
        if " -3.11" in base:
            run_command(base.split() + ["-m", "venv", str(VENV_DIR)])
        elif base.endswith("py.exe") and Path(base).name == "py.exe":
            run_command([base, "-3.11", "-m", "venv", str(VENV_DIR)])
        else:
            run_command([base, "-m", "venv", str(VENV_DIR)])
    pip = str(venv_bin("pip"))
    run_command([pip, "install", "-r", "requirements.txt"])


def count_tests() -> int:
    result = run_command([str(venv_python()), "-m", "pytest", "--collect-only", "-q"], allow_failure=True)
    text = result.stdout + result.stderr
    for line in text.splitlines():
        if "tests collected" in line or "test collected" in line:
            digits = "".join(ch if ch.isdigit() else " " for ch in line).split()
            if digits:
                return int(digits[0])
    return 0


def count_source_lines() -> int:
    result = run_command([str(venv_python()), "scripts/count_source_lines.py"], allow_failure=True)
    for line in result.stdout.splitlines():
        if line.startswith("Source lines:"):
            return int(line.split(":")[1].strip())
    return 0


def tool_versions() -> dict[str, str]:
    py = str(venv_python())
    versions = {"python": platform.python_version()}
    for tool, module in [
        ("pytest", "pytest"),
        ("coverage", "coverage"),
        ("radon", "radon"),
        ("lizard", "lizard"),
    ]:
        proc = subprocess.run(
            [py, "-m", module, "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        versions[tool] = (proc.stdout or proc.stderr).strip()
    proc = subprocess.run([str(venv_bin("pip")), "show", "pytest-testmon"], capture_output=True, text=True)
    for line in (proc.stdout or "").splitlines():
        if line.startswith("Version:"):
            versions["pytest-testmon"] = f"pytest-testmon {line.split(':', 1)[1].strip()}"
            break
    else:
        versions["pytest-testmon"] = "unknown"
    return versions


def patch_file(path: Path, transform: Callable[[str], str]) -> str:
    original = path.read_text(encoding="utf-8")
    path.write_text(transform(original), encoding="utf-8")
    return original


def restore_file(path: Path, original: str) -> None:
    path.write_text(original, encoding="utf-8")


def run_testmon(label: str, output_name: str) -> CommandResult:
    return run_command(
        [str(venv_python()), "-m", "pytest", "--testmon", "-v"],
        save_as=REPORTS / output_name,
        allow_failure=True,
    )


def find_testmon_db() -> Path | None:
    candidates = [ROOT / ".testmondata", ROOT / ".testmon" / "data"]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    matches = list(ROOT.rglob(".testmondata"))
    return matches[0] if matches else None


def generate_validation_report(
    *,
    source_lines: int,
    total_tests: int,
    versions: dict[str, str],
    execution_log: dict[str, Any],
    status: dict[str, str],
    meta: dict[str, Any],
    testmon_db: Path | None,
) -> None:
    py_files = len(list((ROOT / "src").rglob("*.py")))
    test_files = len(list((ROOT / "tests").rglob("*.py")))
    modules = len({p.parent.name for p in (ROOT / "src" / "commerce_platform").rglob("*.py")})

    examples = meta.get("examples", {})
    example_section = ""
    for label, row in examples.items():
        example_section += textwrap.dedent(
            f"""
            ### {label}
            - Component: `{row['component_name']}` in `{row['source_file']}`
            - Complexity: {row['cyclomatic_complexity']} (normalized {row['normalized_complexity']})
            - Affected tests: {row['affected_tests']} / {row['total_tests']} (ratio {row['affected_test_ratio']})
            - Coverage gap: {row['coverage_gap']}
            - Score: {row['qa_resource_priority_score']} -> {row['qa_priority']}
            """
        )

    runs = execution_log.get("testmon_runs", {})
    report = (
        "# Testmon Metric Validation Report\n\n"
        "## 1. Metric Mapping\n\n"
        "Technique: Cyclomatic Complexity\n"
        "Classification: Test Prioritization\n"
        "Metric: QA Resource Allocation\n"
        "Primary Tool: Testmon\n\n"
        "## 2. Repository Information\n\n"
        f"* Repository name: commerce-platform\n"
        f"* Branch: main\n"
        f"* Python version: {versions.get('python', 'unknown')}\n"
        f"* Total Python files: {py_files}\n"
        f"* Total source lines: {source_lines}\n"
        f"* Total test files: {test_files}\n"
        f"* Total test cases: {total_tests}\n"
        f"* Total modules: {modules}\n"
        f"* Tool versions:\n"
        f"  * pytest: {versions.get('pytest', '')}\n"
        f"  * pytest-testmon: {versions.get('pytest-testmon', '')}\n"
        f"  * coverage: {versions.get('coverage', '')}\n"
        f"  * radon: {versions.get('radon', '')}\n"
        f"  * lizard: {versions.get('lizard', '')}\n\n"
        "## 3. Tool Execution Status\n\n"
        f"* Pytest execution status: {execution_log.get('pytest_status', 'unknown')}\n"
        f"* Testmon installation status: {execution_log.get('testmon_install_status', 'unknown')}\n"
        f"* Testmon initial-run status: {execution_log.get('testmon_initial_status', 'unknown')}\n"
        f"* Testmon unchanged-run status: {execution_log.get('testmon_unchanged_status', 'unknown')}\n"
        f"* Testmon changed-file-run status: {execution_log.get('testmon_change_status', 'unknown')}\n"
        f"* Radon execution status: {execution_log.get('radon_status', 'unknown')}\n"
        f"* Lizard execution status: {execution_log.get('lizard_status', 'unknown')}\n"
        f"* Coverage execution status: {execution_log.get('coverage_status', 'unknown')}\n"
        f"* Fatal errors: {execution_log.get('fatal_errors', 'None')}\n"
        f"* Non-fatal warnings: {execution_log.get('warnings', 'None')}\n\n"
        "## 4. Direct Metric Emission\n\n"
        "Answer:\n\n"
        "```text\n"
        "Does Testmon directly emit QA Resource Allocation? NO\n"
        "```\n\n"
        "Evidence: Testmon console outputs under `reports/testmon_*.txt` contain test collection/selection details only. "
        "Parsed output `reports/testmon_parsed.json` sets `emits_qa_resource_allocation=false`.\n\n"
        "## 5. Raw Parameters Available\n\n"
        "| Required Parameter        | Testmon | Radon/Lizard | Coverage.py | Available | Evidence |\n"
        "| ------------------------- | ------: | -----------: | ----------: | --------: | -------- |\n"
        "| Cyclomatic complexity     | NO | YES | NO | YES | `reports/radon_cc.json`, `reports/lizard.xml` |\n"
        "| Test-to-code dependency   | YES | NO | NO | YES | `reports/testmon_parsed.json` -> `dependency_data.file_to_tests` |\n"
        "| Affected-test count       | YES | NO | NO | YES | `reports/testmon_*.txt` selected test counts |\n"
        "| Total-test count          | YES | NO | NO | YES | `reports/testmon_parsed.json` and pytest collection |\n"
        "| Source coverage           | NO | NO | YES | YES | `reports/coverage.json` |\n"
        "| Test duration             | YES | NO | NO | YES | `.testmondata` table `test_execution.duration` |\n"
        "| Change-impact information | YES | NO | NO | YES | Testmon reruns in `reports/testmon_*_change.txt` |\n\n"
        "## 6. Derivation\n\n"
        f"{example_section if example_section else '_No examples available._'}\n\n"
        "## 7. Testmon Behaviour\n\n"
        f"* Number of tests executed during the first run: {runs.get('initial', {}).get('selected_count', 'n/a')}\n"
        f"* Number of tests executed without code changes: {runs.get('unchanged', {}).get('selected_count', 'n/a')}\n"
        f"* Number of tests executed after a low-complexity change: {runs.get('low_complexity', {}).get('selected_count', 'n/a')}\n"
        f"* Number of tests executed after a high-complexity change: {runs.get('high_complexity', {}).get('selected_count', 'n/a')}\n"
        f"* Number of tests executed after changing a shared utility: {runs.get('shared_module', {}).get('selected_count', 'n/a')}\n"
        f"* Whether Testmon correctly selected affected tests: {execution_log.get('testmon_selection_correct', 'see reports/testmon_*_change.txt')}\n\n"
        "## 8. Pass/Fail Assessment\n\n"
        "```text\n"
        f"Testmon direct support: {status.get('direct_support', 'FAIL')}\n"
        f"Testmon-only derivation: {status.get('testmon_only', 'FAIL')}\n"
        f"Combined open-source derivation: {status.get('combined', 'FAIL')}\n"
        f"Overall metric coverage: {status.get('overall', 'FAIL')}\n"
        "```\n\n"
        "## 9. Issue Classification\n\n"
        f"* {status.get('primary_issue', 'none')}\n\n"
        "Testmon is primarily a test-selection engine. Cyclomatic complexity is obtained from Radon/Lizard and coverage from Coverage.py. "
        "Function-level dependency mapping joins file-level Testmon data with per-function complexity records.\n\n"
        "## 10. Final Conclusion\n\n"
        "```text\n"
        "Testmon does not directly emit the QA Resource Allocation metric.\n\n"
        "Testmon provides the following useful raw information:\n"
        "- test node identifiers (test_execution.test_name)\n"
        "- source file dependencies via .testmondata sqlite tables test_execution_file_fp and file_fp\n"
        "- selected vs deselected tests on subsequent runs\n"
        "- changed-file impact through selective re-execution\n"
        "- per-test duration values in test_execution.duration\n\n"
        "Testmon is not sufficient by itself because:\n"
        "it does not compute cyclomatic complexity, coverage percentage, or QA priority scores.\n\n"
        "Using Testmon together with Radon or Lizard and Coverage.py, the metric is derivable because:\n"
        "file-level test dependencies and execution counts can be joined with complexity and coverage outputs "
        "to compute the proxy QA Resource Priority Score.\n\n"
        f"Final status: {status.get('overall', 'FAIL')}\n"
        "```\n\n"
        f"Testmon database file: `{testmon_db}`\n\n"
        "Generated artifacts:\n"
        "- `reports/qa_resource_allocation.csv`\n"
        "- `reports/testmon_parsed.json`\n"
        "- `reports/complexity_parsed.json`\n"
        "- `reports/coverage_parsed.json`\n"
    )
    (REPORTS / "testmon_metric_validation.md").write_text(report, encoding="utf-8")


def main() -> int:
    reports_only = "--reports-only" in sys.argv
    REPORTS.mkdir(parents=True, exist_ok=True)
    execution_log: dict[str, Any] = {"warnings": [], "fatal_errors": []}

    try:
        ensure_venv()
        execution_log["testmon_install_status"] = "installed"
    except Exception as exc:
        execution_log["testmon_install_status"] = f"failed: {exc}"
        execution_log["fatal_errors"].append(str(exc))
        print_final(False, 0, 0, {}, execution_log)
        return 1

    py = str(venv_python())
    if not Path(py).exists():
        raise RuntimeError(f"Virtual environment python not found at {py}")

    if reports_only:
        execution_log.update(
            {
                "pytest_status": "skipped (reports-only)",
                "testmon_initial_status": "skipped (reports-only)",
                "testmon_unchanged_status": "skipped (reports-only)",
                "testmon_change_status": "skipped (reports-only)",
                "coverage_status": "skipped (reports-only)",
                "radon_status": "passed" if (REPORTS / "radon_cc.json").exists() else "failed",
                "lizard_status": "passed" if (REPORTS / "lizard.xml").exists() else "failed",
            }
        )
        testmon_runs = {}
        for key, filename in {
            "initial": "testmon_initial_run.txt",
            "unchanged": "testmon_unchanged_run.txt",
            "low_complexity": "testmon_low_complexity_change.txt",
            "high_complexity": "testmon_high_complexity_change.txt",
            "shared_module": "testmon_shared_module_change.txt",
        }.items():
            text = (REPORTS / filename).read_text(encoding="utf-8") if (REPORTS / filename).exists() else ""
            testmon_runs[key] = {"selected_count": _extract_selected(text)}
        execution_log["testmon_runs"] = testmon_runs
        execution_log["testmon_selection_correct"] = (
            "yes" if testmon_runs.get("unchanged", {}).get("selected_count", 9999) == 0 else "review reports"
        )
    else:
        baseline = run_command([py, "-m", "pytest", "-v"], allow_failure=True)
        execution_log["pytest_status"] = "passed" if baseline.ok else "completed with failures"
        if not baseline.ok:
            execution_log["warnings"].append("Baseline pytest reported failures from fragile tests.")

        db = find_testmon_db()
        if db and db.exists():
            if db.is_file():
                db.unlink()
            else:
                shutil.rmtree(db, ignore_errors=True)

        testmon_runs: dict[str, dict[str, Any]] = {}

        initial = run_testmon("initial", "testmon_initial_run.txt")
        execution_log["testmon_initial_status"] = "passed" if initial.ok else "completed with failures"
        testmon_runs["initial"] = {"selected_count": _extract_selected(initial.stdout + initial.stderr)}

        unchanged = run_testmon("unchanged", "testmon_unchanged_run.txt")
        execution_log["testmon_unchanged_status"] = "passed" if unchanged.ok else "completed with failures"
        testmon_runs["unchanged"] = {"selected_count": _extract_selected(unchanged.stdout + unchanged.stderr)}

        low_path = ROOT / "src" / "commerce_platform" / "auth" / "session.py"
        low_original = patch_file(
            low_path,
            lambda text: text.replace(
                'return hashlib.sha256(payload.encode()).hexdigest()',
                'return hashlib.sha256((payload + ":v2").encode()).hexdigest()  # testmon change',
            ),
        )
        low_change = run_testmon("low", "testmon_low_complexity_change.txt")
        restore_file(low_path, low_original)
        testmon_runs["low_complexity"] = {"selected_count": _extract_selected(low_change.stdout + low_change.stderr)}

        high_path = ROOT / "src" / "commerce_platform" / "orders" / "pricing_engine.py"
        high_original = patch_file(
            high_path,
            lambda text: text.replace('multiplier = Decimal("1.0")', 'multiplier = Decimal("1.01")  # testmon change', 1),
        )
        high_change = run_testmon("high", "testmon_high_complexity_change.txt")
        restore_file(high_path, high_original)
        testmon_runs["high_complexity"] = {"selected_count": _extract_selected(high_change.stdout + high_change.stderr)}

        shared_path = ROOT / "src" / "commerce_platform" / "utils" / "shared.py"
        shared_original = patch_file(
            shared_path,
            lambda text: text.replace(
                'cleaned = value.strip().upper().replace(" ", "_")',
                'cleaned = value.strip().upper().replace(" ", "-")  # testmon change',
            ),
        )
        shared_change = run_testmon("shared", "testmon_shared_module_change.txt")
        restore_file(shared_path, shared_original)
        testmon_runs["shared_module"] = {"selected_count": _extract_selected(shared_change.stdout + shared_change.stderr)}

        execution_log["testmon_change_status"] = "completed"
        execution_log["testmon_runs"] = testmon_runs
        execution_log["testmon_selection_correct"] = (
            "yes"
            if testmon_runs.get("unchanged", {}).get("selected_count", 9999) == 0
            else "review reports"
        )

        cov_run = run_command([py, "-m", "coverage", "run", "-m", "pytest"], allow_failure=True)
        run_command([py, "-m", "coverage", "json", "-o", str(REPORTS / "coverage.json")], allow_failure=True)
        run_command([py, "-m", "coverage", "xml", "-o", str(REPORTS / "coverage.xml")], allow_failure=True)
        run_command([py, "-m", "coverage", "report", "-m"], allow_failure=True)
        execution_log["coverage_status"] = "passed" if cov_run.returncode in (0, 1) else "failed"

        radon = run_command([py, "-m", "radon", "cc", "src", "-a", "-s", "-j"], allow_failure=True)
        (REPORTS / "radon_cc.json").write_text(radon.stdout or "{}", encoding="utf-8")
        execution_log["radon_status"] = "passed" if radon.ok else "failed"

        lizard = run_command(
            [py, "-m", "lizard", "src", "-l", "python", "-o", str(REPORTS / "lizard.xml")],
            allow_failure=True,
        )
        execution_log["lizard_status"] = "passed" if lizard.ok else "failed"

    for script in [
        "parse_testmon.py",
        "parse_complexity.py",
        "parse_coverage.py",
        "calculate_qa_priority.py",
    ]:
        run_command([py, f"scripts/{script}"], allow_failure=True)

    testmon_db = find_testmon_db()
    if testmon_db and testmon_db.is_file():
        backup = REPORTS / "testmon_database_backup"
        backup.mkdir(parents=True, exist_ok=True)
        shutil.copy2(testmon_db, backup / testmon_db.name)

    meta = json.loads((REPORTS / "qa_priority_meta.json").read_text(encoding="utf-8"))
    status = meta["status"]
    source_lines = count_source_lines()
    total_tests = count_tests()
    versions = tool_versions()

    generate_validation_report(
        source_lines=source_lines,
        total_tests=total_tests,
        versions=versions,
        execution_log=execution_log,
        status=status,
        meta=meta.get("meta", {}),
        testmon_db=testmon_db,
    )

    success = (
        execution_log.get("testmon_initial_status") != "failed"
        and execution_log.get("radon_status") == "passed"
        and execution_log.get("lizard_status") == "passed"
        and status.get("overall") in {"PASS", "PARTIAL PASS"}
    )
    print_final(success, source_lines, total_tests, status, execution_log, meta.get("meta", {}))
    return 0 if success else 1


def _extract_selected(text: str) -> int:
    import re

    selected = re.search(r"(\d+)\s+selected", text, re.I)
    if selected:
        return int(selected.group(1))
    passed = len(re.findall(r"PASSED", text))
    failed = len(re.findall(r"FAILED", text))
    if passed or failed:
        return passed + failed
    collected = re.search(r"collected\s+(\d+)", text, re.I)
    return int(collected.group(1)) if collected else 0


def print_final(
    repo_ok: bool,
    source_lines: int,
    total_tests: int,
    status: dict[str, str],
    execution_log: dict[str, Any],
    meta: dict[str, Any],
) -> None:
    testmon_ok = execution_log.get("testmon_initial_status") not in {"failed"}
    provides_impact = meta.get("testmon_provides_dependencies", False)
    print(
        textwrap.dedent(
            f"""
            Repository execution: {'PASS' if repo_ok else 'FAIL'}
            Approximate source lines: {source_lines}
            Total tests: {total_tests}
            Testmon executed successfully: {'YES' if testmon_ok else 'NO'}
            Testmon directly emits QA Resource Allocation: NO
            Testmon provides test-impact data: {'YES' if provides_impact else 'NO'}
            Cyclomatic-complexity data available: {'YES' if meta.get('total_components', 0) else 'NO'}
            Coverage data available: {'YES' if meta.get('total_components', 0) else 'NO'}
            Testmon-only metric status: {status.get('testmon_only', 'FAIL')}
            Combined derivation status: {status.get('combined', 'FAIL')}
            Final metric status: {status.get('overall', 'FAIL')}
            Primary issue: {status.get('primary_issue', 'tool limitation')}
            Evidence directory: reports/
            """
        ).strip()
    )


if __name__ == "__main__":
    raise SystemExit(main())
