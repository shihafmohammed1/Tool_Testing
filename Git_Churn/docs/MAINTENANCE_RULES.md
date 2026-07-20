## Testing Team — 100/100 Validation

**This repo is the golden reference for Testable Code Churn metrics.**

### Quick validation (run this first)

```powershell
.\scripts\validate_all.ps1
```

### Full guide

See [docs/TESTING_TEAM_GUIDE.md](docs/TESTING_TEAM_GUIDE.md) for:
- Complete metric checklist
- Prod-to-test pairing rules
- Maintenance guidelines
- Troubleshooting when scores drop

### Key rules for maintainers

1. **Never commit production changes without matching test changes in the same commit**
2. **Keep all `src/` modules under 60 lines** — split files if they grow
3. **Always run `--strict` gate before pushing:** `python run_metrics.py --repo "." --since 2020-01-01 --strict`
4. **Update `config/regression_suite.yaml`** when adding new production modules
