# Repository Structure

## Subject volume (~55,000 LOC)

Pylint validation uses pre-generated modules under `src/`:

```text
src/
├── api/module_*.py
├── core/module_*.py
├── models/module_*.py
├── services/module_*.py
└── utils/module_*.py
```

This folder **already exceeds** the 50k LOC target. Do not replace these modules with
shared codegen output.

## Other paths

| Path | Purpose |
|------|---------|
| `tests/` | Taxonomy violation tests |
| `tools/` | Metrics and audit scripts |
| `plugins/` | Pylint plugin configuration |

See [`docs/REPO_LAYOUT.md`](../../docs/REPO_LAYOUT.md) at repo root.
