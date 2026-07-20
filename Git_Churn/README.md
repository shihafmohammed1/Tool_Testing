# Testable PyDriller Metrics — Golden Reference Repository

Official **Testable Strategy & Metrics Mapping v0.2** reference repo for **Development Process Analysis / Code Churn** validation using [PyDriller](https://github.com/ishepard/pydriller).

**GitHub:** https://github.com/sakthisudarshan/Pydriller  
**Branch:** `main`

## For Testing Team (start here)

```powershell
.\scripts\validate_all.ps1
```

Expected: `ALL CHECKS PASSED — Repository ready for Testable 100/100 validation`

| Guide | Purpose |
|-------|---------|
| [docs/TESTING_TEAM_GUIDE.md](docs/TESTING_TEAM_GUIDE.md) | Full validation checklist for Testable re-scan |
| [docs/MAINTENANCE_RULES.md](docs/MAINTENANCE_RULES.md) | Rules to keep all metrics at 100/100 |

## Metrics (all target 100/100)

| Technique | Classification | Metric |
|-----------|----------------|--------|
| All Definition Coverage | Reporting Validation | Audit Trail Verification |
| Code Churn | Risk-Based Testing Prioritization | Code Churn Score |
| Code Churn | Regression Testing Focus | Impact-Driven Verification |
| Code Churn | Defect Prediction | Fault Probability Modeling |
| Code Churn | Test Case Maintenance Identification | Validation Suite Updates |
| Code Churn | Change Impact Analysis | Side Effect Mapping |

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python -m pytest tests/ -v
python run_metrics.py --repo "." --since 2020-01-01 --strict
```

## Project Structure

```
Pydriller/
├── config/
│   ├── metrics_mapping.yaml      # Metric formulas and thresholds
│   └── regression_suite.yaml       # Prod-to-test mapping (19 pairs)
├── docs/
│   ├── TESTING_TEAM_GUIDE.md       # Testing team validation guide
│   └── MAINTENANCE_RULES.md        # How to keep 100/100
├── scripts/
│   ├── validate_all.ps1            # One-command 100/100 gate
│   ├── connect_git.ps1             # Git remote helper
│   └── rebuild_history.ps1         # Rebuild incremental git history
├── src/
│   ├── models.py                   # Data models
│   ├── file_filters.py             # Production vs test file detection
│   ├── regression_registry.py      # Regression coverage registry
│   ├── repo/                       # PyDriller snapshot loader
│   ├── metrics/                    # Individual metric calculators
│   └── report/                     # Markdown report writer
├── tests/                          # 30 automated validation tests
└── run_metrics.py                  # CLI with --strict gate
```

## Maintenance rules (summary)

1. Pair every production change with its test in the **same commit**
2. Keep `src/` modules **under 60 lines**
3. Update `config/regression_suite.yaml` when adding new modules
4. Run `.\scripts\validate_all.ps1` before every push
5. Use modification-only churn scoring (ADD commits are not high-risk)

## Requirements

- Python 3.9+
- Git on PATH
- Target repo must have `.git` directory
