from src.metrics.side_effect import compute_side_effect_mapping


def test_side_effect_mapping(sample_snapshot):
    result = compute_side_effect_mapping(sample_snapshot)
    assert result["score"] == 100.0
