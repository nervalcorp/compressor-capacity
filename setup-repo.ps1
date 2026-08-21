<#
    First-time setup for the compressor-capacity repo.

    Run this from the folder that contains index.html:

        cd "C:\Users\JohnL\Downloads\WIDGETS-PLUGINS 4Elementor\07 Not a Widget - JUST REG HTML Files\Rated - Refrigerants and temp ranges"
        powershell -ExecutionPolicy Bypass -File .\setup-repo.ps1

    It initialises git, commits everything, points at
    github.com/nervalcorp/compressor-capacity and pushes to main.

    The repo must already exist on GitHub and be empty. Create it at
    https://github.com/organizations/nervalcorp/repositories/new
    Keep it PRIVATE while the data is provisional.
#>

$ErrorActionPreference = "Stop"
$Remote = "https://github.com/nervalcorp/compressor-capacity.git"

if (-not (Test-Path ".\index.html")) {
    Write-Host "index.html not found. Run this from the folder holding the files." -ForegroundColor Red
    exit 1
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "git is not installed or not on PATH. Get it from https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}

if (Test-Path ".\.git") {
    Write-Host "This folder is already a git repo - skipping init." -ForegroundColor Yellow
} else {
    git init
    git branch -M main
}

# point at the remote, replacing any existing one
if (git remote | Select-String -Quiet "^origin$") {
    git remote set-url origin $Remote
} else {
    git remote add origin $Remote
}

git add -A
git status --short

$msg = "Provisional capacity tables - 15 models, 5 refrigerants, 4725 rated points"
git commit -m $msg

Write-Host ""
Write-Host "Pushing to $Remote" -ForegroundColor Cyan
Write-Host "A browser or credential prompt may appear for GitHub sign-in." -ForegroundColor Cyan
git push -u origin main

Write-Host ""
Write-Host "Done. https://github.com/nervalcorp/compressor-capacity" -ForegroundColor Green
Write-Host ""
Write-Host "The data is PROVISIONAL. Only enable GitHub Pages if the repo is private" -ForegroundColor Yellow
Write-Host "or you are fine with unverified numbers being publicly reachable." -ForegroundColor Yellow
