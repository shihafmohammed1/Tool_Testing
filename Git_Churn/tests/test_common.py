from src.common import load_repo_snapshot


def test_common_exports_loader():
    assert callable(load_repo_snapshot)
