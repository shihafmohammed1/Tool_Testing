"""Shared churn calculations for Testable pydriller metrics."""

from __future__ import annotations

from src.file_filters import is_production_file
from src.models import FileChurnStats, RepoSnapshot
from src.scoring import pct, resolve_file_loc

HIGH_CHURN_THRESHOLD_PCT = 30.0


def file_churn_pct(snapshot: RepoSnapshot, filepath: str, stats: FileChurnStats) -> float:
    if not is_production_file(filepath):
        return 0.0

    total_loc = resolve_file_loc(snapshot.repo_path, filepath, stats.churn)
    risk_churn = stats.risk_churn

    if risk_churn == 0:
        return 0.0

    return pct(risk_churn, max(total_loc, 1))


def is_high_risk_module(churn_pct: float) -> bool:
    return churn_pct > HIGH_CHURN_THRESHOLD_PCT


def production_file_stats(snapshot: RepoSnapshot) -> dict[str, FileChurnStats]:
    return {
        path: stats
        for path, stats in snapshot.file_stats.items()
        if is_production_file(path)
    }
