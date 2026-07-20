"""Regression suite registry for high-churn module coverage."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Set

import yaml

from src.file_filters import expected_test_file, file_basename, prod_has_matching_test


def load_regression_mappings(config_path: Path | None = None) -> List[Dict[str, str]]:
    path = config_path or Path(__file__).resolve().parents[1] / "config" / "regression_suite.yaml"
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return data.get("mappings", [])


def regression_test_for_prod(prod_file: str, mappings: List[Dict[str, str]]) -> str | None:
    prod_name = file_basename(prod_file)
    for item in mappings:
        mapped_prod = file_basename(item.get("prod", ""))
        if mapped_prod == prod_name:
            return file_basename(item.get("test", ""))
    return expected_test_file(prod_file)


def regression_coverage(
    prod_files: Set[str],
    changed_test_files: Set[str],
    mappings: List[Dict[str, str]] | None = None,
) -> Dict[str, object]:
    mappings = mappings or load_regression_mappings()
    changed_test_basenames = {file_basename(test) for test in changed_test_files}
    covered = []
    missing = []
    for prod in sorted(prod_files):
        mapped_test = regression_test_for_prod(prod, mappings)
        matched = mapped_test if mapped_test in changed_test_basenames else None
        if not matched:
            matched = next(
                (
                    file_basename(test)
                    for test in changed_test_files
                    if prod_has_matching_test(test, prod)
                ),
                None,
            )
        if matched:
            covered.append({"prod_file": prod, "test_file": matched})
        else:
            missing.append(prod)
    total = len(prod_files)
    pct = round((len(covered) / total) * 100, 2) if total else 100.0
    return {
        "regression_coverage_pct": pct,
        "covered_modules": covered,
        "missing_modules": missing,
    }
