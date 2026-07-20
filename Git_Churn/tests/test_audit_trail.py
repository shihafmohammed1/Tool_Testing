from src.metrics.audit_trail import compute_audit_trail_verification


def test_audit_trail_verification(sample_snapshot):
    result = compute_audit_trail_verification(sample_snapshot)
    assert result["score"] == 100.0
