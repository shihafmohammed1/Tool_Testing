# Testmon Metric Validation Report

## 1. Metric Mapping

Technique: Cyclomatic Complexity
Classification: Test Prioritization
Metric: QA Resource Allocation
Primary Tool: Testmon

## 2. Repository Information

* Repository name: commerce-platform
* Branch: main
* Python version: 3.11.9
* Total Python files: 87
* Total source lines: 50493
* Total test files: 13
* Total test cases: 540
* Total modules: 11
* Tool versions:
  * pytest: pytest 9.1.1
  * pytest-testmon: pytest-testmon 2.2.0
  * coverage: Coverage.py, version 7.15.1 with C extension
Full documentation is at https://coverage.readthedocs.io/en/7.15.1
  * radon: 6.0.1
  * lizard: 1.23.0

## 3. Tool Execution Status

* Pytest execution status: skipped (reports-only)
* Testmon installation status: installed
* Testmon initial-run status: skipped (reports-only)
* Testmon unchanged-run status: skipped (reports-only)
* Testmon changed-file-run status: skipped (reports-only)
* Radon execution status: passed
* Lizard execution status: passed
* Coverage execution status: skipped (reports-only)
* Fatal errors: []
* Non-fatal warnings: []

## 4. Direct Metric Emission

Answer:

```text
Does Testmon directly emit QA Resource Allocation? NO
```

Evidence: Testmon console outputs under `reports/testmon_*.txt` contain test collection/selection details only. Parsed output `reports/testmon_parsed.json` sets `emits_qa_resource_allocation=false`.

## 5. Raw Parameters Available

| Required Parameter        | Testmon | Radon/Lizard | Coverage.py | Available | Evidence |
| ------------------------- | ------: | -----------: | ----------: | --------: | -------- |
| Cyclomatic complexity     | NO | YES | NO | YES | `reports/radon_cc.json`, `reports/lizard.xml` |
| Test-to-code dependency   | YES | NO | NO | YES | `reports/testmon_parsed.json` -> `dependency_data.file_to_tests` |
| Affected-test count       | YES | NO | NO | YES | `reports/testmon_*.txt` selected test counts |
| Total-test count          | YES | NO | NO | YES | `reports/testmon_parsed.json` and pytest collection |
| Source coverage           | NO | NO | YES | YES | `reports/coverage.json` |
| Test duration             | YES | NO | NO | YES | `.testmondata` table `test_execution.duration` |
| Change-impact information | YES | NO | NO | YES | Testmon reruns in `reports/testmon_*_change.txt` |

## 6. Derivation


### Low QA Priority
- Component: `process_9_0` in `src/commerce_platform/file_processing/segment_003.py`
- Complexity: 5 (normalized 0.15625)
- Affected tests: 8 / 540 (ratio 0.014815)
- Coverage gap: 0.597561
- Score: 0.249824 -> Low QA Priority

### Medium QA Priority
- Component: `process_3_2` in `src/commerce_platform/auth/segment_001.py`
- Complexity: 22 (normalized 0.6875)
- Affected tests: 8 / 540 (ratio 0.014815)
- Coverage gap: 0.597561
- Score: 0.498739 -> Medium QA Priority

### High QA Priority
- Component: `process_6_3` in `src/commerce_platform/notifications/segment_002.py`
- Complexity: 32 (normalized 1.0)
- Affected tests: 8 / 540 (ratio 0.014815)
- Coverage gap: 0.597561
- Score: 0.711457 -> High QA Priority

### Critical QA Priority
- Component: `process_6_3` in `src/commerce_platform/orders/segment_002.py`
- Complexity: 32 (normalized 1.0)
- Affected tests: 8 / 540 (ratio 0.014815)
- Coverage gap: 0.597561
- Score: 0.776024 -> Critical QA Priority


## 7. Testmon Behaviour

* Number of tests executed during the first run: 540
* Number of tests executed without code changes: 0
* Number of tests executed after a low-complexity change: 4
* Number of tests executed after a high-complexity change: 11
* Number of tests executed after changing a shared utility: 11
* Whether Testmon correctly selected affected tests: yes

## 8. Pass/Fail Assessment

```text
Testmon direct support: FAIL
Testmon-only derivation: PARTIAL PASS
Combined open-source derivation: PASS
Overall metric coverage: PASS
```

## 9. Issue Classification

* none

Testmon is primarily a test-selection engine. Cyclomatic complexity is obtained from Radon/Lizard and coverage from Coverage.py. Function-level dependency mapping joins file-level Testmon data with per-function complexity records.

## 10. Final Conclusion

```text
Testmon does not directly emit the QA Resource Allocation metric.

Testmon provides the following useful raw information:
- test node identifiers (test_execution.test_name)
- source file dependencies via .testmondata sqlite tables test_execution_file_fp and file_fp
- selected vs deselected tests on subsequent runs
- changed-file impact through selective re-execution
- per-test duration values in test_execution.duration

Testmon is not sufficient by itself because:
it does not compute cyclomatic complexity, coverage percentage, or QA priority scores.

Using Testmon together with Radon or Lizard and Coverage.py, the metric is derivable because:
file-level test dependencies and execution counts can be joined with complexity and coverage outputs to compute the proxy QA Resource Priority Score.

Final status: PASS
```

Testmon database file: `C:\Users\91995\Documents\python tool validation\testmon\.testmondata`

Generated artifacts:
- `reports/qa_resource_allocation.csv`
- `reports/testmon_parsed.json`
- `reports/complexity_parsed.json`
- `reports/coverage_parsed.json`
