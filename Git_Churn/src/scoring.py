"""Scoring helpers aligned to Testable Strategy Mapping v0.2."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


def parse_date(value: Optional[str], default: datetime) -> datetime:
    if not value:
        return default
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%d-%m-%Y"):
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    raise ValueError(f"Unsupported date format: {value}")


def pct(value: float, total: float) -> float:
    if total <= 0:
        return 0.0
    return round((value / total) * 100, 2)


def score_gate(value: float, gate: float, higher_is_better: bool = True) -> str:
    if higher_is_better:
        return "PASS" if value >= gate else "FAIL"
    return "PASS" if value <= gate else "FAIL"


def churn_confidence_score(churn_pct: float) -> float:
    """MAX(0, 100 - (Churn% x 2)) per Excel mapping."""
    return max(0.0, round(100 - (churn_pct * 2), 2))


def stale_test_confidence_score(stale_pct: float) -> float:
    """MAX(0, 100 - (Stale_Test% x 10)) per Excel mapping."""
    return max(0.0, round(100 - (stale_pct * 10), 2))


from src.file_filters import resolve_workspace_file


def resolve_file_loc(repo_path: str, filepath: str, fallback: int) -> int:
    candidate = resolve_workspace_file(repo_path, filepath)
    if candidate and candidate.exists():
        return max(len(candidate.read_text(encoding="utf-8", errors="ignore").splitlines()), 1)
    return max(fallback, 1)


def metric_result(
    metric_id: str,
    technique: str,
    classification: str,
    metric_name: str,
    value: Any,
    score: Optional[float] = None,
    status: str = "INFO",
    details: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "metric_id": metric_id,
        "technique": technique,
        "classification": classification,
        "metric": metric_name,
        "tool": "pydriller",
        "value": value,
        "score": score,
        "status": status,
        "details": details or {},
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
