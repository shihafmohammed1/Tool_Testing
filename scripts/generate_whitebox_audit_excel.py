#!/usr/bin/env python3
"""Generate WhiteBox_Metrics_Data_Readiness_Audit.xlsx from strategy Excel, git, and Jira."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_XLSX = REPO_ROOT / "SPOTBUGS" / "docs" / "Testable_Strategy_Metrics_Mapping_v0.2.xlsx"
JIRA_JSON = Path(__file__).resolve().parent / "data" / "jira_whitebox_audit.json"
SCRIPTS_DIR = Path(__file__).resolve().parent
SHAREPOINT_BUG_XLSX = SCRIPTS_DIR / "data" / "sharepoint_audit_workbook.xlsx"
SHAREPOINT_BUG_URL = (
    "https://hopewellsolutions.sharepoint.com/:x:/s/Testable-ExecutionTeam/"
    "IQCzRy3rTrp7S6qtDgTt7weFAaOU4WltZoxASErJ7wTbhp4?e=hthT5g"
)
OUTPUT_XLSX = REPO_ROOT / "WhiteBox_Metrics_Data_Readiness_Audit.xlsx"

ARTIFACT_CHECKS = {
    "testing_team": ["TESTING_TEAM", "TESTING_TEAM_GUIDE"],
    "metric_coverage": ["metric_coverage.json"],
    "golden": ["golden"],
    "platform": ["platform"],
    "metrics_mapping": ["metrics-mapping"],
    "validate": ["validate"],
    "taxonomy": ["taxonomy"],
    "output_files": ["metrics.json", "spotbugs.json", "dashboard", "artifacts/"],
    "subject_volume": ["subject_volume", "generated-volume"],
    "generate_subject": ["generate_subject_code"],
}

# Excel primary tool name -> (branch, folder, language)
TOOL_FOLDER_MAP: dict[str, tuple[str, str, str]] = {
    "coverage.py": ("Python_1.1", "coverage .py", "Python"),
    "pylint": ("Python_1.1", "pylint", "Python"),
    "coverage.py + beniget": ("Python_1.1", "coverage + beniget .py", "Python"),
    "pip-audit": ("Python_1.1", "Pip Audit.py", "Python"),
    "cognitive-ast": ("Python_1.1", "Cognitive-AST", "Python"),
    "jscpd": ("Python_1.1", "JSCPD", "Python"),
    "semgrep oss + bandit": ("Python_1.1", "semgrep .py", "Python"),
    "semgrep oss\n+ \nbandit": ("Python_1.1", "semgrep .py", "Python"),
    "cosmic-ray": ("Python_1.1", "cosmic-ray", "Python"),
    "pydriller": ("Python_1.1", "Git_Churn", "Python"),
    "crosshair": ("Python_1.1", "crosshair", "Python"),
    "beniget": ("Python_1.1", "Beniget", "Python"),
    "pymcdc": ("Python_1.1", "pymcdc.py", "Python"),
    "radon/lizard": ("Python_1.1", "randon-lizard", "Python"),
    "testmon": ("Python_1.1", "TESTMON", "Python"),
    "spotbugs": ("Java_1.1", "SPOTBUGS", "Java"),
    "pit": ("Java_1.1", "PIT", "Java"),
    "checkstyle": ("Java_1.1", "", "Java"),
    "jacoco": ("Java_1.1", "", "Java"),
    "pmd": ("Java_1.1", "", "Java"),
    "cpd": ("Java_1.1", "", "Java"),
    "ck": ("Java_1.1", "", "Java"),
    "git": ("Java_1.1", "", "Java"),
    "static du": ("Java_1.1", "", "Java"),
    "diff-coverage": ("Java_1.1", "", "Java"),
    "owasp dependency-check": ("Java_1.1", "Dependency_Check", "Java"),
}

TOOL_KEYWORDS: dict[str, list[str]] = {
    "coverage.py": ["coverage.py", "coverage-py", "coverge.py"],
    "pylint": ["pylint"],
    "coverage.py + beniget": ["beniget", "coverge.py+beniget", "coverage+beniget"],
    "pip-audit": ["pip audit", "pip-audit"],
    "cognitive-ast": ["cognitive-ast", "cognitive ast"],
    "jscpd": ["jscpd"],
    "semgrep oss + bandit": ["semgrep", "bandit"],
    "cosmic-ray": ["cosmic-ray", "cosmic ray"],
    "pydriller": ["pydriller", "git-churn", "git churn"],
    "crosshair": ["crosshair"],
    "beniget": ["beniget"],
    "pymcdc": ["pymcdc"],
    "radon/lizard": ["randon", "lizard", "radon"],
    "testmon": ["testmon"],
    "spotbugs": ["spotbugs", "spot bugs"],
    "pit": ["pit", "pitest"],
    "checkstyle": ["checkstyle"],
    "jacoco": ["jacoco"],
    "pmd": ["pmd"],
    "cpd": ["cpd", "cpm"],
    "ck": [" ck", '"ck"', " ck tool"],
    "owasp dependency-check": ["owasp", "dependency-check", "dependency check"],
    "git": ["java tool - git", "git + jacoco"],
    "static du": ["static du"],
    "diff-coverage": ["diff-coverage", "diff coverage"],
}

AUDIT_COLUMNS = [
    "Tool",
    "Language",
    "Testing Type",
    "Technique",
    "Classification",
    "Metric Name",
    "Jira ID",
    "Output File(s) Empty or Non Empty",
    "Completed",
    "DB vs UI / Taxonomy Values Verified?",
    "% Completion",
    "ETA",
    "Owner",
    "Notes / Blockers",
    "Bug ID",
    "Golden Repo",
]

TOOL_AUDIT_SHEET_COLUMNS = AUDIT_COLUMNS + ["Repo Evidence", "Test Case"]

TEAM_SHEET_DROP_COLUMNS = {
    "Output File(s) Empty or Non Empty",
    "DB vs UI / Taxonomy Values Verified?",
    "ETA",
    "% Completion",
}


def tool_audit_sheet_columns(team_sheet: bool = False) -> list[str]:
    audit_cols = (
        [col for col in AUDIT_COLUMNS if col not in TEAM_SHEET_DROP_COLUMNS]
        if team_sheet
        else AUDIT_COLUMNS
    )
    return audit_cols + ["Repo Evidence", "Test Case"]

JIRA_BROWSE_URL = "https://testable.atlassian.net/browse/"
GOLDEN_REPO_URL = "https://github.com/testable-platform/Testable-WhiteBox-Repo.git"
LINK_FONT = Font(color="0563C1", underline="single")
FILL_GREEN = PatternFill("solid", fgColor="C6EFCE")
FILL_YELLOW = PatternFill("solid", fgColor="FFEB9C")
FILL_RED = PatternFill("solid", fgColor="FFC7CE")
HEADER_FILL = PatternFill("solid", fgColor="4472C4")
HEADER_FONT = Font(color="FFFFFF", bold=True)
SECTION_DIVIDER_KEY = "_section_divider"
SECTION_FILL = PatternFill("solid", fgColor="D9E1F2")
SECTION_FONT = Font(bold=True, size=12)
CELL_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
HEADER_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)


@dataclass
class MetricRow:
    l1: str
    l2: str
    l3: str
    l4: str
    l5: str
    measure: str
    python_primary: str
    java_primary: str
    raw_formula: str
    norm_formula: str
    language: str
    primary_tool: str


@dataclass
class RepoArtifacts:
    branch: str
    folder: str
    file_count: int
    hits: dict[str, bool] = field(default_factory=dict)
    evidence_paths: list[str] = field(default_factory=list)


@dataclass
class JiraIssue:
    key: str
    summary: str
    status: str
    assignee: str
    updated: str
    description: str
    is_e2e: bool
    is_open: bool
    is_bug: bool


def normalize_tool(name: str) -> str:
    text = re.sub(r"\s+", " ", (name or "").strip().lower())
    text = text.replace("\n", " ").replace("+", " + ")
    text = re.sub(r" +", " ", text)
    if text.startswith("owasp"):
        return "owasp dependency-check"
    return text


def canonical_tool_key(tool: str, language: str) -> str:
    norm = normalize_tool(tool)
    if norm.startswith("owasp"):
        return "owasp dependency-check"
    if norm in {"jscpd"} or norm.startswith("jscpd "):
        return "jscpd"
    if norm in {"spotbugs"} or norm.startswith("spotbugs "):
        return "spotbugs"
    if norm in {"pit", "pitest"} or norm.startswith("pit "):
        return "pit"
    if "checkstyle" in norm:
        return "checkstyle"
    if norm in {"pmd"} or norm.startswith("pmd "):
        return "pmd"
    if norm in {"cpd", "cpm"} or norm.startswith("cpd ") or "cpm" in norm:
        return "cpd"
    if norm in {"ck"} or norm.startswith("ck "):
        return "ck"
    if "jacoco" in norm:
        return "jacoco"
    if "static du" in norm:
        return "static du"
    if norm.startswith("git") or norm.startswith("git "):
        return "git"
    if "diff-coverage" in norm or "diff coverage" in norm:
        return "diff-coverage"
    if norm in {"semgrep oss + bandit"}:
        return "semgrep oss + bandit"
    return norm


def parse_whitebox_metrics() -> list[MetricRow]:
    wb = load_workbook(SOURCE_XLSX, read_only=True, data_only=True)
    ws = wb["White Box"]
    metrics: list[MetricRow] = []
    for row in ws.iter_rows(min_row=5, values_only=True):
        l1 = row[0] if row else None
        l5 = row[4] if row and len(row) > 4 else None
        if not l1 or str(l1).strip().lower() != "white box" or not l5:
            continue
        py = (row[6] or "").strip() if len(row) > 6 else ""
        java = (row[14] or "").strip() if len(row) > 14 else ""
        language = "Python" if py else "Java"
        primary = py or java
        metrics.append(
            MetricRow(
                l1=str(l1).strip(),
                l2=str(row[1] or "").strip(),
                l3=str(row[2] or "").strip(),
                l4=str(row[3] or "").strip(),
                l5=str(l5).strip(),
                measure=str(row[5] or "").strip() if len(row) > 5 else "",
                python_primary=py,
                java_primary=java,
                raw_formula=str(row[30] or "").strip() if len(row) > 30 else "",
                norm_formula=str(row[32] or "").strip() if len(row) > 32 else "",
                language=language,
                primary_tool=primary,
            )
        )
    wb.close()
    return metrics


def git_ls_files(branch: str, folder: str) -> list[str]:
    if not folder:
        return []
    ref = f"origin/{branch}"
    try:
        out = subprocess.check_output(
            ["git", "ls-tree", "-r", "--name-only", ref, folder],
            cwd=REPO_ROOT,
            text=True,
            errors="ignore",
        )
    except subprocess.CalledProcessError:
        return []
    return [line for line in out.splitlines() if line.strip()]


def scan_repo_artifacts(tool_key: str) -> RepoArtifacts | None:
    mapping = None
    for key, value in TOOL_FOLDER_MAP.items():
        if normalize_tool(key) == tool_key or key == tool_key:
            mapping = value
            break
    if tool_key == "owasp dependency-check":
        mapping = ("Java_1.1", "Dependency_Check", "Java")
    if not mapping:
        return None
    branch, folder, _lang = mapping
    files = git_ls_files(branch, folder)
    if not folder:
        return RepoArtifacts(branch=branch, folder="", file_count=0)
    hits: dict[str, bool] = {}
    evidence: list[str] = []
    for check, patterns in ARTIFACT_CHECKS.items():
        matched = any(any(p.lower() in f.lower() for p in patterns) for f in files)
        hits[check] = matched
        if matched:
            for f in files:
                if any(p.lower() in f.lower() for p in patterns):
                    evidence.append(f"{branch}:{f}")
                    break
    return RepoArtifacts(branch=branch, folder=folder, file_count=len(files), hits=hits, evidence_paths=evidence[:8])


def load_jira_issues() -> list[JiraIssue]:
    if not JIRA_JSON.exists():
        return []
    payload = json.loads(JIRA_JSON.read_text(encoding="utf-8"))
    issues: list[JiraIssue] = []
    for item in payload.get("issues", []):
        fields = item.get("fields", {})
        status = (fields.get("status") or {}).get("name", "")
        assignee = (fields.get("assignee") or {}).get("displayName", "")
        desc = fields.get("description") or ""
        if isinstance(desc, dict):
            desc = json.dumps(desc)
        summary = fields.get("summary") or ""
        issue_type = ((fields.get("issuetype") or {}).get("name") or "").lower()
        issues.append(
            JiraIssue(
                key=item.get("key", ""),
                summary=summary,
                status=status,
                assignee=assignee,
                updated=fields.get("updated", ""),
                description=str(desc),
                is_e2e="end to end validation" in summary.lower(),
                is_open=status.lower() not in {"done", "closed", "resolved"},
                is_bug=issue_type == "bug",
            )
        )
    return issues


def issue_matches_tool(issue: JiraIssue, tool_key: str) -> bool:
    hay = f"{issue.summary} {issue.description}".lower()
    keywords = TOOL_KEYWORDS.get(tool_key, [tool_key])
    return any(kw.lower() in hay for kw in keywords)


def jira_issues_by_key(jira: list[JiraIssue]) -> dict[str, JiraIssue]:
    return {issue.key.upper(): issue for issue in jira if issue.key}


def primary_tools_for_bug(issue: JiraIssue) -> list[str]:
    """Map a Jira Bug issue to canonical tool key(s) using summary/description."""
    text = f"{issue.summary} {issue.description}".lower()

    specific_rules: list[tuple[str, str]] = [
        (r"\bck tool\b|\bjava tool.?[\"']?ck[\"']?", "ck"),
        (r"\blizard\b", "radon/lizard"),
        (r"\bpitest\b|\bjava tool.?[\"']?pit[\"']?", "pit"),
        (r"\bspotbugs\b", "spotbugs"),
        (r"\bpip[- ]audit\b", "pip-audit"),
        (r"\bowasp\b|\bdependency-check\b", "owasp dependency-check"),
        (r"\bsemgrep\b|\bbandit\b", "semgrep oss + bandit"),
    ]
    for pattern, tool in specific_rules:
        if re.search(pattern, text, re.I):
            return [tool]

    category_rules: list[tuple[str, list[str]]] = [
        (r"secret detection", ["semgrep oss + bandit"]),
        (r"dependency risk|\(sca\)", ["pip-audit", "owasp dependency-check"]),
        (r"static vulnerabilities|\(sast\)", ["semgrep oss + bandit", "spotbugs"]),
    ]
    for pattern, tools in category_rules:
        if re.search(pattern, text, re.I):
            return tools
    return []


def build_tool_bug_map_from_jira(jira: list[JiraIssue]) -> dict[str, list[str]]:
    tool_map: dict[str, set[str]] = defaultdict(set)
    for issue in jira:
        if not issue.is_bug:
            continue
        for tool_key in primary_tools_for_bug(issue):
            tool_map[tool_key].add(issue.key.upper())
    return {tool: sorted(bug_ids) for tool, bug_ids in sorted(tool_map.items())}


def load_tool_bug_map_from_reference(path: Path | None, jira: list[JiraIssue]) -> dict[str, list[str]]:
    """Load Bug ID mappings from Jira BUG issues, with optional SharePoint Tool Audit overrides."""
    by_key = jira_issues_by_key(jira)
    tool_map: dict[str, set[str]] = defaultdict(set)
    for tool, bug_ids in build_tool_bug_map_from_jira(jira).items():
        tool_map[tool].update(bug_ids)

    if not path or not path.exists():
        return {tool: sorted(bug_ids) for tool, bug_ids in sorted(tool_map.items())}

    wb = load_workbook(path, read_only=True, data_only=True)

    if "Tool Audit" in wb.sheetnames:
        ws = wb["Tool Audit"]
        header_row = next(ws.iter_rows(min_row=1, max_row=1, values_only=True))
        headers = [normalize_header(value) for value in header_row]
        tool_idx = headers.index("tool") if "tool" in headers else None
        bug_idx = headers.index("bug id") if "bug id" in headers else None
        if tool_idx is not None and bug_idx is not None:
            for row in ws.iter_rows(min_row=2, values_only=True):
                tool_val = row[tool_idx] if tool_idx < len(row) else None
                bug_val = row[bug_idx] if bug_idx < len(row) else None
                if not tool_val or not bug_val or str(tool_val).upper() == "JAVA":
                    continue
                tool_key = canonical_tool_key(str(tool_val), "")
                manual_ids = {
                    token.strip().upper()
                    for token in re.split(r"[,;\s]+", str(bug_val))
                    if re.fullmatch(r"TP-\d+", token.strip(), re.I)
                }
                manual_ids = {
                    bug_key
                    for bug_key in manual_ids
                    if bug_key in by_key and by_key[bug_key].is_bug
                }
                if manual_ids:
                    tool_map[tool_key] = manual_ids

    wb.close()
    return {tool: sorted(bug_ids) for tool, bug_ids in sorted(tool_map.items())}


def resolve_bug_source_path(bug_source: Path | None, _input_path: Path | None) -> Path | None:
    if bug_source:
        return bug_source
    if SHAREPOINT_BUG_XLSX.exists():
        return SHAREPOINT_BUG_XLSX
    return None


def golden_repo_label(language: str) -> str:
    return "python_golden_repo"


def status_label(value: str) -> str:
    if value in {"Yes", "Done", "Non Empty", "Verified", "Correct", "Completed"}:
        return "Yes"
    if value in {"Partial", "QA In Progress", "In Progress", "To Do"}:
        return "Partial"
    if value in {"No", "Empty", "Missing", "Not Verified", "Incorrect", "Not Started"}:
        return "No"
    if value in {"N/A", ""}:
        return "N/A"
    return value


def format_metric_names_by_technique(metrics: list[MetricRow]) -> str:
    """Deprecated: metric rows are now one row per metric in Tool Audit."""
    return ""


def jira_id_for_tool(e2e_key: str) -> str:
    """Return TP ticket id only (e.g. TP-2822)."""
    key = (e2e_key or "").strip()
    if re.fullmatch(r"TP-\d+", key, re.I):
        return key.upper()
    return ""


def apply_jira_hyperlink(cell, jira_id: str) -> None:
    if not jira_id:
        return
    cell.value = jira_id
    cell.hyperlink = f"{JIRA_BROWSE_URL}{jira_id}"
    cell.font = LINK_FONT


def apply_golden_repo_hyperlink(cell, label: str, url: str = GOLDEN_REPO_URL) -> None:
    if not label:
        return
    cell.value = label
    cell.hyperlink = url
    cell.font = LINK_FONT


def apply_bug_id_hyperlinks(cell, bug_ids: list[str]) -> None:
    if not bug_ids:
        return
    if len(bug_ids) == 1:
        apply_jira_hyperlink(cell, bug_ids[0])
        return
    formula = "=" + '&", "&'.join(
        f'HYPERLINK("{JIRA_BROWSE_URL}{bug_id}","{bug_id}")' for bug_id in bug_ids
    )
    cell.value = formula
    cell.font = LINK_FONT


def build_metric_audit_rows(
    metrics: list[MetricRow],
    jira: list[JiraIssue],
    tool_bug_map: dict[str, list[str]],
) -> list[dict]:
    """One audit row per metric per tool (language-specific primary tool)."""
    rows: list[dict] = []
    tool_groups = build_tool_groups(metrics)
    tool_audits: dict[tuple[str, str], dict] = {}
    jira_by_key = jira_issues_by_key(jira)

    for (language, tool_key) in sorted(tool_groups):
        group = tool_groups[(language, tool_key)]
        repo = scan_repo_artifacts(tool_key)
        tool_audit = compute_tool_audit(tool_key, group, repo, jira, tool_bug_map, jira_by_key)
        tool_audit["Language"] = language
        tool_audit["Tool"] = tool_key
        tool_audit["Repo Evidence"] = tool_audit.get("_repo_evidence", "")
        tool_audits[(language, tool_key)] = tool_audit
        e2e_key = tool_audit.get("E2E Jira Key", "")

        for m in group:
            rows.append(
                {
                    "Tool": tool_key,
                    "Language": language,
                    "Testing Type": m.l2,
                    "Technique": m.l3,
                    "Classification": m.l4,
                    "Metric Name": m.l5,
                    "Jira ID": jira_id_for_tool(e2e_key),
                    "Output File(s) Empty or Non Empty": tool_audit["Output File(s) Empty or Non Empty"],
                    "Completed": tool_audit["Completed"],
                    "DB vs UI / Taxonomy Values Verified?": tool_audit[
                        "DB vs UI / Taxonomy Values Verified?"
                    ],
                    "% Completion": tool_audit["% Completion"],
                    "ETA": tool_audit["ETA"],
                    "Owner": tool_audit["Owner"],
                    "Notes / Blockers": tool_audit["Notes / Blockers"],
                    "Bug ID": tool_audit["Bug ID"],
                    "Golden Repo": golden_repo_label(language),
                    "Repo Evidence": tool_audit["Repo Evidence"],
                    "Test Case": "",
                    "_checks": tool_audit["_checks"],
                    "_bug_ids": tool_audit.get("_bug_ids", []),
                }
            )
    return rows


def order_metric_rows_with_sections(rows: list[dict]) -> list[dict]:
    """Python metrics first, then a JAVA section divider row, then Java metrics."""
    python_rows = sorted(
        [r for r in rows if r.get("Language") == "Python"],
        key=lambda r: (r["Tool"], r["Technique"], r["Metric Name"]),
    )
    java_rows = sorted(
        [r for r in rows if r.get("Language") == "Java"],
        key=lambda r: (r["Tool"], r["Technique"], r["Metric Name"]),
    )
    ordered = list(python_rows)
    if java_rows:
        ordered.append({SECTION_DIVIDER_KEY: True, "label": "JAVA"})
        ordered.extend(java_rows)
    return ordered


def write_tool_audit_data_rows(
    ws,
    header_row: int,
    ordered_rows: list[dict],
    preserve_manual: bool = False,
    preserved_eta: dict[tuple[str, str, str], object] | None = None,
    team_sheet: bool = False,
) -> None:
    headers = tool_audit_sheet_columns(team_sheet)
    preserved_eta = preserved_eta or {}
    row_idx = header_row

    for item in ordered_rows:
        row_idx += 1
        if item.get(SECTION_DIVIDER_KEY):
            label = item.get("label", "JAVA")
            cell = ws.cell(row=row_idx, column=1, value=label)
            cell.font = SECTION_FONT
            cell.fill = SECTION_FILL
            cell.alignment = Alignment(horizontal="left", vertical="center")
            if len(headers) > 1:
                ws.merge_cells(
                    start_row=row_idx,
                    start_column=1,
                    end_row=row_idx,
                    end_column=len(headers),
                )
            continue

        audit = item
        if preserve_manual:
            eta_key = (
                str(audit["Tool"]).lower(),
                str(audit["Language"]).lower(),
                str(audit["Metric Name"]).lower(),
            )
            if eta_key in preserved_eta:
                audit = {**audit, "ETA": preserved_eta[eta_key]}
        for col, header in enumerate(headers, 1):
            value = audit.get(header, "")
            if team_sheet:
                if header == "Completed":
                    value = "Yes"
                elif header == "Repo Evidence":
                    value = ""
            cell = ws.cell(row=row_idx, column=col, value=value)
            if header == "Jira ID" and value:
                apply_jira_hyperlink(cell, str(value))
            elif header == "Golden Repo" and value:
                apply_golden_repo_hyperlink(cell, str(value))
            elif header == "Bug ID":
                bug_ids = audit.get("_bug_ids") or []
                if bug_ids:
                    apply_bug_id_hyperlinks(cell, bug_ids)
            else:
                apply_status_fill(cell, header, value)
            if team_sheet:
                cell.alignment = CELL_CENTER


def compute_tool_audit(
    tool_key: str,
    metrics: list[MetricRow],
    repo: RepoArtifacts | None,
    jira: list[JiraIssue],
    tool_bug_map: dict[str, list[str]],
    jira_by_key: dict[str, JiraIssue],
) -> dict:
    related = [i for i in jira if issue_matches_tool(i, tool_key)]
    e2e = [i for i in related if i.is_e2e]
    tool_bug_ids = tool_bug_map.get(tool_key, [])
    open_bugs = [
        jira_by_key[bug_key]
        for bug_key in tool_bug_ids
        if bug_key in jira_by_key and jira_by_key[bug_key].is_open
    ]
    e2e_done = any(i.status.lower() == "done" for i in e2e)
    e2e_in_progress = any("progress" in i.status.lower() or i.status.lower() == "to do" for i in e2e)

    l2 = sorted({m.l2 for m in metrics if m.l2})
    l3 = sorted({m.l3 for m in metrics if m.l3})
    language = metrics[0].language if metrics else ""

    output_status = "No"
    if repo and repo.hits.get("platform"):
        output_status = "Non Empty"
    elif repo and repo.hits.get("golden"):
        output_status = "Non Empty"
    elif repo and repo.file_count > 0:
        output_status = "Partial"

    consolidated = "No"
    if e2e_done and not open_bugs:
        consolidated = "Yes"
    elif e2e_done:
        consolidated = "Partial"
    elif e2e_in_progress:
        consolidated = "Partial"

    taxonomy = "No"
    if open_bugs:
        taxonomy = "Partial (open bugs)"
    elif e2e_done:
        taxonomy = "Partial"

    checks = {
        "strategy": bool(metrics),
        "repo_folder": bool(repo and repo.folder and repo.file_count > 0),
        "validation": bool(repo and (repo.hits.get("validate") or repo.hits.get("testing_team"))),
        "output": bool(repo and (repo.hits.get("platform") or repo.hits.get("golden"))),
        "e2e_done": e2e_done,
        "no_open_bugs": not open_bugs,
        "formula_doc": bool(repo and repo.hits.get("metrics_mapping")),
    }
    weights = {
        "strategy": 10,
        "repo_folder": 15,
        "validation": 15,
        "output": 15,
        "e2e_done": 20,
        "no_open_bugs": 15,
        "formula_doc": 10,
    }
    completion = sum(weights[k] for k, ok in checks.items() if ok)

    owner = e2e[0].assignee if e2e else (related[0].assignee if related else "")
    e2e_jira_key = e2e[0].key if e2e else ""
    notes = "; ".join(
        dict.fromkeys(
            [i.key + ": " + i.summary for i in (e2e[:1] + open_bugs[:3])]
        )
    )

    return {
        "Tool": tool_key,
        "Language": language,
        "Testing Type(s)": "; ".join(l2),
        "Technique(s)": "; ".join(l3),
        "Output File(s) Empty or Non Empty": output_status,
        "Completed": consolidated,
        "DB vs UI / Taxonomy Values Verified?": taxonomy,
        "% Completion": completion,
        "ETA": "",
        "Owner": owner,
        "E2E Jira Key": e2e_jira_key,
        "Notes / Blockers": notes,
        "Bug ID": ", ".join(tool_bug_ids),
        "Golden Repo": golden_repo_label(language),
        "_bug_ids": tool_bug_ids,
        "_repo_evidence": "; ".join(repo.evidence_paths if repo else []),
        "_checks": checks,
    }


def metric_missing_columns(row: MetricRow, repo: RepoArtifacts | None, jira: list[JiraIssue]) -> str:
    tool_key = canonical_tool_key(row.primary_tool, row.language)
    missing = []
    if not row.raw_formula:
        missing.append("Formula")
    if not repo or not repo.folder:
        missing.append("Output Files")
    if not repo or not repo.hits.get("platform"):
        missing.append("DB Raw")
    if not any(issue_matches_tool(i, tool_key) for i in jira):
        missing.append("Owner/Jira")
    if not row.norm_formula:
        missing.append("Normalized")
    return ", ".join(missing) if missing else ""


def metric_data_available(missing: str) -> str:
    if not missing:
        return "Yes"
    if len(missing.split(",")) <= 2:
        return "Partial"
    return "No"


def apply_status_fill(cell, column_name: str, value) -> None:
    if column_name == "% Completion":
        try:
            pct = int(value)
        except (TypeError, ValueError):
            return
        if pct >= 80:
            cell.fill = FILL_GREEN
        elif pct >= 50:
            cell.fill = FILL_YELLOW
        else:
            cell.fill = FILL_RED
        return
    label = status_label(str(value))
    if label == "Yes":
        cell.fill = FILL_GREEN
    elif label == "Partial":
        cell.fill = FILL_YELLOW
    elif label == "No":
        cell.fill = FILL_RED


def write_tool_audit_headers(ws, header_row: int, headers: list[str], team_sheet: bool = False) -> None:
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=header_row, column=col, value=header)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = HEADER_CENTER if team_sheet else Alignment(wrap_text=True, vertical="top")


def autosize_columns(ws, max_width: int = 48) -> None:
    for col_idx in range(1, ws.max_column + 1):
        letter = get_column_letter(col_idx)
        max_len = 0
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=col_idx, max_col=col_idx):
            val = row[0].value
            if val is None:
                continue
            max_len = max(max_len, min(len(str(val)), max_width))
        ws.column_dimensions[letter].width = max(12, max_len + 2)


def write_sheet_headers(ws, headers: list[str]) -> None:
    write_tool_audit_headers(ws, 1, headers, team_sheet=False)


def build_tool_groups(metrics: list[MetricRow]) -> dict[tuple[str, str], list[MetricRow]]:
    """Group metrics by (language, canonical tool). White Box rows include both Python and Java primaries."""
    groups: dict[tuple[str, str], list[MetricRow]] = defaultdict(list)
    for m in metrics:
        if m.python_primary:
            py_key = canonical_tool_key(m.python_primary, "Python")
            groups[("Python", py_key)].append(m)
        if m.java_primary:
            java_key = canonical_tool_key(m.java_primary, "Java")
            groups[("Java", java_key)].append(m)
    return groups


def build_workbook(
    metrics: list[MetricRow],
    jira: list[JiraIssue],
    tool_bug_map: dict[str, list[str]],
    team_sheet: bool = False,
) -> Workbook:
    wb = Workbook()

    tool_groups = build_tool_groups(metrics)
    metric_rows = order_metric_rows_with_sections(build_metric_audit_rows(metrics, jira, tool_bug_map))
    tool_audits = []
    seen_tools: set[tuple[str, str]] = set()
    for row in metric_rows:
        if row.get(SECTION_DIVIDER_KEY):
            continue
        key = (row["Language"], row["Tool"])
        if key not in seen_tools:
            seen_tools.add(key)
            tool_audits.append(row)

    # Sheet 1: Tool Audit (one row per metric; Python first, JAVA divider, then Java)
    ws1 = wb.active
    ws1.title = "Tool Audit"
    write_tool_audit_headers(ws1, 1, tool_audit_sheet_columns(team_sheet), team_sheet=team_sheet)
    write_tool_audit_data_rows(ws1, 1, metric_rows, team_sheet=team_sheet)
    ws1.freeze_panes = "A2"
    autosize_columns(ws1, max_width=48)

    # Sheet 2: Metric Detail
    ws2 = wb.create_sheet("Metric Detail")
    metric_headers = [
        "L1 Strategy",
        "L2 Testing Type",
        "L3 Technique",
        "L4 Classification",
        "L5 Metric",
        "Language",
        "Primary Tool (Py | Java)",
        "Raw Measurement Formula",
        "Normalisation Formula (0-100)",
        "Data Available?",
        "Missing Columns",
        "Repo Evidence Path",
        "Jira Reference",
    ]
    write_sheet_headers(ws2, metric_headers)
    for r, m in enumerate(metrics, 2):
        py_key = canonical_tool_key(m.python_primary, "Python") if m.python_primary else ""
        java_key = canonical_tool_key(m.java_primary, "Java") if m.java_primary else ""
        repo = scan_repo_artifacts(py_key) or scan_repo_artifacts(java_key)
        related = list(
            dict.fromkeys(
                i.key
                for key in (py_key, java_key)
                if key
                for i in jira
                if issue_matches_tool(i, key)
            )
        )
        missing = metric_missing_columns(m, repo, jira)
        values = [
            m.l1,
            m.l2,
            m.l3,
            m.l4,
            m.l5,
            f"Python: {m.python_primary}; Java: {m.java_primary}",
            f"Py={m.python_primary} | Java={m.java_primary}",
            m.raw_formula,
            m.norm_formula,
            metric_data_available(missing),
            missing,
            "; ".join(repo.evidence_paths if repo else []),
            ", ".join(related[:5]),
        ]
        for c, val in enumerate(values, 1):
            cell = ws2.cell(row=r, column=c, value=val)
            if metric_headers[c - 1] == "Data Available?":
                apply_status_fill(cell, "Data Available?", val)
        ws2.freeze_panes = "A2"
    autosize_columns(ws2)

    # Sheet 3: Jira Cross-Ref
    ws3 = wb.create_sheet("Jira Cross-Ref")
    jira_headers = ["Key", "Summary", "Status", "Assignee", "Updated", "Type", "Open?", "Matched Tools"]
    write_sheet_headers(ws3, jira_headers)
    seen = set()
    r = 2
    for issue in sorted(jira, key=lambda i: i.updated, reverse=True):
        if issue.key in seen:
            continue
        seen.add(issue.key)
        matched = (
            primary_tools_for_bug(issue)
            if issue.is_bug
            else [t for (_lang, t) in tool_groups if issue_matches_tool(issue, t)]
        )
        ws3.append(
            [
                issue.key,
                issue.summary,
                issue.status,
                issue.assignee,
                issue.updated[:10] if issue.updated else "",
                "Bug" if issue.is_bug else ("E2E Validation" if issue.is_e2e else "Story/Other"),
                "Yes" if issue.is_open else "No",
                ", ".join(matched[:6]),
            ]
        )
        r += 1
    ws3.freeze_panes = "A2"
    autosize_columns(ws3)

    # Sheet 4: Column Legend
    ws4 = wb.create_sheet("Column Legend")
    legend = [
        ("Tool", "White Box sheet primary tool (Python col G / Java col O)", "Auto"),
        ("Testing Type(s)", "Unique L2 values aggregated per tool", "Auto"),
        ("Technique(s)", "Unique L3 values aggregated per tool", "Auto"),
        ("Jira ID", "TP E2E validation ticket with hyperlink to Jira", "Auto"),
        ("Output File(s) Empty or Non Empty", "Repo committed platform/golden/output artifacts", "Derived"),
        ("Completed", "Jira E2E Done + no open bugs", "Derived"),
        ("DB vs UI / Taxonomy Values Verified?", "Jira taxonomy/workbook mismatch bugs", "Derived"),
        ("% Completion", "Weighted checklist (strategy/repo/validation/output/e2e/bugs/formula)", "Derived"),
        ("ETA", "Manual entry", "Manual"),
        ("Owner", "Jira E2E validation assignee", "Auto"),
        ("Notes / Blockers", "Jira summaries for E2E + open bugs", "Auto"),
        ("Bug ID", "Jira Bug issue keys from SharePoint/Jira BUG filter with hyperlinks", "Auto"),
        ("Golden Repo", "python_golden_repo hyperlink to WhiteBox repo", "Auto"),
        ("Test Case", "Manual test case reference", "Manual"),
    ]
    write_sheet_headers(ws4, ["Audit Column", "Source", "Fill Type"])
    for i, row in enumerate(legend, 2):
        ws4.cell(row=i, column=1, value=row[0])
        ws4.cell(row=i, column=2, value=row[1])
        ws4.cell(row=i, column=3, value=row[2])
    autosize_columns(ws4)

    # Sheet 5: Review Gaps (manual review helper)
    ws5 = wb.create_sheet("Review Gaps")
    review_headers = ["Tool", "% Completion", "Priority", "Gap Summary", "Suggested Action", "Reviewer"]
    write_sheet_headers(ws5, review_headers)
    rr = 2
    for audit in sorted(tool_audits, key=lambda a: a["% Completion"]):
        if audit["% Completion"] >= 80:
            continue
        gaps = []
        checks = audit.get("_checks", {})
        if not checks["repo_folder"]:
            gaps.append("No repo folder")
        if not checks["validation"]:
            gaps.append("No validation guide/script")
        if not checks["output"]:
            gaps.append("No committed output/golden")
        if not checks["e2e_done"]:
            gaps.append("E2E validation not Done")
        if not checks["no_open_bugs"]:
            bug_label = audit.get("Bug ID") or "open bugs"
            gaps.append(f"Open bugs: {bug_label}")
        if not checks["formula_doc"]:
            gaps.append("No formula doc/code parity")
        priority = "High" if audit["% Completion"] < 50 else "Medium"
        ws5.cell(row=rr, column=1, value=audit["Tool"])
        ws5.cell(row=rr, column=2, value=audit["% Completion"])
        ws5.cell(row=rr, column=3, value=priority)
        ws5.cell(row=rr, column=4, value="; ".join(gaps))
        ws5.cell(row=rr, column=5, value="Confirm with Owner; fill ETA manually")
        ws5.cell(row=rr, column=6, value=audit["Owner"])
        apply_status_fill(ws5.cell(row=rr, column=2), "% Completion", audit["% Completion"])
        rr += 1
    ws5.freeze_panes = "A2"
    autosize_columns(ws5)

    return wb


def normalize_header(value: object) -> str:
    text = str(value or "").strip().lower()
    text = text.replace("\u2014", "-").replace("\ufffd", "")
    return " ".join(text.split())


def find_header_row(ws) -> tuple[int, dict[str, int]]:
    """Return (header_row_index, header_name -> column_index)."""
    for row_idx in range(1, min(ws.max_row, 10) + 1):
        headers: dict[str, int] = {}
        for col_idx in range(1, ws.max_column + 1):
            val = ws.cell(row=row_idx, column=col_idx).value
            if val:
                headers[normalize_header(val)] = col_idx
        if "tool" in headers and (
            "metric name" in headers
            or "technique" in headers
            or "technique(s)" in headers
            or "# metrics" in headers
        ):
            return row_idx, headers
    raise ValueError("Could not find header row with Tool and metric columns")


def rewrite_tool_audit_sheet(
    ws,
    header_row: int,
    metric_rows: list[dict],
    preserve_manual: bool,
    team_sheet: bool = False,
) -> None:
    """Replace Tool Audit sheet with one row per metric."""
    preserved_eta: dict[tuple[str, str, str], object] = {}
    if preserve_manual:
        header_map = {
            normalize_header(ws.cell(row=header_row, column=c).value): c
            for c in range(1, ws.max_column + 1)
            if ws.cell(row=header_row, column=c).value
        }
        tool_col = header_map.get("tool", 1)
        lang_col = header_map.get("language", 2)
        metric_col = header_map.get("metric name") or header_map.get("metric names")
        eta_col = header_map.get("eta")
        if eta_col and metric_col:
            for row_idx in range(header_row + 1, ws.max_row + 1):
                tool = ws.cell(row=row_idx, column=tool_col).value
                if not tool or str(tool).upper() == "JAVA":
                    continue
                lang = ws.cell(row=row_idx, column=lang_col).value or ""
                metric = ws.cell(row=row_idx, column=metric_col).value or ""
                eta_val = ws.cell(row=row_idx, column=eta_col).value
                if eta_val not in (None, ""):
                    preserved_eta[(str(tool).lower(), str(lang).lower(), str(metric).lower())] = eta_val

    if ws.max_row > header_row:
        ws.delete_rows(header_row + 1, ws.max_row - header_row)

    headers = tool_audit_sheet_columns(team_sheet)
    write_tool_audit_headers(ws, header_row, headers, team_sheet=team_sheet)

    ordered_rows = order_metric_rows_with_sections(metric_rows)
    write_tool_audit_data_rows(
        ws,
        header_row,
        ordered_rows,
        preserve_manual,
        preserved_eta,
        team_sheet=team_sheet,
    )

    ws.freeze_panes = f"A{header_row + 1}"
    autosize_columns(ws, max_width=48)

    extra_cols = ws.max_column - len(headers)
    if extra_cols > 0:
        ws.delete_cols(len(headers) + 1, extra_cols)


def _header_aliases_map() -> tuple[dict[str, str], list[str]]:
    aliases = {
        "tool": "Tool",
        "language": "Language",
        "testing type": "Testing Type",
        "testing type(s)": "Testing Type",
        "technique": "Technique",
        "technique(s)": "Technique",
        "classification": "Classification",
        "metric name": "Metric Name",
        "metric names": "Metric Name",
        "test case": "Test Case",
        "jira id": "Jira ID",
        "output file(s) empty or non empty": "Output File(s) Empty or Non Empty",
        "completed": "Completed",
        "completed?": "Completed",
        "consolidated value vs local execution - completed?": "Completed",
        "consolidated value vs local execution completed?": "Completed",
        "db vs ui / taxonomy values verified?": "DB vs UI / Taxonomy Values Verified?",
        "% completion": "% Completion",
        "eta": "ETA",
        "owner": "Owner",
        "notes / blockers": "Notes / Blockers",
        "bug id": "Bug ID",
        "bugs opened - numbers": "Bug ID",
        "golden repo": "Golden Repo",
        "golden run id": "Golden Repo",
        "repo evidence": "Repo Evidence",
    }
    return aliases, TOOL_AUDIT_SHEET_COLUMNS


def fill_existing_workbook(
    path: Path,
    metrics: list[MetricRow],
    jira: list[JiraIssue],
    tool_bug_map: dict[str, list[str]],
    preserve_manual: bool = True,
    team_sheet: bool = False,
) -> Workbook:
    wb = load_workbook(path)
    sheet_name = "Tool Audit" if "Tool Audit" in wb.sheetnames else wb.sheetnames[0]
    ws = wb[sheet_name]
    header_row, _col_map = find_header_row(ws)
    metric_rows = build_metric_audit_rows(metrics, jira, tool_bug_map)
    rewrite_tool_audit_sheet(ws, header_row, metric_rows, preserve_manual, team_sheet=team_sheet)
    return wb


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate or fill White Box audit Excel")
    parser.add_argument(
        "--input",
        type=Path,
        help="Existing workbook to fill in place (SharePoint local copy)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output path (defaults to --input or repo WhiteBox_Metrics_Data_Readiness_Audit.xlsx)",
    )
    parser.add_argument(
        "--bug-source",
        type=Path,
        help=(
            "SharePoint/reference workbook for Bug ID mapping "
            f"(default: {SHAREPOINT_BUG_XLSX.name} or --input)"
        ),
    )
    parser.add_argument(
        "--team-sheet",
        action="store_true",
        help="Team-fill layout: center cells, Completed=Yes, empty Repo Evidence",
    )
    parser.add_argument(
        "--preserve-manual",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Preserve manually entered ETA values",
    )
    args = parser.parse_args()

    if not SOURCE_XLSX.exists():
        raise FileNotFoundError(f"Source workbook not found: {SOURCE_XLSX}")
    metrics = parse_whitebox_metrics()
    jira = load_jira_issues()
    bug_source = resolve_bug_source_path(args.bug_source, args.input)
    tool_bug_map = load_tool_bug_map_from_reference(bug_source, jira)
    bug_count = sum(len(ids) for ids in tool_bug_map.values())

    if args.input:
        out_path = args.output or args.input
        wb = fill_existing_workbook(
            args.input,
            metrics,
            jira,
            tool_bug_map,
            preserve_manual=args.preserve_manual,
            team_sheet=args.team_sheet,
        )
        wb.save(out_path)
        print(f"Updated {out_path}")
        if args.team_sheet:
            print("  Team sheet mode: centered data, Completed=Yes, Repo Evidence cleared")
            print(f"  SharePoint link for teammates: {SHAREPOINT_BUG_URL}")
    else:
        out_path = args.output or OUTPUT_XLSX
        wb = build_workbook(metrics, jira, tool_bug_map, team_sheet=args.team_sheet)
        wb.save(out_path)
        print(f"Generated {out_path}")

    print(f"  Metrics parsed: {len(metrics)}")
    print(f"  Jira issues loaded: {len(jira)}")
    print(f"  Bug mappings loaded: {bug_count} across {len(tool_bug_map)} tools")
    if bug_source:
        print(f"  Bug source: {bug_source}")
    print(f"  Generated at: {datetime.now().isoformat(timespec='seconds')}")


if __name__ == "__main__":
    main()
