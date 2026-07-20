# Testing Team Guide — Code Duplication Gate (100/100)

This repository is the **reference implementation** for TESTABLE **Code Duplication** metrics using **jscpd**. Your team should use this guide to verify all seven Code Duplication classifications report **100/100 PASS**.

## Repository

| Item | Value |
|------|-------|
| GitHub | https://github.com/sakthisudarshan/jscpd |
| Branch | `main` |
| Tool | jscpd |

## Metrics to verify (7 classifications)

| # | Classification | Expected score | Scan scope |
|---|----------------|----------------|------------|
| 1 | Defect Propagation Risk Detection | 100/100 | `src/` + `tests/` |
| 2 | Refactoring Identification | 100/100 | `src/` + `tests/` |
| 3 | **Code Quality Assessment** | **100/100** | **`src/` only** |
| 4 | **Test Maintenance Reduction** | **100/100** | **`tests/` only** |
| 5 | Refactoring Opportunity Detection | 100/100 | `src/` + `tests/` |
| 6 | Risk-Based Testing Prioritization | 100/100 | `src/` + `tests/` |
| 7 | Maintainability Testing | 100/100 | `src/` + `tests/` |

## One-command validation (recommended)

```powershell
git clone https://github.com/sakthisudarshan/jscpd.git
cd jscpd
npm install
npm run export:testable
npm run validate:gate
```

**Expected final line:** `METRICS GATE VALIDATION: PASS (100/100)`

## Files your review must check

| File | Purpose |
|------|---------|
| `jscpd/0/jscpd.json` | **Primary file** read by TESTABLE taxonomy gate |
| `reports/code-duplication-gate.json` | Dashboard-format summary |
| `reports/metrics-report.json` | Full metrics detail |

### Required content in `jscpd/0/jscpd.json`

```json
{
  "exit": 0,
  "scan_ok": true,
  "StructuralCleanlinessScore": 100,
  "TestSuiteStreamlining": 100,
  "metrics": [
    { "classification": "Code Quality Assessment", "value": 100, "result": "PASS", "coverage": 100 },
    { "classification": "Test Maintenance Reduction", "value": 100, "result": "PASS", "coverage": 100 }
  ]
}
```

**Critical:** Scores must be **0–100 integers**, not fractions like `0.88` (which displays as **1/100 FAIL** on the gate).

## TESTABLE platform integration

When TESTABLE scans this repo, it looks for:

```text
jscpd/0/jscpd.json
```

After jscpd analysis completes, the export step **must** run:

```powershell
npm run export:testable
```

If the platform runs jscpd alone without export, **Code Quality Assessment** and **Test Maintenance Reduction** will show **1/100 FAIL** even when the code is clean.

## Validation checklist

- [ ] `npm install` completes without errors
- [ ] `npm test` passes all unit tests
- [ ] `npm run export:testable` writes `jscpd/0/jscpd.json`
- [ ] `npm run validate:gate` reports **PASS (100/100)**
- [ ] `StructuralCleanlinessScore` equals **100**
- [ ] `TestSuiteStreamlining` equals **100**
- [ ] All 7 `metrics[].result` fields equal `"PASS"`
- [ ] GitHub Actions workflow **JSCPD Metrics Validation** is green on `main`

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Gate shows **1/100** on Code Quality or Test Maintenance | Platform reads wrapper JSON without 0–100 scores | Run `npm run export:testable` |
| Gate shows **~99%** not 100% | Duplication detected in `src/` or `tests/` | Run strict scan: `npx jscpd src --min-lines 2 --min-tokens 20` |
| `validate:gate` fraction warning | Scores stored as 0–1 | Re-run export script from latest `main` |
| 5 metrics pass, 2 fail | Missing platform keys for scoped metrics | Ensure `jscpd/0/jscpd.json` exists with all 7 classifications |

## Do not change without re-validating

These areas directly affect the 100/100 score:

- `src/` — must have 0% duplication under strict scan
- `tests/` — must have 0% duplication under strict scan
- `scripts/export_testable_jscpd.js` — platform JSON format
- `scripts/metrics-utils.js` — metric formulas and 0–100 scale
- `jscpd/0/jscpd.json` — TESTABLE platform file

## Contact / ownership

Maintained for TESTABLE white-box **Code Duplication Gate** validation.  
Reference commit on `main` should always pass `npm run validate:gate`.
