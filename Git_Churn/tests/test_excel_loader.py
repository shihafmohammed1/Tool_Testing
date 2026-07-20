from src.excel_loader import PYDRILLER_METRIC_ROWS, load_metric_definitions


def test_metric_definitions_loaded():
    config = load_metric_definitions()
    assert len(config["metrics"]) == len(PYDRILLER_METRIC_ROWS)
