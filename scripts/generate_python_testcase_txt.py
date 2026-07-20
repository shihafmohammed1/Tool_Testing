#!/usr/bin/env python3
"""Generate QA validation testcase .txt files for Python White Box tools."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_whitebox_audit_excel import (  # noqa: E402
    TOOL_FOLDER_MAP,
    build_tool_groups,
    canonical_tool_key,
    issue_matches_tool,
    load_jira_issues,
    parse_whitebox_metrics,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "scripts" / "testcases"
DEFAULT_TOOLS = ["pylint", "cognitive-ast", "cosmic-ray", "jscpd", "pydriller"]
GOLDEN_REPO_BASE = "https://github.com/testable-platform/Testable-WhiteBox-Repo/tree/Python_1.1"
COMMON_TEST_REPOS = [
    "https://github.com/django/django",
    "https://github.com/pallets/flask",
]

TOOL_TEST_REPOS: dict[str, list[str]] = {
    "coverage.py": ["https://github.com/visvantha-testable/python-tool-testing-coverage-py"],
    "coverage.py + beniget": [
        "https://github.com/visvantha-testable/python-tool-testing-coverage-py-beniget",
        "https://github.com/serge-sans-paille/beniget",
    ],
    "pip-audit": ["https://github.com/visvantha-testable/python-tool-testing-pip-audit"],
    "pymcdc": ["https://github.com/visvantha-testable/python-tool-testing-pymcdc"],
    "semgrep oss + bandit": [
        "https://github.com/visvantha-testable/python-tool-testing-semgrep-bandit"
    ],
}

TOOL_JIRA_OVERRIDES: dict[str, str] = {
    "coverage.py + beniget": "TP-2802",
}

TOOL_DISPLAY_NAMES: dict[str, str] = {
    "coverage.py": "Coverage.py",
    "coverage.py + beniget": "Coverage.py + Beniget",
    "pip-audit": "PIP Audit",
    "semgrep oss + bandit": "Semgrep OSS + Bandit",
    "radon/lizard": "Radon/Lizard",
    "cognitive-ast": "Cognitive-AST",
    "cosmic-ray": "Cosmic-Ray",
    "pydriller": "PyDriller (Git Churn)",
    "crosshair": "CrossHair",
    "jscpd": "JSCPD",
    "pylint": "Pylint",
    "pymcdc": "Pymcdc",
    "beniget": "Beniget",
    "testmon": "Testmon",
}

STEPS_TEMPLATE = """------------------------------------------------------------------------

Step 1: Understand the Tool

-   Identify what the tool is designed to analyze.
-   List all metrics officially supported by the tool.
-   Use AI, official documentation, and the tool's website to understand
    its capabilities.

Output: - Tool capability analysis - Supported metrics list -
Unsupported metrics list

------------------------------------------------------------------------

Step 2: Verify Metric Coverage

-   Collect the list of required metrics and classifications.
-   Compare them against the metrics supported by the tool.
-   Identify which metrics are supported directly.
-   Identify which metrics require derivation or are unsupported.
-   Confirm whether the tool can satisfy the required metric coverage
    before execution.

------------------------------------------------------------------------

Step 3: Find a Suitable Repository

Provide AI with: - Tool name - Required metrics - Required
classifications

Ask AI to recommend a suitable repository that: - Supports the
programming language required by the tool. - Can trigger the tool
successfully. - Covers the required metrics and classifications. -
Contains sufficient source code patterns to generate meaningful
results. - Is either an open-source repository or a repository created
specifically for testing.

Save the repository link for execution.

------------------------------------------------------------------------

Step 4: Create QA Testable Account and Upload Repository

-   Create an individual account in the QA Testable environment.
-   Upload the selected repository (either created by us or an
    open-source repository).
-   Configure the required tool and execute the analysis.

------------------------------------------------------------------------

Step 5: Record the Tenant ID

-   Record the generated Tenant ID.
-   The Tenant ID is required because all generated S3 reports are
    organized under it.

------------------------------------------------------------------------

Step 6: Check S3 Reports

foundation-shared-services -> QA-S3-Readonly -> Click S3 ->
us2-qa-testable -> Search "qa" -> Click "qa-op" -> cell-001 -> Search
using the Tenant ID

------------------------------------------------------------------------

Step 7: Check Tool Folder

Case 1 – Tool Folder Exists - Download raw report, JSON/XML/CSV report,
and output files. - Validate file generation and expected metrics. -
Verify the report with AI.

Case 2 – Tool Folder Does Not Exist - Verify the repository. - Execute
the tool again. - Record the Tenant ID. - Check the S3 location again. -
Repeat until reports are generated.

Case 3 – Tool not execute with Multiple repos so execute in local

Proceed with:
- Step 8: Validate Report Contents
- Step 9: If No Metric Values Are Generated
- Step 10: If Results Are Still Incorrect
- Step 11: Cross-Check the Results
- Step 12: Compare Local and QA Results
- Step 13: Verify Parameters Covered


Step 8: Validate Report Contents

-   Check whether the report is empty.
-   Verify expected metrics are present.
-   Verify report format.
-   Verify expected output files.


Step 9: If No Metric Values Are Generated

-   Repository does not trigger the required metrics.
-   Insufficient or unsuitable test data.

Action: - Modify the repository. - Add suitable code constructs. -
Execute the tool again.

Step 10: If Results Are Still Incorrect

-   Install the tool locally.
-   Clone the repository.
-   Execute the tool locally.
-   Generate the raw output.
-   Compare the local output with QA Testable output.


Step 11: Cross-Check the Results

Compare: - Expected metrics - Generated metrics - AI validation -
Official documentation

Verify: - Metric names - Metric values - Counts - Percentages - Formulas
(if applicable)


Step 12: Compare Local and QA Results

Compare: - Number of files analyzed - Metrics generated - Metric
values - Missing metrics - Report format



Step 13: Verify Parameters Covered

Identify: - Parameters analyzed - Supported metrics - Unsupported
metrics - Derived metrics - Files scanned - Rules executed - Report
outputs

------------------------------------------------------------------------

REPO NAME

Repository Name: {golden_repo_url}

Golden Repo Folder: {golden_folder}

Jira E2E Ticket: {jira_id}

------------------------------------------------------------------------

Expected Deliverables

-   Tool capability analysis
-   Metric coverage validation
-   Repository Name
-   QA Testable execution evidence
-   Tenant ID
-   S3 report
-   Downloaded tool reports
-   AI validation of report contents
-   Local execution report (if required)
-   QA vs Local comparison
-   Final metric coverage summary
"""


FILE_SLUG_OVERRIDES: dict[str, str] = {
    "pydriller": "gitchurn",
}


def slugify(tool: str) -> str:
    if tool in FILE_SLUG_OVERRIDES:
        return FILE_SLUG_OVERRIDES[tool]
    text = tool.lower().replace("/", "-").replace(" + ", "_").replace(" ", "_")
    text = re.sub(r"[^a-z0-9_-]+", "", text.replace(".", ""))
    return text


def display_name(tool: str) -> str:
    return TOOL_DISPLAY_NAMES.get(tool, tool.title())


def folder_for_tool(tool: str) -> str:
    for key, value in TOOL_FOLDER_MAP.items():
        if canonical_tool_key(key, "") == tool:
            return value[1]
    return ""


def golden_repo_url(tool: str) -> str:
    folder = folder_for_tool(tool)
    if folder:
        encoded = folder.replace(" ", "%20")
        return f"{GOLDEN_REPO_BASE}/{encoded}"
    return GOLDEN_REPO_BASE


def test_repos_for_tool(tool: str) -> list[str]:
    seen: set[str] = set()
    repos: list[str] = []
    for url in TOOL_TEST_REPOS.get(tool, []) + COMMON_TEST_REPOS:
        if url not in seen:
            seen.add(url)
            repos.append(url)
    return repos


def format_metrics_table(metrics: list) -> str:
    lines = [
        "  Testing Type                   Technique                       Classification                        Metric",
        "  ----------------             ----------------                 ----------------                  ----------------",
    ]
    for m in metrics:
        lines.append(
            f"  {m.l2:<28} {m.l3:<32} {m.l4:<32} {m.l5}"
        )
    return "\n".join(lines)


def build_objective(tool: str, metrics: list) -> str:
    name = display_name(tool)
    techniques = sorted({m.l3 for m in metrics if m.l3})
    technique_text = ", ".join(techniques[:3])
    if len(techniques) > 3:
        technique_text += ", and related techniques"
    return (
        f"Validate whether {name} correctly detects and reports the expected\n"
        f"metrics by executing it in the QA Testable environment, verifying the\n"
        f"generated reports, and comparing the results with local execution.\n"
        f"\n"
        f"Focus areas include {technique_text}."
    )


def jira_for_tool(tool: str, jira: list) -> tuple[str, str]:
    override = TOOL_JIRA_OVERRIDES.get(tool)
    if override:
        for issue in jira:
            if issue.key == override:
                return issue.key, issue.summary
    e2e = [i for i in jira if issue_matches_tool(i, tool) and i.is_e2e]
    if not e2e:
        return "TBD", ""
    issue = e2e[0]
    return issue.key, issue.summary


def render_testcase(tool: str, metrics: list, jira: list) -> str:
    name = display_name(tool)
    jira_id, _summary = jira_for_tool(tool, jira)
    folder = folder_for_tool(tool)
    repos = test_repos_for_tool(tool)

    parts = [
        f"QA Validation Process for {name}",
        "",
        "Objective",
        "",
        build_objective(tool, metrics),
        "",
        "Metrics Covered:",
        "",
        format_metrics_table(metrics),
        "",
        "Test Data Covered:",
    ]
    parts.extend(repos)
    parts.extend(["", STEPS_TEMPLATE.format(
        golden_repo_url=golden_repo_url(tool),
        golden_folder=folder or "TBD",
        jira_id=jira_id,
    )])
    return "\n".join(parts) + "\n"


def generate_all(output_dir: Path, tools: list[str] | None = None) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    selected = {canonical_tool_key(t, "Python") for t in (tools or DEFAULT_TOOLS)}
    jira = load_jira_issues()
    groups = build_tool_groups(parse_whitebox_metrics())
    written: list[Path] = []

    for (language, tool), metrics in sorted(groups.items()):
        if language != "Python" or tool not in selected:
            continue
        filename = f"Python_Testcase_{slugify(tool)}.txt"
        path = output_dir / filename
        path.write_text(render_testcase(tool, metrics, jira), encoding="utf-8")
        written.append(path)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Python tool QA testcase txt files")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for generated testcase files",
    )
    parser.add_argument(
        "--tools",
        nargs="+",
        default=DEFAULT_TOOLS,
        help="Canonical tool keys to generate (default: pylint cognitive-ast cosmic-ray jscpd pydriller)",
    )
    args = parser.parse_args()
    paths = generate_all(args.output_dir, args.tools)
    print(f"Generated {len(paths)} testcase files in {args.output_dir}")
    for path in paths:
        print(f"  {path.name}")


if __name__ == "__main__":
    main()
