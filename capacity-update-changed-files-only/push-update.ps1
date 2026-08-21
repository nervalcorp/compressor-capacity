<#
    Commit and push whatever has changed in this folder.

        .\push-update.ps1
        .\push-update.ps1 -Message "Add URL parameters for iframe embeds"

    Use setup-repo.ps1 instead if this folder is not a git repo yet.
#>

param(
    [string]$Message = "Update capacity tables"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".\.git")) {
    Write-Host "Not a git repo yet - run setup-repo.ps1 first." -ForegroundColor Red
    exit 1
}

git fetch origin 2>$null

$changes = git status --porcelain
if (-not $changes) {
    Write-Host "Nothing to commit - the folder matches the last commit." -ForegroundColor Yellow
    exit 0
}

Write-Host "Changes to be committed:" -ForegroundColor Cyan
git status --short
Write-Host ""

git add -A
git commit -m $Message
git push

Write-Host ""
Write-Host "Pushed. https://github.com/nervalcorp/compressor-capacity" -ForegroundColor Green
