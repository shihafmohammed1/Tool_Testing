# Testing Team Guide — Mutation Score Gate (100/100)

This repository is the **reference implementation** for TESTABLE **Mutation Testing** metrics using **cosmic-ray**. Your team should use this guide to verify all seven Mutation Score classifications report **100/100 PASS**.

## Repository

| Item | Value |
|------|-------|
| GitHub | https://github.com/sakthisudarshan/cosmic-ray |
| Branch | `main` |
| Strategy mapping | `docs/Testable_Strategy_Metrics_Mapping_v0.2.xlsx` (White Box → Mutation Testing, rows 77–83) |

## Metrics to verify (7 classifications)

| # | Classification | Expected score | Gate |
|---|----------------|----------------|------|
| 1 | Fault Detection Capability | 100/100 | ≥ 70% |
| 2 | Test Coverage Quality Validation | 100/100 | ≥ 70% |
| 3 | Test Case Improvement Identification | 100/100 | 0 weak modules |
| 4 | Edge Case Detection | 100/100 | ≥ 80% |
| 5 | Regression Testing Validation | 100/100 | ≥ 95% |
| 6 | Code Logic Validation | 100/100 | ≥ 75% |
| 7 | Test Suite Effectiveness Evaluation | 100/100 | ≥ 70% |

## One-command validation (recommended)

### Windows

```powershell
git clone https://github.com/sakthisudarshan/cosmic-ray.git
cd cosmic-ray
.\scripts\run_mutation_testing.ps1
python scripts\validate_metrics_gate.py --require-100
```

### Linux / macOS

```bash
git clone https://github.com/sakthisudarshan/cosmic-ray.git
cd cosmic-ray
chmod +x scripts/run_mutation_testing.sh
./scripts/run_mutation_testing.sh
python scripts/validate_metrics_gate.py --require-100
```

**Expected final line:** `METRICS GATE VALIDATION: PASS (100/100)`

Runtime: ~5–8 minutes (mutation execution is the slow step).

## Files your review must check

| File | Purpose |
|------|---------|
| `cosmic-ray/0/cosmic_ray.json` | **Primary file** read by TESTABLE taxonomy gate |
| `reports/mutation-score-gate.json` | Dashboard-format summary |
| `reports/metrics-report.md` | Human-readable report |
| `session.sqlite` | Raw cosmic-ray session (optional deep dive) |

### Required content in `cosmic-ray/0/cosmic_ray.json`

```json
{
  "exit": 0,
  "dump_ok": true,
  "survivedMutants": 0,
  "MutationKillRatePercent": 100.0,
  "LogicErrorSensitivity": 100.0,
  "metrics": [
    { "classification": "Fault Detection Capability", "value": 100, "result": "PASS", "coverage": 100 }
  ]
}
```

**Critical:** Scores must be **0–100 integers**, not fractions like `0.88` (which displays as 1% on the gate).

## TESTABLE platform integration

When TESTABLE scans this repo, it looks for:

```text
cosmic-ray/0/cosmic_ray.json
```

After cosmic-ray completes, the export step **must** run:

```powershell
python scripts/export_testable_cosmic_ray.py
```

CI on GitHub Actions runs this automatically. If the platform runs cosmic-ray alone without export, the gate will show **1/100 FAIL** even when tests are good.

## Validation checklist

- [ ] `python -m pytest tests -q` — all tests pass
- [ ] `cosmic-ray baseline cosmic-ray.toml` — exits 0
- [ ] `cosmic-ray exec` completes with **0 surviving mutants**
- [ ] `python scripts/export_testable_cosmic_ray.py` — writes platform JSON
- [ ] `python scripts/validate_metrics_gate.py --require-100` — **PASS**
- [ ] All 7 `metrics[].result` fields equal `"PASS"`
- [ ] GitHub Actions workflow **Mutation Testing (Cosmic Ray)** is green on `main`

## CI artifacts

After each push to `main`, download artifact **mutation-metrics-report** from GitHub Actions. It contains:

- `cosmic-ray/0/cosmic_ray.json`
- `reports/mutation-score-gate.json`
- `reports/metrics-report.json`

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Gate shows **1/100** | Platform reads wrapper JSON without scores | Run `export_testable_cosmic_ray.py` |
| Gate shows **~88%** not 100% | Surviving mutants in session | Run `cr-report session.sqlite --surviving-only` and strengthen tests |
| `validate_metrics_gate` fraction warning | Scores stored as 0–1 | Re-run export script from latest `main` |
| `session already contains results` | Stale session file | Delete `session.sqlite` or use `cosmic-ray init --force` |
| Tests fail after mutation run | Mutated source left on disk | Run `python scripts/restore_source.py` |
| `git diff src/testable_demo` not empty | Source corruption | Restore from git; never commit post-mutation files |

## Do not change without re-validating

These areas directly affect the 100/100 score:

- `src/testable_demo/*.py` — code under mutation
- `tests/test_*.py` — must kill all non-equivalent mutants
- `scripts/metrics_reporter.py` — metric formulas and 0–100 scale
- `scripts/export_testable_cosmic_ray.py` — platform JSON format
- `cosmic-ray.toml` — module path and test command

## Contact / ownership

Maintained for TESTABLE white-box **Mutation Score Gate** validation.  
Reference commit on `main` should always pass `validate_metrics_gate.py --require-100`.
