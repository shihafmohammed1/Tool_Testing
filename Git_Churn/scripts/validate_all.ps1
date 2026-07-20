$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "=== Testable PyDriller - Full Validation Gate ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/3] Running pytest suite..." -ForegroundColor Yellow
python -m pytest tests/ -q
if ($LASTEXITCODE -ne 0) { throw "pytest failed" }
Write-Host "  PASSED" -ForegroundColor Green

Write-Host "[2/3] Running PyDriller metrics (strict 100/100 gate)..." -ForegroundColor Yellow
python run_metrics.py --repo "." --since 2020-01-01 --strict
if ($LASTEXITCODE -ne 0) { throw "Metrics gate failed - one or more scores below 100" }
Write-Host "  PASSED" -ForegroundColor Green

Write-Host "[3/3] Checking regression suite mapping..." -ForegroundColor Yellow
python scripts/check_regression_mapping.py
if ($LASTEXITCODE -ne 0) { throw "Regression mapping check failed" }
Write-Host "  PASSED" -ForegroundColor Green

Write-Host ""
Write-Host "ALL CHECKS PASSED - Repository ready for Testable 100/100 validation" -ForegroundColor Green
Write-Host "GitHub: https://github.com/sakthisudarshan/Pydriller (branch: main)" -ForegroundColor Cyan
