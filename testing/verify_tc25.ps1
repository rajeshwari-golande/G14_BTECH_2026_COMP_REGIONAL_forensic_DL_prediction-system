# TC25 — Build: Docker image for deployment backend (exit 0, pip install in Dockerfile).
#
# Requires: Docker Desktop (or docker CLI) installed and running.
#
# Run from repo root (PowerShell):
#   .\testing\verify_tc25.ps1
#
# If you get "running scripts is disabled", either:
#   .\testing\verify_tc25.cmd
#   or: powershell -ExecutionPolicy Bypass -File .\testing\verify_tc25.ps1
#   or (once): Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
#
# Expected: docker build completes with exit code 0; final line "Successfully tagged ..." or similar.

$ErrorActionPreference = "Stop"
# testing/ -> repo root
$RepoRoot = Split-Path $PSScriptRoot -Parent
$Backend = Join-Path $RepoRoot "deployment\backend"
if (-not (Test-Path $Backend)) {
    Write-Error "Backend folder not found: $Backend"
    exit 1
}

Write-Host "TC25 - Docker build (backend)"
Write-Host "Context:" $Backend

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker CLI not found. Install Docker Desktop and ensure 'docker' is on PATH."
    exit 2
}

docker build -t forensic-backend-tc25:latest $Backend
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "PASS (exit 0)"
exit 0
