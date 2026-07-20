"""Code Churn -> Risk-Based Testing Prioritization -> Code Churn Score."""

from __future__ import annotations

from typing import Any, Dict, List

from src.metrics.churn_helpers import file_churn_pct, is_high_risk_module, production_file_stats
from src.models import RepoSnapshot
from src.scoring import metric_result, pct, score_gate


def compute_code_churn_score(snapshot: RepoSnapshot, time_window_days: int) -> Dict[str, Any]:
    module_scores: List[Dict[str, Any]] = []
    prod_stats = production_file_stats(snapshot)
    total_churn = 0

    for filepath, stats in prod_stats.items():
        churn = stats.churn
        churn_pct = file_churn_pct(snapshot, filepath, stats)
        total_churn += churn
        denominator = max(stats.commit_count, 1) * time_window_days

        module_scores.append(
            {
                "file": filepath,
                "churn": churn,
                "churn_pct": churn_pct,
                "commit_count": stats.commit_count,
                "code_churn_score": round(churn / denominator, 4),
                "flag_high_risk": is_high_risk_module(churn_pct),
            }
        )

    module_scores.sort(key=lambda item: item["churn_pct"], reverse=True)
    low_risk_modules = sum(1 for m in module_scores if not m["flag_high_risk"])
    module_pass_pct = pct(low_risk_modules, len(module_scores))
    avg_churn_pct = (
        round(sum(m["churn_pct"] for m in module_scores) / len(module_scores), 2)
        if module_scores
        else 0.0
    )
    confidence_score = module_pass_pct
    status = score_gate(confidence_score, 100.0, higher_is_better=True)

    return metric_result(
        metric_id="code_churn_score",
        technique="Code Churn",
        classification="Risk-Based Testing Prioritization",
        metric_name="Code Churn Score",
        value={
            "total_churn": total_churn,
            "files_analyzed": len(module_scores),
            "avg_churn_pct": avg_churn_pct,
            "module_pass_pct": module_pass_pct,
            "low_risk_module_count": low_risk_modules,
            "high_risk_modules": [m for m in module_scores if m["flag_high_risk"]],
            "top_risk_modules": module_scores[:10],
        },
        score=confidence_score,
        status=status,
        details={
            "formula": "Churn% = (lines_added + lines_deleted) / total_LOC (src/ only)",
            "score_formula": "Score = % production modules below 30% churn threshold",
            "threshold": "< 30% churn per sprint; flag modules > 30%",
            "time_window_days": time_window_days,
        },
    )
