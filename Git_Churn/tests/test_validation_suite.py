from src.metrics.validation_suite import compute_validation_suite_updates


def test_validation_suite_updates_has_evidence(sample_snapshot):
    result = compute_validation_suite_updates(sample_snapshot, stale_churn_threshold_pct=20)

    assert result["classification"] == "Test Case Maintenance Identification"
    assert result["metric"] == "Validation Suite Updates"
    assert result["value"]["evidence_available"] is True
    assert result["value"]["paired_commit_count"] == 2
    assert result["value"]["changed_test_files"] == 2
    assert result["status"] == "PASS"
    assert result["score"] == 100.0


def test_validation_suite_updates_fails_without_evidence(sample_snapshot):
    sample_snapshot.test_files_changed = set()
    sample_snapshot.paired_maintenance_commits = []

    result = compute_validation_suite_updates(sample_snapshot, stale_churn_threshold_pct=20)
    assert result["value"]["evidence_available"] is False
    assert result["status"] == "FAIL"
