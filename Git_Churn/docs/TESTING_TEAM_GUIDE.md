# Testing Team Guide — Testable PyDriller Metrics (100/100 Validation)

This repository is the **official reference repo** for Testable **Development Process Analysis / Code Churn** metrics. Your testing team should use this guide before every Testable re-scan.

## Repository

- **GitHub:** https://github.com/sakthisudarshan/Pydriller
- **Branch:** `main` only
- **Tool:** PyDriller (git history analysis)

## Metrics to validate (all must be 100/100 PASS)

| Classification | Metric | Target |
|----------------|--------|--------|
| Risk-Based Testing Prioritization | Code Churn Score | 100/100 |
| Regression Testing Focus | Impact-Driven Verification | 100/100 |
| Defect Prediction | Fault Probability Modeling | 100/100 |
| Test Case Maintenance Identification | Validation Suite Updates | 100/100 |
| Change Impact Analysis | Side Effect Mapping | 100/100 |
| Reporting Validation | Audit Trail Verification | 100/100 |

## One-command local validation (run before Testable scan)

```powershell
cd f:\Testable\Pydriller
.\scripts\validate_all.ps1
```

This script runs:
1. Full pytest suite (30 tests)
2. PyDriller metrics with strict 100/100 gate
3. Regression mapping integrity check

**Expected output:** `ALL CHECKS PASSED — Repository ready for Testable 100/100 validation`

## Manual step-by-step validation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python -m pytest tests/ -v
python run_metrics.py --repo "." --since 2020-01-01 --strict
```

## What keeps this repo at 100/100

### 1. Production files stay small
- Keep every `src/` Python module **under 60 lines**
- Split large logic into new modules instead of growing existing files

### 2. Always pair tests with production changes
Every commit that changes a production file **must** change its matching test in the same commit:

| Production file | Required test file |
|-----------------|-------------------|
| `models.py` | `test_models.py` |
| `churn_score.py` | `test_churn_score.py` |
| `file_filters.py` | `test_file_filters.py` |
| *(see `config/regression_suite.yaml` for full list)* | |

### 3. Use incremental commits (not bulk commits)
- One feature = one commit with prod + test together
- Never squash the entire repo into a single commit
- Run `.\scripts\rebuild_history.ps1` only if history is corrupted

### 4. Churn risk uses modification-only changes
- File **creation** (git ADD) is not counted as high-risk churn
- Only **MODIFY** commits contribute to churn risk scoring
- This keeps maintenance commits from falsely failing metrics

### 5. Excluded from churn risk
- `__init__.py` package markers
- `conftest.py` pytest fixtures
- `config/`, `scripts/`, `README.md`

## Files your team should review

| File | Purpose |
|------|---------|
| `config/regression_suite.yaml` | Prod-to-test mapping for regression coverage |
| `config/metrics_mapping.yaml` | Metric formulas and thresholds |
| `reports/pydriller_metrics_*.md` | Latest generated validation report |
| `src/metrics/churn_helpers.py` | Churn risk calculation logic |
| `tests/` | 30 automated validation tests |

## Testable platform checklist

Before submitting to Testable, confirm:

- [ ] `validate_all.ps1` exits with code 0
- [ ] All 6 Code Churn classifications show **PASS**
- [ ] Every score shows **100/100**
- [ ] No high-risk modules listed in report
- [ ] `evidence_available: true` for Validation Suite Updates
- [ ] `regression_coverage_pct: 100` for Impact-Driven Verification
- [ ] Repo URL points to `sakthisudarshan/Pydriller` branch `main`

## If a metric drops below 100

1. Run `python run_metrics.py --repo "." --since 2020-01-01` and open the JSON report
2. Check `high_risk_modules` and `missing_modules` in the report
3. Add missing test pairings to `config/regression_suite.yaml`
4. Split any production file over 60 lines
5. Commit prod + test together, then re-run `validate_all.ps1`

## Contact / ownership

This repo is maintained for **Testable strategy validation**. Treat it as a golden reference — do not make unpaired or bulk commits without re-running the strict validation gate.
