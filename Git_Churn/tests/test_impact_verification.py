from src.metrics.impact_verification import compute_impact_driven_verification


def test_impact_driven_verification(sample_snapshot):
    result = compute_impact_driven_verification(sample_snapshot, high_churn_threshold_pct=30)
    assert result["classification"] == "Regression Testing Focus"
    assert result["score"] >= 0
