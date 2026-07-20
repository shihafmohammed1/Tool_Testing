"""Path and repository resolution helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


def normalize_path(path: str) -> str:
    return path.replace("\\", "/")


def is_test_file(
    filepath: str,
    test_path_patterns: Iterable[str],
    test_file_suffixes: Iterable[str],
) -> bool:
    normalized = normalize_path(filepath).lower()
    parts = normalized.split("/")
    filename = parts[-1]
    if filename.startswith("test_") or filename.startswith("test.") or filename == "conftest.py":
        return True
    if any(pattern.lower() in parts for pattern in test_path_patterns):
        return True
    return any(filename.endswith(suffix.lower()) for suffix in test_file_suffixes)


def is_remote_repo(repo_path: str) -> bool:
    lowered = repo_path.lower()
    return lowered.startswith("http://") or lowered.startswith("https://") or lowered.startswith("git@")


def resolve_repo_path(repo_path: str) -> str:
    if is_remote_repo(repo_path):
        return repo_path
    path = Path(repo_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Repository path not found: {path}")
    if not (path / ".git").exists():
        raise ValueError(f"Not a git repository: {path}")
    return str(path)
