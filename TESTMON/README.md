# Commerce Platform — Testmon Metric Validation Repository

Medium-to-large Python commerce platform built to validate whether **Testmon** raw output can support derivation of the **QA Resource Allocation** metric under a cyclomatic-complexity-driven test prioritization mapping.

## Repository layout

```text
src/commerce_platform/     # ~50,000 lines of business logic
tests/                     # 500+ pytest cases with varied coverage
scripts/                   # generation, parsing, and validation automation
reports/                   # tool outputs, CSV, and validation report
```

### Core modules

- Authentication and authorization (`auth`)
- User management (`users`)
- Order processing (`orders`)
- Payment processing (`payments`)
- Inventory management (`inventory`)
- Reporting (`reporting`)
- Notification management (`notifications`)
- File processing (`file_processing`)
- Data validation (`validation`)
- Utility functions (`utils`)

## Requirements

- Python 3.10+
- Windows, Linux, or macOS

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate # Linux/macOS
pip install -r requirements.txt
python scripts/generate_codebase.py --target-lines 50000
python scripts/generate_tests.py --target-tests 520
python scripts/run_validation.py
```

## Manual execution steps

```bash
pytest -v
pytest --testmon -v
pytest --testmon -v
coverage run -m pytest
coverage json -o reports/coverage.json
coverage xml -o reports/coverage.xml
radon cc src -a -s -j > reports/radon_cc.json
lizard src -l python -o reports/lizard.xml
```

## Testmon change scenarios

The validation runner temporarily modifies:

1. `src/commerce_platform/auth/session.py` — low-complexity function
2. `src/commerce_platform/orders/pricing_engine.py` — high-complexity function
3. `src/commerce_platform/utils/shared.py` — shared utility

Each file is restored after its Testmon run.

## Testmon database

Testmon stores dependency data in `.testmondata` at the repository root. A backup copy is saved under `reports/testmon_database_backup/` after validation.

## Deliverables

- `reports/qa_resource_allocation.csv`
- `reports/testmon_metric_validation.md`
- `reports/testmon_*.txt`
- `reports/radon_cc.json`, `reports/lizard.xml`
- `reports/coverage.json`, `reports/coverage.xml`

## Metric derivation

QA Resource Priority Score combines normalized complexity (Radon/Lizard), affected-test ratio (Testmon), coverage gap (Coverage.py), and optional normalized test cost (pytest durations).

See `scripts/calculate_qa_priority.py` for the exact weighting logic.
