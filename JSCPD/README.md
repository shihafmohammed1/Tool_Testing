# JSCPD Code Duplication Metrics Validator

Reference repository for **junior trainers** to validate **Code Duplication** metrics using [jscpd](https://github.com/kucherenko/jscpd).

This project is intentionally built with **zero copy-paste debt** — shared utilities, single-responsibility services, and reusable test helpers — so every metric should score **100/100**.

## Metrics Covered

| Objective | Metric | What JSCPD Validates |
| --- | --- | --- |
| Defect Propagation Risk Detection | Multi-Point Failure Probability | No duplicated logic blocks that could spread the same bug |
| Refactoring Identification | Redundancy Localization | No clone clusters requiring merge/refactor |
| Code Quality Assessment | Structural Cleanliness Score | 0% duplicated lines in `src/` (source code only) |
| Test Maintenance Reduction | Test Suite Streamlining | 0% duplicated lines in `tests/` (test code only) |
| Refactoring Opportunity Detection | Abstraction Potential | Common logic lives in shared modules (`src/utils/`) |
| Risk-Based Testing Prioritization | Regression Focus Mapping | No high-duplication hotspots to prioritize for regression |
| Maintainability Testing | Synchronization Verification | 0% cloned lines — no copy-paste synchronization debt |

## Quick Start (Trainer Validation Steps)

### 1. Clone and install

```bash
git clone https://github.com/sakthisudarshan/jscpd.git
cd jscpd
npm install
```

### 2. Export TESTABLE platform file (required for gate)

```bash
npm run export:testable
npm run validate:gate
```

Expected output:

```
METRICS GATE VALIDATION: PASS (100/100)
```

**Important:** TESTABLE reads `jscpd/0/jscpd.json`. Without the export step, **Code Quality Assessment** and **Test Maintenance Reduction** show **1/100 FAIL** even when code is clean.

See **[docs/TESTING_TEAM_GUIDE.md](docs/TESTING_TEAM_GUIDE.md)** for the full checklist.

### 3. Run the metrics validator

```bash
npm run validate
```

Expected output:

```
Overall Score: 100/100
Status       : PASS - Ready for trainer validation
```

### 4. Run raw JSCPD scan (optional)

```bash
npm run scan
```

Expected duplication: **0%** with **0 clones**.

### 5. Review generated report

After export, open:

- `jscpd/0/jscpd.json` — **TESTABLE platform file** (gate reads this)
- `reports/code-duplication-gate.json` — dashboard-format summary
- `reports/metrics-report.json` — trainer-friendly scorecard (100/100 per metric)

## Project Structure

```
src/
  services/     # Domain services (user, product, order)
  utils/        # Shared validation, formatting, entity helpers
tests/
  suite.test.js       # Single consolidated test suite (no cross-file duplication)
  helpers/            # Shared test utilities (DRY test setup)
scripts/
  export_testable_jscpd.js  # Writes jscpd/0/jscpd.json for TESTABLE platform
  validate_metrics_gate.js  # Verifies 100/100 platform JSON
  validate-metrics.js       # Local JSCPD scorecard
jscpd/
  0/jscpd.json              # Primary file read by TESTABLE gate
docs/
  TESTING_TEAM_GUIDE.md     # Full validation checklist for testing team
```

## Scoring Logic

The Code Duplication Gate evaluates each metric on its own scan scope:

| Metric | Scan Scope | Perfect Score (100/100) |
| --- | --- | --- |
| Code Quality Assessment | `src/` only | 0% duplicated source lines |
| Test Maintenance Reduction | `tests/` only | 0% duplicated test lines |
| All other metrics | `src/` + `tests/` | 0% duplication, 0 clones |

Gate detection uses strict settings (`minLines: 2`, `minTokens: 20`) to catch structural copy-paste patterns that default settings may miss.

## Why Code Quality & Test Maintenance Show 1/100 on TESTABLE

Two separate issues can cause **1/100 FAIL**:

1. **Missing platform file** — TESTABLE reads `jscpd/0/jscpd.json`. Without `npm run export:testable`, scoped metrics default to **1/100** (same pattern as cosmic-ray's `cosmic-ray/0/cosmic_ray.json`).
2. **Actual duplication** — These metrics scan separate directories with strict thresholds (`src/` and `tests/` only).

This repo fixes both by:
- Running `export_testable_jscpd.js` to write 0–100 integer scores to `jscpd/0/jscpd.json`
- Extracting shared service dependencies into `src/utils/serviceDeps.js` and `recordBuilder.js`
- Consolidating all tests into a single `tests/suite.test.js` file

## Trainer Checklist

- [ ] `npm install` completes without errors
- [ ] `npm test` passes all unit tests
- [ ] `npm run export:testable` writes `jscpd/0/jscpd.json`
- [ ] `npm run validate:gate` reports **PASS (100/100)**
- [ ] `StructuralCleanlinessScore` and `TestSuiteStreamlining` are **100**

## CI Validation

GitHub Actions runs automatically on push/PR:

- Unit tests
- JSCPD metrics validation (must be 100/100)
- Uploads `reports/` as artifacts for review

## Why This Repo Scores 100/100

1. **Shared abstractions** — `createEntityValidator`, `formatTimestamp`, `formatCurrency` are defined once and reused.
2. **No copy-paste services** — each service has unique domain logic.
3. **DRY tests** — common assertions live in `tests/helpers/testUtils.js`.
4. **Strict threshold** — `.jscpd.json` sets `"threshold": 0` so any future duplication fails CI.

## License

MIT
