# Python Tool Testing — Semgrep OSS + Bandit

Static Vulnerabilities **(SAST)** metric validation using **Semgrep OSS + Bandit**, aligned with *Testable Strategy & Metrics Reference v3.0*.

## Tool + Metrics

| Field | Value |
|-------|-------|
| **Tools** | [Semgrep OSS](https://semgrep.dev/) + [Bandit](https://bandit.readthedocs.io/) |
| **Strategy** | Security White-box Testing → Static Vulnerabilities (SAST) |
| **Metrics** | **7/7** dashboard metrics at **100/100** |
| **Training subject** | `sample_subject/` (secure Python app) |
| **GitHub repo** | https://github.com/visvantha-testable/python-tool-testing-semgrep-bandit |

## 7 SAST metrics covered

| # | L4 Classification | L5 Metric |
|---|-------------------|-----------|
| 1 | Secure Coding Validation | Best Practice Compliance |
| 2 | Input Validation Testing | Entry Point Sanitization |
| 3 | Data Flow Security Analysis | Sensitive Information Tracking |
| 4 | Authentication & Authorization Weakness Detection | Access Control Verification |
| 5 | Dependency & Library Vulnerability Detection | Supply Chain Security |
| 6 | Compliance & Security Standard Validation | Regulatory Alignment |
| 7 | Security Vulnerability Detection | Exploit Surface Identification |

## Platform trigger (REQUIRED)

```bash
python semgrep_bandit_trigger.py
```

Alternative:

```bash
python -m semgrep_bandit_platform sample_subject -o semgrep_bandit.json
```

Do **not** run raw `bandit` or `semgrep` alone without the export pipeline — the platform needs unified `semgrep_bandit.json` with all 7 metric scores.

## Primary output

**`semgrep_bandit.json`** at repository root.

Verify:

```powershell
python scripts/verify_semgrep_bandit_json.py --semgrep-bandit-json semgrep_bandit.json
python -m pytest tests/ -q
```

## Quick start

```powershell
git clone https://github.com/visvantha-testable/python-tool-testing-semgrep-bandit.git
cd python-tool-testing-semgrep-bandit
python semgrep_bandit_trigger.py
```

See **[TESTING_TEAM.md](TESTING_TEAM.md)** for QA verification steps.
