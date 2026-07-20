from src.repo.snapshot_builder import load_repo_snapshot


def test_snapshot_builder_importable():
    assert callable(load_repo_snapshot)
