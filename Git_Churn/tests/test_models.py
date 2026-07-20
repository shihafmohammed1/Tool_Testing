def test_file_churn_stats_risk_churn():
    from src.models import FileChurnStats

    stats = FileChurnStats("models.py", lines_added=100, lines_deleted=20)
    stats.modify_lines_added = 15
    stats.modify_lines_deleted = 5
    assert stats.churn == 120
    assert stats.risk_churn == 20
