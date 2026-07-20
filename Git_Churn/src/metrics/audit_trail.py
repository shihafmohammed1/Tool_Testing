"""All Definition Coverage -> Reporting Validation -> Audit Trail Verification."""

from __future__ import annotations

from typing import Any, Dict

from src.models import RepoSnapshot
from src.scoring import metric_result, pct, score_gate


def compute_audit_trail_verification(snapshot: RepoSnapshot) -> Dict[str, Any]:
    total_commits = len(snapshot.commits)
    complete_commits = sum(1 for c in snapshot.commits if c.audit_complete)
    audit_entries = []

    for commit in snapshot.commits:
        audit_activity = commit.lines_added + commit.lines_deleted
        audit_entries.append(
            {
                "commit_hash": commit.hash[:12],
                "author": commit.author,
                "date": commit.date.isoformat(),
                "audit_activity": audit_activity,
                "files_changed": len(commit.files),
                "audit_complete": commit.audit_complete,
            }
        )

    completeness = pct(complete_commits, total_commits)
    status = score_gate(completeness, 90.0, higher_is_better=True)

    return metric_result(
        metric_id="audit_trail_verification",
        technique="All Definition Coverage",
        classification="Reporting Validation",
        metric_name="Audit Trail Verification",
        value={
            "audit_completeness_pct": completeness,
            "complete_commits": complete_commits,
            "total_commits": total_commits,
        },
        score=completeness,
        status=status,
        details={
            "formula": "audit_activity = insertions + deletions",
            "threshold": ">= 90% audit completeness",
            "audit_trail": audit_entries[:50],
        },
    )
