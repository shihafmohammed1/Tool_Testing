"""Backward-compatible exports for PyDriller metric extraction."""

from src.models import CommitRecord, FileChurnStats, RepoSnapshot
from src.repo.paths import is_remote_repo, is_test_file, resolve_repo_path
from src.repo_loader import load_repo_snapshot
from src.scoring import metric_result, parse_date, pct, score_gate

__all__ = [
    "CommitRecord",
    "FileChurnStats",
    "RepoSnapshot",
    "is_remote_repo",
    "is_test_file",
    "load_repo_snapshot",
    "resolve_repo_path",
    "metric_result",
    "parse_date",
    "pct",
    "score_gate",
]
