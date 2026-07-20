from src.metrics.audit_trail import compute_audit_trail_verification
from src.metrics_engine import compute_all_metrics


def test_audit_trail_verification(sample_snapshot):
    result = compute_audit_trail_verification(sample_snapshot)
    assert result["metric"] == "Audit Trail Verification"
    assert result["score"] == 100.0


def test_compute_all_metrics_returns_six_results(sample_snapshot):
    metrics = compute_all_metrics(sample_snapshot, {"time_window_days": 30})
    assert len(metrics) == 6
    names = {item["metric"] for item in metrics}
    assert "Code Churn Score" in names
    assert "Validation Suite Updates" in names
