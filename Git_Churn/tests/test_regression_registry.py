from src.regression_registry import load_regression_mappings, regression_coverage


def test_regression_mappings_loaded():
    mappings = load_regression_mappings()
    assert len(mappings) >= 10


def test_regression_coverage_complete(sample_snapshot):
    prod_files = {"models.py", "scoring.py"}
    test_files = {"test_models.py", "test_scoring.py"}
    result = regression_coverage(prod_files, test_files)
    assert result["regression_coverage_pct"] == 100.0
