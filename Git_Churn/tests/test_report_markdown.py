from pathlib import Path

from src.report.markdown import write_markdown_report


def test_write_markdown_report(tmp_path):
    report = {
        "repository": "demo",
        "analysis_window": {"since": "2025-01-01", "to": "2026-01-01"},
        "excel_source": None,
        "generated_at": "2026-01-01",
        "metrics": [
            {
                "technique": "Code Churn",
                "classification": "Risk-Based Testing Prioritization",
                "metric": "Code Churn Score",
                "metric_id": "code_churn_score",
                "score": 100,
                "status": "PASS",
                "details": {"formula": "demo", "threshold": "demo"},
                "value": {},
            }
        ],
    }
    output = tmp_path / "report.md"
    write_markdown_report(report, output)
    assert output.exists()
