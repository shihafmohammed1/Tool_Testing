# Pylint White Box Metrics Validation

Golden-reference repo for **Pylint** taxonomy and lint metric validation on branch `Python_1.1`.

## Layout

| Path | Purpose |
|------|---------|
| `src/` | ~55k LOC generated modules for KLOC density metrics |
| `tests/` | Targeted violation tests for taxonomy coverage |
| `tools/` | Pylint runner, metrics Excel, coverage audit |
| `docs/STRUCTURE.md` | Folder structure reference |

## Quick start

```bash
pip install -r requirements.txt
python run_tests.py
python tools/generate_metrics_excel.py
```

See [`taxonomy_report.md`](taxonomy_report.md) for metric coverage details.

## Subject volume

This folder **already meets** the ~50k LOC standard via `src/module_*.py`. No shared
codegen profile is required. See [`docs/STRUCTURE.md`](docs/STRUCTURE.md).
