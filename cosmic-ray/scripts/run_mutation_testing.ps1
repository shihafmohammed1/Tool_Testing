#!/usr/bin/env pwsh
# Run cosmic-ray mutation testing and generate TESTABLE metrics report.

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot/..

Write-Host "==> Ensuring clean source (reset any prior mutation artifacts)"
python scripts/restore_source.py

Write-Host "==> Installing dependencies"
python -m pip install -e ".[dev]" -q

Write-Host "==> Running pytest baseline"
python -m pytest tests -q

Write-Host "==> Baseline (unmutated tests)"
cosmic-ray baseline cosmic-ray.toml

Write-Host "==> Initializing mutation session"
if (Test-Path session.sqlite) { Remove-Item session.sqlite -Force }
cosmic-ray init cosmic-ray.toml session.sqlite --force

Write-Host "==> Executing mutations (this may take several minutes)"
cosmic-ray exec cosmic-ray.toml session.sqlite

Write-Host "==> Restoring source (cosmic-ray may leave last mutant on disk)"
python scripts/restore_source.py
git diff --exit-code src/testable_demo/

Write-Host "==> Exporting TESTABLE platform JSON and reports"
python scripts/export_testable_cosmic_ray.py --fail-on-gate

Write-Host "==> Validating 100/100 mutation score gate"
python scripts/validate_metrics_gate.py --require-100

Write-Host "==> Cosmic Ray summary"
cr-rate session.sqlite
cr-report session.sqlite --surviving-only
