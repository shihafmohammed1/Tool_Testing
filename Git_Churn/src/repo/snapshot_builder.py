"""Build repository snapshots from PyDriller commit history."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Dict, Iterable, List, Set, Tuple

from pydriller import Repository

from src.models import CommitRecord, FileChurnStats, RepoSnapshot
from src.repo.paths import is_test_file, normalize_path, resolve_repo_path


def load_repo_snapshot(
    repo_path: str,
    since: datetime,
    to: datetime,
    test_path_patterns: Iterable[str],
    test_file_suffixes: Iterable[str],
) -> RepoSnapshot:
    repo_path = resolve_repo_path(repo_path)
    file_stats: Dict[str, FileChurnStats] = {}
    commits: List[CommitRecord] = []
    co_change_pairs: Dict[Tuple[str, str], int] = defaultdict(int)
    test_files_changed: Set[str] = set()
    prod_files_changed: Set[str] = set()
    paired_maintenance_commits: List[Dict[str, object]] = []

    repository = Repository(
        repo_path,
        since=since.replace(tzinfo=None),
        to=to.replace(tzinfo=None),
    )

    for commit in repository.traverse_commits():
        commit_files: List[str] = []
        commit_test_files: List[str] = []
        commit_prod_files: List[str] = []
        commit_added = 0
        commit_deleted = 0

        for modified in commit.modified_files:
            filepath = normalize_path(modified.filename)
            if modified.change_type.name == "DELETE":
                continue

            added = modified.added_lines or 0
            deleted = modified.deleted_lines or 0
            commit_added += added
            commit_deleted += deleted
            commit_files.append(filepath)

            stats = file_stats.setdefault(filepath, FileChurnStats(filepath=filepath))
            stats.lines_added += added
            stats.lines_deleted += deleted
            if modified.change_type.name == "ADD":
                pass
            else:
                stats.modify_lines_added += added
                stats.modify_lines_deleted += deleted
            stats.commit_count += 1
            if stats.last_modified is None or commit.committer_date > stats.last_modified:
                stats.last_modified = commit.committer_date

            if is_test_file(filepath, test_path_patterns, test_file_suffixes):
                test_files_changed.add(filepath)
                commit_test_files.append(filepath)
            else:
                prod_files_changed.add(filepath)
                commit_prod_files.append(filepath)

        unique_files = sorted(set(commit_files))
        unique_test = sorted(set(commit_test_files))
        unique_prod = sorted(set(commit_prod_files))

        if unique_test and unique_prod:
            paired_maintenance_commits.append(
                {
                    "commit_hash": commit.hash[:12],
                    "date": commit.committer_date.isoformat(),
                    "test_files": unique_test,
                    "prod_files": unique_prod,
                    "maintenance_ratio": round(len(unique_test) / len(unique_prod), 4),
                }
            )

        for i, file_a in enumerate(unique_files):
            for file_b in unique_files[i + 1 :]:
                pair = tuple(sorted((file_a, file_b)))
                co_change_pairs[pair] += 1
                file_stats[file_a].co_changed_with.add(file_b)
                file_stats[file_b].co_changed_with.add(file_a)

        audit_complete = all(
            [
                bool(commit.hash),
                bool(commit.author.name),
                bool(commit.author.email),
                bool(commit.committer_date),
                bool(commit.msg.strip()),
            ]
        )

        commits.append(
            CommitRecord(
                hash=commit.hash,
                author=commit.author.name,
                author_email=commit.author.email,
                date=commit.committer_date,
                message=commit.msg.strip(),
                files=unique_files,
                lines_added=commit_added,
                lines_deleted=commit_deleted,
                audit_complete=audit_complete,
                test_files=unique_test,
                prod_files=unique_prod,
            )
        )

    return RepoSnapshot(
        repo_path=repo_path,
        since=since,
        to=to,
        total_commits=len(commits),
        file_stats=file_stats,
        commits=commits,
        co_change_pairs=dict(co_change_pairs),
        test_files_changed=test_files_changed,
        prod_files_changed=prod_files_changed,
        paired_maintenance_commits=paired_maintenance_commits,
    )
