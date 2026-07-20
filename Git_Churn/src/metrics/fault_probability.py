"""Code Churn -> Defect Prediction -> Fault Probability Modeling."""

from __future__ import annotations

from typing import Any, Dict

from src.metrics.churn_helpers import file_churn_pct, production_file_stats
from src.models import RepoSnapshot
from src.scoring import metric_result, score_gate


def compute_fault_probability_modeling(snapshot: RepoSnapshot) -> Dict[str, Any]:
    module_fault_scores = []
    prod_stats = production_file_stats(snapshot)

    for filepath, stats in prod_stats.items():
        churn_pct = file_churn_pct(snapshot, filepath, stats)
        fault_probability_score = round((stats.risk_churn / max(stats.commit_count, 1)) * (churn_pct / 100), 4)
        confidence = max(0, round(100 - (fault_probability_score * 10), 2))

        module_fault_scores.append(
            {
                "file": filepath,
                "fault_probability": round(stats.fault_probability, 4),
                "fault_probability_score": fault_probability_score,
                "confidence_score": confidence,
            }
        )

    module_fault_scores.sort(key=lambda item: item["fault_probability_score"], reverse=True)
    top_score = module_fault_scores[0]["fault_probability_score"] if module_fault_scores else 0.0
    avg_confidence = (
        round(sum(item["confidence_score"] for item in module_fault_scores) / len(module_fault_scores), 2)
        if module_fault_scores
        else 100.0
    )
    status = score_gate(top_score, 5.0, higher_is_better=False)
    score = 100.0 if status == "PASS" else avg_confidence

    return metric_result(
        metric_id="fault_probability_modeling",
        technique="Code Churn",
        classification="Defect Prediction",
        metric_name="Fault Probability Modeling",
        value={"top_fault_probability_score": top_score, "unstable_modules": module_fault_scores[:10]},
        score=score,
        status=status,
        details={
            "formula": "FaultProbability = (added_lines + deleted_lines) / commit_count",
            "threshold": "Fault Probability Score < 5",
        },
    )
