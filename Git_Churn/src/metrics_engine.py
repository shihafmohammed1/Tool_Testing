"""PyDriller metric calculators aligned to Testable Strategy Mapping v0.2."""

from __future__ import annotations

from typing import Any, Dict, List

from src.metrics import (
    compute_audit_trail_verification,
    compute_code_churn_score,
    compute_fault_probability_modeling,
    compute_impact_driven_verification,
    compute_side_effect_mapping,
    compute_validation_suite_updates,
)
from src.models import RepoSnapshot


def compute_all_metrics(snapshot: RepoSnapshot, defaults: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        compute_audit_trail_verification(snapshot),
        compute_code_churn_score(snapshot, defaults.get("time_window_days", 30)),
        compute_impact_driven_verification(snapshot, defaults.get("high_churn_threshold_pct", 30)),
        compute_fault_probability_modeling(snapshot),
        compute_validation_suite_updates(snapshot, defaults.get("stale_churn_threshold_pct", 20)),
        compute_side_effect_mapping(snapshot),
    ]
