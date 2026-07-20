from src.scoring import churn_confidence_score, pct, stale_test_confidence_score


def test_pct_handles_zero_total():
    assert pct(0, 0) == 0.0


def test_churn_confidence_score_per_excel_formula():
    assert churn_confidence_score(0) == 100.0
    assert churn_confidence_score(25) == 50.0
    assert churn_confidence_score(50) == 0.0


def test_stale_test_confidence_score_per_excel_formula():
    assert stale_test_confidence_score(0) == 100.0
    assert stale_test_confidence_score(5) == 50.0
    assert stale_test_confidence_score(10) == 0.0
