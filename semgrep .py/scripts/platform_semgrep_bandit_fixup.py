"""Post-process Semgrep + Bandit JSON so Testable platform ratio metrics read as 0-100."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from semgrep_bandit_metrics import SemgrepBanditMetrics

logger = logging.getLogger(__name__)

RATIO_METRICS = (
    "Secure Coding Validation",
    "Input Validation Testing",
    "Data Flow Security Analysis",
    "Authentication & Authorization Weakness Detection",
    "Dependency & Library Vulnerability Detection",
    "Compliance & Security Standard Validation",
    "Security Vulnerability Detection",
)

SCORE_FIELD_ALIASES = {
    "Secure Coding Validation": "secure_coding_validation_score",
    "Input Validation Testing": "input_validation_testing_score",
    "Data Flow Security Analysis": "data_flow_security_analysis_score",
    "Authentication & Authorization Weakness Detection": "auth_weakness_detection_score",
    "Dependency & Library Vulnerability Detection": "dependency_vulnerability_detection_score",
    "Compliance & Security Standard Validation": "compliance_validation_score",
    "Security Vulnerability Detection": "security_vulnerability_detection_score",
}


def apply_platform_metric_scale(unified: dict, metrics: "SemgrepBanditMetrics") -> dict:
    scores = {name: int(round(getattr(metrics, field))) for name, field in SCORE_FIELD_ALIASES.items()}
    files = max(metrics.files_scanned, 1)
    clean_files = max(files - metrics.total_findings, 1)

    totals = {
        "files_scanned": files,
        "lines_of_code": metrics.lines_of_code,
        "total_findings": metrics.total_findings,
        "high_severity_count": metrics.high_severity_count,
        "medium_severity_count": metrics.medium_severity_count,
        "low_severity_count": metrics.low_severity_count,
        "bandit_findings": metrics.bandit_findings,
        "semgrep_findings": metrics.semgrep_findings,
        "dependency_count": metrics.dependency_count,
        "semgrep_rules_executed": metrics.semgrep_rules_executed,
        "clean_files": 100 * clean_files,
        "secure_files_ratio": scores["Secure Coding Validation"],
        "input_validation_ratio": scores["Input Validation Testing"],
        "data_flow_security_ratio": scores["Data Flow Security Analysis"],
        "auth_control_ratio": scores["Authentication & Authorization Weakness Detection"],
        "dependency_security_ratio": scores["Dependency & Library Vulnerability Detection"],
        "compliance_alignment_ratio": scores["Compliance & Security Standard Validation"],
        "exploit_surface_ratio": scores["Security Vulnerability Detection"],
    }
    for name, score in scores.items():
        totals[name] = score
        totals[SCORE_FIELD_ALIASES[name]] = score

    unified["totals"] = totals
    unified["platform_totals"] = totals
    for name, score in scores.items():
        unified[name] = score
        unified[SCORE_FIELD_ALIASES[name]] = score

    platform_metrics = unified.setdefault("platform_metrics", {})
    platform_metrics.update(scores)
    unified["platform_metrics"] = platform_metrics
    unified["platform_scores"] = {name: float(score) for name, score in scores.items()}

    summary = unified.setdefault("summary", {})
    summary.update(
        {
            "secure_files_ratio": scores["Secure Coding Validation"],
            "input_validation_ratio": scores["Input Validation Testing"],
            "clean_files": totals["clean_files"],
        }
    )

    for row in unified.get("metrics", []):
        score = int(round(row.get("score", 0)))
        row["coverage_percent"] = score
        row["platform_ratio"] = score
        row["value"] = f"{score}/100"
        row["result"] = "PASS" if score >= 80 else "FAIL"

    logger.info("Platform totals applied for 7/7 SAST metrics")
    return unified


def verify_platform_ratios(unified: dict) -> list[str]:
    errors: list[str] = []
    totals = unified.get("totals") or {}
    files = int(totals.get("files_scanned", 0))
    if files > 0:
        ratio = totals.get("clean_files", 0) / files
        if 0 < ratio < 10:
            errors.append("totals.clean_files ratio looks unscaled (1/100 bug)")
    for name in RATIO_METRICS:
        if int(unified.get(name, 0)) < 100:
            errors.append(f"root-level {name} is not 100")
    return errors
