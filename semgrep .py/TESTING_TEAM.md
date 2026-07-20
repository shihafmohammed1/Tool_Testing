# Testing Team Guide — Semgrep OSS + Bandit

This repo is maintained for **100/100 PASS** on all **7 Static Vulnerabilities (SAST)** metrics.

## Quick verify (must pass before submission)

```powershell
git clone https://github.com/visvantha-testable/python-tool-testing-semgrep-bandit.git
cd python-tool-testing-semgrep-bandit
python semgrep_bandit_trigger.py
python scripts/verify_semgrep_bandit_json.py --semgrep-bandit-json semgrep_bandit.json
python validate_metric_coverage.py --metrics-json semgrep_bandit_metrics.json
python -m pytest tests/ -q
```

Expected final lines:

```
TRIGGER COMPLETE: semgrep_bandit.json ready — all 7 SAST metrics covered=yes 100/100
PASS: semgrep_bandit.json has all 7 SAST metrics covered=yes with 100/100 scores
All 7 Semgrep OSS + Bandit SAST metrics are covered with 100/100 scores.
```

## Platform trigger

Use **`python semgrep_bandit_trigger.py`** on Testable (see `config/platform_trigger.json`).

## Root files the platform reads

| File | Purpose |
|------|---------|
| **`semgrep_bandit.json`** | PRIMARY unified output |
| `platform_metrics.json` | 7 integer scores |
| `sast_metric_evidence.json` | Raw parameters + formulas |
| `semgrep_bandit_metrics.json` | Full metrics payload |
| `dashboard_metrics.json` | PASS/FAIL rows |

## Expected training values

| Parameter | Expected |
|-----------|----------|
| Files scanned | ≥ 1 |
| Total findings | 0 |
| High severity | 0 |
| All 7 metric scores | 100 |

## Re-generate outputs

```powershell
python semgrep_bandit_trigger.py
```
