from src.metrics.fault_probability import compute_fault_probability_modeling


def test_fault_probability_modeling(sample_snapshot):
    result = compute_fault_probability_modeling(sample_snapshot)
    assert result["metric"] == "Fault Probability Modeling"
    assert result["score"] == 100.0
