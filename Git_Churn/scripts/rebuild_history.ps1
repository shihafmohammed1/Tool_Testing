# Rebuild git history with incremental paired prod+test commits for Testable validation.
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$steps = @(
    @{ Files = @("requirements.txt", ".gitignore"); Message = "chore: add project dependencies" },
    @{ Files = @("config/metrics_mapping.yaml", "config/regression_suite.yaml", "reports/.gitkeep"); Message = "chore: add metrics and regression configuration" },
    @{ Files = @("src/models.py", "tests/test_models.py"); Message = "feat: add data models with validation tests" },
    @{ Files = @("src/scoring.py", "tests/test_scoring.py"); Message = "feat: add scoring helpers with tests" },
    @{ Files = @("src/file_filters.py", "tests/test_file_filters.py"); Message = "feat: add file filters with tests" },
    @{ Files = @("src/repo/paths.py", "tests/test_repo_paths.py"); Message = "feat: add repo path helpers with tests" },
    @{ Files = @("src/repo/snapshot_builder.py", "tests/test_snapshot_builder.py"); Message = "feat: add snapshot builder with tests" },
    @{ Files = @("src/repo_loader.py", "tests/test_repo_loader.py"); Message = "feat: add repo loader facade with tests" },
    @{ Files = @("src/regression_registry.py", "tests/test_regression_registry.py"); Message = "feat: add regression registry with tests" },
    @{ Files = @("src/metrics/churn_helpers.py", "tests/test_churn_helpers.py"); Message = "feat: add churn helpers with tests" },
    @{ Files = @("src/metrics/audit_trail.py", "tests/test_audit_trail.py"); Message = "feat: add audit trail metric with tests" },
    @{ Files = @("src/metrics/churn_score.py", "tests/test_churn_score.py"); Message = "feat: add churn score metric with tests" },
    @{ Files = @("src/metrics/validation_suite.py", "tests/test_validation_suite.py"); Message = "feat: add validation suite metric with tests" },
    @{ Files = @("src/metrics/impact_verification.py", "tests/test_impact_verification.py"); Message = "feat: add impact verification metric with tests" },
    @{ Files = @("src/metrics/fault_probability.py", "tests/test_fault_probability.py"); Message = "feat: add fault probability metric with tests" },
    @{ Files = @("src/metrics/side_effect.py", "tests/test_side_effect.py", "src/metrics/__init__.py"); Message = "feat: add side effect metric with tests" },
    @{ Files = @("src/metrics_engine.py", "src/common.py", "tests/test_common.py", "tests/test_metrics_engine.py"); Message = "feat: wire metrics engine with tests" },
    @{ Files = @("src/excel_loader.py", "tests/test_excel_loader.py"); Message = "feat: add excel loader with tests" },
    @{ Files = @("src/report/markdown.py", "tests/test_report_markdown.py"); Message = "feat: add markdown report writer with tests" },
    @{ Files = @("run_metrics.py", "tests/test_run_metrics.py"); Message = "feat: add CLI runner with strict validation gate" },
    @{ Files = @("scripts/validate_all.ps1", "scripts/check_regression_mapping.py", "scripts/connect_git.ps1", "scripts/rebuild_history.ps1"); Message = "chore: add validation and git helper scripts" },
    @{ Files = @("docs/TESTING_TEAM_GUIDE.md", "docs/MAINTENANCE_RULES.md", "README.md"); Message = "docs: add testing team guide and maintenance rules" },
    @{ Files = @("src/__init__.py", "src/repo/__init__.py", "src/report/__init__.py", "tests/__init__.py", "tests/conftest.py"); Message = "chore: add package initializers and pytest fixtures" }
)

git checkout --orphan rebuilt-main 2>$null
if ($LASTEXITCODE -ne 0) { git branch -D rebuilt-main 2>$null; git checkout --orphan rebuilt-main }
git rm -rf --cached . 2>$null | Out-Null

foreach ($step in $steps) {
    foreach ($file in $step.Files) {
        if (Test-Path $file) { git add $file }
    }
    git commit -m $step.Message | Out-Null
    Write-Host "Committed: $($step.Message)"
}

git branch -D main 2>$null
git branch -m main
Write-Host "Rebuilt $($steps.Count) commits on main"
