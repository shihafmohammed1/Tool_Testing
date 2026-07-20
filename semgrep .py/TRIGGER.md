# Platform Trigger — Semgrep OSS + Bandit

## Required command on Testable

```bash
python semgrep_bandit_trigger.py
```

Or:

```bash
python -m semgrep_bandit_platform sample_subject -o semgrep_bandit.json
```

## Do NOT run alone

```bash
python -m bandit -r sample_subject
semgrep scan --config auto sample_subject
```

Raw tool output does not include the 7 derived dashboard metric scores or platform `totals` block.

## Pipeline steps

1. Install `semgrep>=1.69` and `bandit>=1.7`
2. Run Bandit JSON scan on `sample_subject/`
3. Run Semgrep OSS multi-config scan (`auto`, `p/python`, `p/owasp-top-ten`, `p/security-audit`, `p/supply-chain`)
4. Derive 7 SAST metric scores via `semgrep_bandit_metrics.py`
5. Export unified **`semgrep_bandit.json`** with platform fixup

Config: `config/platform_trigger.json`
