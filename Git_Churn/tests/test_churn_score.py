from src.metrics.churn_score import compute_code_churn_score


def test_code_churn_score_passes_for_low_churn_modules(sample_snapshot):
    result = compute_code_churn_score(sample_snapshot, time_window_days=30)

    assert result["classification"] == "Risk-Based Testing Prioritization"
    assert result["metric"] == "Code Churn Score"
    assert result["score"] == 100.0
    assert result["status"] == "PASS"
    assert result["value"]["high_risk_modules"] == []


def test_code_churn_score_flags_high_risk_modules(sample_snapshot):
    stats = sample_snapshot.file_stats["models.py"]
    stats.modify_lines_added = 500
    stats.modify_lines_deleted = 100
    stats.commit_count = 5

    result = compute_code_churn_score(sample_snapshot, time_window_days=30)
    assert result["value"]["high_risk_modules"]
