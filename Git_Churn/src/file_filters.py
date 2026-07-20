"""File classification helpers for churn and maintenance metrics."""

from __future__ import annotations

from pathlib import Path


def normalize_path(path: str) -> str:
    return path.replace("\\", "/")


def file_basename(filepath: str) -> str:
    return normalize_path(filepath).split("/")[-1]


def is_test_path(filepath: str) -> bool:
    filename = file_basename(filepath).lower()
    lowered = normalize_path(filepath).lower()
    return (
        filename.startswith("test_")
        or filename == "conftest.py"
        or "/tests/" in lowered
        or lowered.startswith("tests/")
    )


NON_PRODUCTION_FILES = {
    "__init__.py",
    "conftest.py",
    "check_regression_mapping.py",
}


def is_production_file(filepath: str) -> bool:
    lowered = normalize_path(filepath).lower()
    if file_basename(lowered) in NON_PRODUCTION_FILES:
        return False
    if is_test_path(lowered):
        return False
    if not lowered.endswith(".py"):
        return False
    if lowered.startswith("config/") or lowered.startswith("scripts/"):
        return False
    return True


def prod_basename(filepath: str) -> str:
    return file_basename(filepath)


def expected_test_file(prod_file: str) -> str:
    return f"test_{prod_basename(prod_file)}"


def prod_has_matching_test(test_file: str, prod_file: str) -> bool:
    return file_basename(test_file) == expected_test_file(prod_file)


def resolve_workspace_file(repo_path: str, filepath: str) -> Path | None:
    if repo_path.startswith("http://") or repo_path.startswith("https://"):
        return None
    root = Path(repo_path)
    normalized = normalize_path(filepath)
    basename = file_basename(normalized)
    candidates = [
        root / normalized,
        root / "src" / normalized,
        root / "tests" / normalized,
        root / "src" / "metrics" / basename,
        root / "src" / "repo" / basename,
        root / "src" / "report" / basename,
        root / basename,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    matches = list(root.rglob(basename))
    return matches[0] if matches else None
