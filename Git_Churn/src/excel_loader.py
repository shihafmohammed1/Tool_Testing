"""Load metric definitions from Excel mapping file or YAML fallback."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import yaml

# User-requested PyDriller metrics (Technique | Classification | Metric)
PYDRILLER_METRIC_ROWS = [
    {
        "id": "audit_trail_verification",
        "technique": "All Definition Coverage",
        "classification": "Reporting Validation",
        "metric": "Audit Trail Verification",
        "python_formula": "audit_activity = insertions + deletions",
    },
    {
        "id": "code_churn_score",
        "technique": "Code Churn",
        "classification": "Risk-Based Testing Prioritization",
        "metric": "Code Churn Score",
        "python_formula": "CodeChurnScore = churn / commit_count",
    },
    {
        "id": "impact_driven_verification",
        "technique": "Code Churn",
        "classification": "Regression Testing Focus",
        "metric": "Impact-Driven Verification",
        "python_formula": "ImpactDrivenVerification = churn",
    },
    {
        "id": "fault_probability_modeling",
        "technique": "Code Churn",
        "classification": "Defect Prediction",
        "metric": "Fault Probability Modeling",
        "python_formula": "FaultProbability = (added_lines + deleted_lines) / commit_count",
    },
    {
        "id": "validation_suite_updates",
        "technique": "Code Churn",
        "classification": "Test Case Maintenance Identification",
        "metric": "Validation Suite Updates",
        "python_formula": "ValidationSuiteUpdates = changed_test_files / changed_prod_files",
    },
    {
        "id": "side_effect_mapping",
        "technique": "Code Churn",
        "classification": "Change Impact Analysis",
        "metric": "Side Effect Mapping",
        "python_formula": "co_change_rate = co_changed_commits / total_commits",
    },
]


def load_yaml_config(config_path: Path) -> Dict[str, Any]:
    with config_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_excel_mapping(excel_path: Path) -> List[Dict[str, Any]]:
    """Extract PyDriller rows from the White Box sheet."""
    if not excel_path.exists():
        return PYDRILLER_METRIC_ROWS

    df = pd.read_excel(excel_path, sheet_name="White Box", header=None)
    rows: List[Dict[str, Any]] = []

    for _, row in df.iterrows():
        technique = str(row.get(2, "")).strip()
        classification = str(row.get(3, "")).strip()
        metric = str(row.get(4, "")).strip()
        tool = str(row.get(6, "")).strip().lower()

        if tool != "pydriller":
            continue

        matched = next(
            (
                item
                for item in PYDRILLER_METRIC_ROWS
                if item["technique"] == technique
                and item["classification"] == classification
                and item["metric"] == metric
            ),
            None,
        )
        if matched:
            enriched = dict(matched)
            enriched["description"] = str(row.get(5, "")).strip()
            enriched["threshold"] = str(row.get(31, "")).strip()
            enriched["score_formula"] = str(row.get(32, "")).strip()
            enriched["frequency"] = str(row.get(33, "")).strip()
            enriched["excel_formula"] = str(row.get(21, "")).strip()
            rows.append(enriched)

    return rows or PYDRILLER_METRIC_ROWS


def load_metric_definitions(
    excel_path: Optional[str] = None,
    yaml_path: Optional[str] = None,
) -> Dict[str, Any]:
    project_root = Path(__file__).resolve().parents[1]
    yaml_file = Path(yaml_path) if yaml_path else project_root / "config" / "metrics_mapping.yaml"
    config = load_yaml_config(yaml_file)

    excel_file = Path(excel_path) if excel_path else None
    metrics = load_excel_mapping(excel_file) if excel_file else config.get("metrics", PYDRILLER_METRIC_ROWS)

    return {
        "metrics": metrics,
        "defaults": config.get("defaults", {}),
        "excel_source": str(excel_file) if excel_file else None,
        "yaml_source": str(yaml_file),
    }
