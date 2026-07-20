import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

from src.models import CommitRecord, FileChurnStats, RepoSnapshot
from src.repo.paths import is_test_file


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def sample_snapshot() -> RepoSnapshot:
    since = datetime(2025, 1, 1, tzinfo=timezone.utc)
    to = datetime(2026, 7, 9, tzinfo=timezone.utc)
    file_stats = {
        "models.py": FileChurnStats("models.py", lines_added=2, commit_count=1),
        "scoring.py": FileChurnStats("scoring.py", lines_added=2, commit_count=1),
        "test_models.py": FileChurnStats("test_models.py", lines_added=2, commit_count=1),
        "test_scoring.py": FileChurnStats("test_scoring.py", lines_added=2, commit_count=1),
    }
    commits = [
        CommitRecord(
            hash="abc123",
            author="tester",
            author_email="tester@example.com",
            date=since,
            message="add models and tests",
            files=["models.py", "test_models.py"],
            lines_added=60,
            lines_deleted=0,
            audit_complete=True,
            test_files=["test_models.py"],
            prod_files=["models.py"],
        ),
        CommitRecord(
            hash="def456",
            author="tester",
            author_email="tester@example.com",
            date=to,
            message="update scoring with tests",
            files=["scoring.py", "test_scoring.py"],
            lines_added=35,
            lines_deleted=0,
            audit_complete=True,
            test_files=["test_scoring.py"],
            prod_files=["scoring.py"],
        ),
    ]
    return RepoSnapshot(
        repo_path=str(ROOT),
        since=since,
        to=to,
        total_commits=2,
        file_stats=file_stats,
        commits=commits,
        co_change_pairs={},
        test_files_changed={"test_models.py", "test_scoring.py"},
        prod_files_changed={"models.py", "scoring.py"},
        paired_maintenance_commits=[
            {
                "commit_hash": "abc123",
                    "test_files": ["test_models.py"],
                    "prod_files": ["models.py"],
                "maintenance_ratio": 1.0,
            },
            {
                "commit_hash": "def456",
                    "test_files": ["test_scoring.py"],
                    "prod_files": ["scoring.py"],
                "maintenance_ratio": 1.0,
            },
        ],
    )


def test_is_test_file_detects_tests_directory():
    assert is_test_file("test_scoring.py", ["tests"], ["_test.py"]) is True
    assert is_test_file("models.py", ["tests"], ["_test.py"]) is False
