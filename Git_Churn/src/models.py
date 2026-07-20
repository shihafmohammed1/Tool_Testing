"""Data models for PyDriller metric extraction."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class FileChurnStats:
    filepath: str
    lines_added: int = 0
    lines_deleted: int = 0
    modify_lines_added: int = 0
    modify_lines_deleted: int = 0
    commit_count: int = 0
    last_modified: Optional[datetime] = None
    co_changed_with: Set[str] = field(default_factory=set)

    @property
    def churn(self) -> int:
        return self.lines_added + self.lines_deleted

    @property
    def risk_churn(self) -> int:
        """Churn from modifications only; file creation (ADD) is excluded from risk."""
        return self.modify_lines_added + self.modify_lines_deleted

    @property
    def fault_probability(self) -> float:
        if self.commit_count == 0:
            return 0.0
        return self.churn / self.commit_count


@dataclass
class CommitRecord:
    hash: str
    author: str
    author_email: str
    date: datetime
    message: str
    files: List[str]
    lines_added: int
    lines_deleted: int
    audit_complete: bool
    test_files: List[str] = field(default_factory=list)
    prod_files: List[str] = field(default_factory=list)


@dataclass
class RepoSnapshot:
    repo_path: str
    since: datetime
    to: datetime
    total_commits: int
    file_stats: Dict[str, FileChurnStats]
    commits: List[CommitRecord]
    co_change_pairs: Dict[Tuple[str, str], int]
    test_files_changed: Set[str]
    prod_files_changed: Set[str]
    paired_maintenance_commits: List[Dict[str, object]] = field(default_factory=list)
