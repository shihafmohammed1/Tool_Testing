# Testable White Box Metrics — Radon / Lizard (`liz2`)

Source mapping: `Testable_Strategy_Metrics_Mapping_v0.2` (White Box sheet)

| Field | Value |
|-------|-------|
| **L3 Technique** | Cyclomatic Complexity |
| **L4 Classification** | Maintainability Analysis |
| **L5 Metric** | **Technical Debt Impact** |
| **Tool** | Radon / Lizard (`randon/lizard`) |
| **Raw formula** | `technical_debt = sum(ccn_values)` |

## What Technical Debt Impact measures

It measures how likely a developer is to introduce a bug while trying to fix another one.
High complexity scores identify code that is brittle and expensive to change or support over time.

## Normalisation (from spreadsheet)

```text
Normalized CC  = average_cyclomatic_complexity / 10
Normalized NLOC = average_nloc / 200
Normalized ND  = ND / 10

Technical Debt Score =
    (Normalized CC  * 0.5)
  + (Normalized NLOC * 0.3)
  + (Normalized ND  * 0.2)
```

## Commands

```bash
pip install radon lizard

# Aggregate CCN (Technical Debt Impact primary signal)
radon cc src -a -s
lizard src -l python -C 10

# JSON / XML reports for sum(ccn_values)
radon cc src -j > lizard_metrics/radon_cc.json
lizard src -l python -o lizard_metrics/lizard_report.xml

# Optional helper (prints sum(ccn) + Technical Debt Score)
python lizard_metrics/compute_technical_debt.py src
```

## Best analysis targets in this repo

| File | Why it stresses Technical Debt Impact |
|------|----------------------------------------|
| `src/algorithms/patterns/access_control.py` | Multiple decision branches → higher CCN |
| `src/algorithms/numbers/coin_change_min.py` | DP / nested loops → CCN + nesting depth |
| `src/algorithms/strings/word_split.py` | Branchy string DP → CCN + NLOC |
| `src/algorithms/structures/linked_lists.py` | Multi-method structure → sum(ccn) across methods |

## Branch policy

This repository is **single-branch only** (`master`).
