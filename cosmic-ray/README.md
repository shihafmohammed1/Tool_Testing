# TESTABLE Cosmic Ray — Mutation Testing Metrics Demo

Python mutation testing repository aligned with **Testable Strategy Metrics Mapping v0.2** (White Box → Mutation Testing). Uses [cosmic-ray](https://github.com/sixty-north/cosmic-ray) to measure mutation score and validate test suite effectiveness.

**This repo is maintained at 100/100 on all seven Mutation Score gate classifications** for testing team validation.

## For the testing team

See **[docs/TESTING_TEAM_GUIDE.md](docs/TESTING_TEAM_GUIDE.md)** for the full checklist.

Quick validation:

```powershell
git clone https://github.com/sakthisudarshan/cosmic-ray.git
cd cosmic-ray
python -m pip install -e ".[dev]"
.\scripts\run_mutation_testing.ps1
```

Expected output: `METRICS GATE VALIDATION: PASS (100/100)`

| Check | Command |
|-------|---------|
| Full mutation run + export | `.\scripts\run_mutation_testing.ps1` |
| Verify 100/100 only (after run) | `python scripts\validate_metrics_gate.py --require-100` |
| Platform file to inspect | `cosmic-ray\0\cosmic_ray.json` |

## Metrics covered (7 classifications)

| Classification | Formula | Target |
|----------------|---------|--------|
| Fault Detection Capability | killed / total non-equivalent mutants | **100%** |
| Test Coverage Quality Validation | killed / (killed + survived) | **100%** |
| Test Case Improvement Identification | 0 modules with kill rate < 50% | **100%** |
| Edge Case Detection | boundary mutants killed / total boundary | **100%** |
| Regression Testing Validation | resilience score (single-run = 100%) | **100%** |
| Code Logic Validation | semantic kill rate | **100%** |
| Test Suite Effectiveness Evaluation | mutation kill rate % | **100%** |

Reference mapping: [`docs/Testable_Strategy_Metrics_Mapping_v0.2.xlsx`](docs/Testable_Strategy_Metrics_Mapping_v0.2.xlsx) (White Box sheet, rows 77–83).

## Quick start

### Prerequisites

- Python 3.10+
- Git

### Install

```powershell
python -m pip install -e ".[dev]"
```

### Run mutation testing + metrics (Windows)

```powershell
.\scripts\run_mutation_testing.ps1
```

### Run mutation testing + metrics (Linux/macOS)

```bash
chmod +x scripts/run_mutation_testing.sh
./scripts/run_mutation_testing.sh
```

## Output files

| File | Purpose |
|------|---------|
| `cosmic-ray/0/cosmic_ray.json` | **TESTABLE platform file** (taxonomy gate reads this) |
| `reports/mutation-score-gate.json` | Dashboard gate summary |
| `reports/metrics-report.json` | Full metrics detail |
| `reports/metrics-report.md` | Human-readable report |

**Important:** Without `export_testable_cosmic_ray.py`, the TESTABLE gate shows **1/100 FAIL** because only metadata is emitted.

## Project layout

```
src/testable_demo/              # Code under test
tests/                          # Pytest suite (must kill all mutants)
tests/fixtures/                 # Golden platform JSON for schema tests
scripts/
  export_testable_cosmic_ray.py # Writes cosmic-ray/0/cosmic_ray.json
  validate_metrics_gate.py      # Testing team 100/100 verifier
  metrics_reporter.py           # Metric derivation from session
  run_mutation_testing.ps1/.sh  # Full pipeline
docs/
  TESTING_TEAM_GUIDE.md         # Testing team checklist
  Testable_Strategy_Metrics_Mapping_v0.2.xlsx
.github/workflows/mutation-testing.yml
```

## GitHub CI

Every push/PR to `main` runs mutation testing and **fails unless**:

- All metric gates pass
- `validate_metrics_gate.py --require-100` passes
- Zero surviving mutants

Artifacts: **mutation-metrics-report** (includes `cosmic_ray.json`).

**Remote:** https://github.com/sakthisudarshan/cosmic-ray

## License

MIT — reference repo for TESTABLE mutation metrics validation.
