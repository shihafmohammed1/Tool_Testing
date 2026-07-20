from pathlib import Path

from src.repo.paths import is_test_file, resolve_repo_path


def test_resolve_repo_path_for_local_repo():
    root = Path(__file__).resolve().parents[1]
    assert resolve_repo_path(str(root)) == str(root.resolve())


def test_is_test_file_suffix_detection():
    patterns = ["tests"]
    suffixes = ["_test.py"]
    assert is_test_file("tests/test_models.py", patterns, suffixes)
    assert not is_test_file("src/models.py", patterns, suffixes)
