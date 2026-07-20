from src.repo.paths import is_remote_repo, resolve_repo_path


def test_is_remote_repo_detects_https():
    assert is_remote_repo("https://github.com/example/repo.git")


def test_resolve_local_repo():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    assert resolve_repo_path(str(root)) == str(root.resolve())
