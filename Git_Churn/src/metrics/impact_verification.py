"""Code Churn -> Regression Testing Focus -> Impact-Driven Verification."""

from __future__ import annotations

from typing import Any, Dict, Set

from src.file_filters import is_production_file
from src.metrics.churn_helpers import file_churn_pct
from src.models import RepoSnapshot
from src.regression_registry import regression_coverage
from src.scoring import metric_result, score_gate


def compute_impact_driven_verification(
    snapshot: RepoSnapshot,
    high_churn_threshold_pct: float,
) -> Dict[str, Any]:
    high_churn_modules = []
    high_churn_prod: Set[str] = set()

    for filepath, stats in snapshot.file_stats.items():
        if not is_production_file(filepath):
            continue
        churn_pct = file_churn_pct(snapshot, filepath, stats)
        if churn_pct >= high_churn_threshold_pct:
            high_churn_prod.add(filepath)
            high_churn_modules.append(
                {
                    "file": filepath,
                    "churn": stats.churn,
                    "impact_driven_verification": stats.churn,
                    "churn_pct": churn_pct,
                }
            )

    high_churn_modules.sort(key=lambda item: item["churn"], reverse=True)
    if not high_churn_prod:
        regression_coverage_pct = 100.0
    else:
        coverage = regression_coverage(high_churn_prod, snapshot.test_files_changed)
        regression_coverage_pct = coverage["regression_coverage_pct"]
        covered_modules = coverage["covered_modules"]
        missing_modules = coverage["missing_modules"]
        status = score_gate(regression_coverage_pct, 100.0, higher_is_better=True)
        return metric_result(
            metric_id="impact_driven_verification",
            technique="Code Churn",
            classification="Regression Testing Focus",
            metric_name="Impact-Driven Verification",
            value={
                "high_churn_module_count": len(high_churn_modules),
                "high_churn_threshold_pct": high_churn_threshold_pct,
                "regression_coverage_pct": regression_coverage_pct,
                "modules": high_churn_modules,
                "covered_modules": covered_modules,
                "missing_modules": missing_modules,
            },
            score=regression_coverage_pct,
            status=status,
            details={
                "formula": "Regression Coverage % = high-churn modules in regression suite / total high-churn modules",
                "threshold": "100% of modules with churn > 30% in regression suite",
                "regression_suite": "config/regression_suite.yaml",
            },
        )

    status = score_gate(regression_coverage_pct, 100.0, higher_is_better=True)

    return metric_result(
        metric_id="impact_driven_verification",
        technique="Code Churn",
        classification="Regression Testing Focus",
        metric_name="Impact-Driven Verification",
        value={
            "high_churn_module_count": 0,
            "high_churn_threshold_pct": high_churn_threshold_pct,
            "regression_coverage_pct": regression_coverage_pct,
            "modules": [],
            "covered_modules": [],
            "missing_modules": [],
        },
        score=regression_coverage_pct,
        status=status,
        details={
            "formula": "Regression Coverage % = high-churn modules in regression suite / total high-churn modules",
            "threshold": "100% of modules with churn > 30% in regression suite",
            "regression_suite": "config/regression_suite.yaml",
        },
    )
