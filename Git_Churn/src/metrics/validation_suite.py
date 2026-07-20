"""Code Churn -> Test Case Maintenance Identification -> Validation Suite Updates."""

from __future__ import annotations

from typing import Any, Dict, Set

from src.file_filters import is_production_file, is_test_path, prod_has_matching_test
from src.models import RepoSnapshot
from src.regression_registry import load_regression_mappings, regression_coverage
from src.scoring import metric_result, pct, score_gate, stale_test_confidence_score


def compute_validation_suite_updates(
    snapshot: RepoSnapshot,
    stale_churn_threshold_pct: float,
) -> Dict[str, Any]:
    changed_test = snapshot.test_files_changed
    changed_prod = {path for path in snapshot.prod_files_changed if is_production_file(path)}
    ratio = round(len(changed_test) / max(len(changed_prod), 1), 4)

    coverage = regression_coverage(changed_prod, changed_test, load_regression_mappings())
    maintenance_coverage = coverage["regression_coverage_pct"]

    all_test_files = {fp for fp in snapshot.file_stats if is_test_path(fp)}
    stale_tests = [fp for fp in all_test_files if fp not in changed_test]
    stale_pct = pct(len(stale_tests), max(len(all_test_files), 1))

    evidence_available = len(changed_test) > 0 and len(snapshot.paired_maintenance_commits) > 0

    if not evidence_available:
        score = 0.0
        status = "FAIL"
    else:
        ratio_score = min(100.0, round(ratio * 100, 2)) if ratio <= 1 else 100.0
        score = min(
            stale_test_confidence_score(stale_pct),
            maintenance_coverage,
            ratio_score if ratio_score > 0 else maintenance_coverage,
        )
        if maintenance_coverage >= 100 and stale_pct <= 5:
            score = 100.0
        status = score_gate(score, 100.0, higher_is_better=True)

    return metric_result(
        metric_id="validation_suite_updates",
        technique="Code Churn",
        classification="Test Case Maintenance Identification",
        metric_name="Validation Suite Updates",
        value={
            "changed_test_files": len(changed_test),
            "changed_prod_files": len(changed_prod),
            "validation_suite_update_ratio": ratio,
            "stale_test_pct": stale_pct,
            "maintenance_coverage_pct": maintenance_coverage,
            "evidence_available": evidence_available,
            "paired_commit_count": len(snapshot.paired_maintenance_commits),
            "covered_modules": coverage["covered_modules"],
            "missing_modules": coverage["missing_modules"],
        },
        score=score,
        status=status,
        details={
            "formula": "Validation Suite Updates = changed_test_files / changed_prod_files",
            "score_formula": "MAX(0, 100 - (Stale_Test% x 10)) x maintenance coverage",
            "threshold": "< 5% stale test files; 100% prod-test mapping",
            "maintenance_evidence": snapshot.paired_maintenance_commits[:30],
        },
    )
