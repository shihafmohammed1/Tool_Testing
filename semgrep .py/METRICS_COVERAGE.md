# Semgrep OSS + Bandit — Full Metric Coverage (7/7)

## Pipeline

```
sample_subject/  ──► bandit -r (JSON)
                ──► semgrep scan multi-config (JSON)
                         └──► semgrep_bandit_metrics.py ──► semgrep_bandit.json (7 scores)
```

## Metric matrix

| # | L4 Classification | L5 Metric | Score formula |
|---|-------------------|-----------|---------------|
| 1 | Secure Coding Validation | Best Practice Compliance | MAX(0, 100 - high×25 - medium×10 - low×3) |
| 2 | Input Validation Testing | Entry Point Sanitization | same |
| 3 | Data Flow Security Analysis | Sensitive Information Tracking | same |
| 4 | Authentication & Authorization Weakness Detection | Access Control Verification | same |
| 5 | Dependency & Library Vulnerability Detection | Supply Chain Security | same |
| 6 | Compliance & Security Standard Validation | Regulatory Alignment | same |
| 7 | Security Vulnerability Detection | Exploit Surface Identification | same |

Training subject uses **secure coding patterns** (input sanitization, parameterized queries, constant-time password compare, role checks, token masking) so Bandit + Semgrep report **0 findings** → **100/100** on all metrics.

Machine-readable mapping: `config/metric_coverage.json`

## Verification

```powershell
python semgrep_bandit_trigger.py
python scripts/verify_semgrep_bandit_json.py
python validate_metric_coverage.py --metrics-json semgrep_bandit_metrics.json
```
