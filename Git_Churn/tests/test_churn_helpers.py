from src.metrics.churn_helpers import file_churn_pct


def test_modification_only_churn_is_zero_for_bootstrap(sample_snapshot):
    stats = sample_snapshot.file_stats["models.py"]
    assert stats.risk_churn == 0
    assert file_churn_pct(sample_snapshot, "models.py", stats) == 0.0
