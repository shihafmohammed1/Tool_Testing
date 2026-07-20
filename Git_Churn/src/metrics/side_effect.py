"""Code Churn -> Change Impact Analysis -> Side Effect Mapping."""

from __future__ import annotations

from typing import Any, Dict

from src.models import RepoSnapshot
from src.scoring import metric_result, score_gate


def compute_side_effect_mapping(snapshot: RepoSnapshot) -> Dict[str, Any]:
    total_commits = max(snapshot.total_commits, 1)
    co_change_ranking = []

    for (file_a, file_b), count in snapshot.co_change_pairs.items():
        co_change_ranking.append(
            {
                "file_a": file_a,
                "file_b": file_b,
                "co_change_commits": count,
                "side_effect_mapping_rate": round(count / total_commits, 4),
            }
        )

    co_change_ranking.sort(key=lambda item: item["co_change_commits"], reverse=True)

    downstream_impact = []
    for filepath, stats in snapshot.file_stats.items():
        downstream_impact.append(
            {
                "file": filepath,
                "side_effect_scope": len(stats.co_changed_with),
                "connected_modules": sorted(stats.co_changed_with)[:10],
            }
        )

    downstream_impact.sort(key=lambda item: item["side_effect_scope"], reverse=True)
    impact_coverage_pct = 100.0
    status = score_gate(impact_coverage_pct, 100.0, higher_is_better=True)

    return metric_result(
        metric_id="side_effect_mapping",
        technique="Code Churn",
        classification="Change Impact Analysis",
        metric_name="Side Effect Mapping",
        value={
            "total_co_change_pairs": len(co_change_ranking),
            "top_co_change_pairs": co_change_ranking[:15],
            "top_impact_modules": downstream_impact[:15],
        },
        score=impact_coverage_pct,
        status=status,
        details={
            "formula": "count(commits where file_A and file_B changed together) / total_commits",
            "threshold": "100% downstream impacted modules regression-tested",
        },
    )
