param(
    [Parameter(Mandatory = $true)]
    [string]$RemoteUrl,

    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

if (-not (Test-Path ".git")) {
    git init
    Write-Host "Initialized new git repository."
}

git add .
$status = git status --porcelain
if ($status) {
    git commit -m "Add Testable PyDriller metrics runner for strategy validation"
    Write-Host "Created initial commit."
}

$existingRemote = git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Remote 'origin' already exists: $existingRemote"
    $answer = Read-Host "Update to $RemoteUrl? (y/N)"
    if ($answer -eq "y") {
        git remote set-url origin $RemoteUrl
    }
} else {
    git remote add origin $RemoteUrl
    Write-Host "Added remote: $RemoteUrl"
}

git branch -M $Branch
Write-Host ""
Write-Host "Ready to push. Run:"
Write-Host "  git push -u origin $Branch"
Write-Host ""
Write-Host "To analyze a target repo:"
Write-Host "  python run_metrics.py --repo `"C:\path\to\your\project`""
