#  This folder is deployedto Railway using an account API token.
# Prerequisites:
#   Remove-Item Env:RAILWAY_TOKEN -ErrorAction SilentlyContinue
#   $env:RAILWAY_API_TOKEN="your-token"
#
# Usage (first time — get Project ID from Railway dashboard URL or `railway list`):
#   .\deploy.ps1 -ProjectId "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" -Environment production
#
# Later runs (after .railway is linked), you can omit -ProjectId/-Environment or keep them.

param(
    [string] $ProjectId,
    [string] $Environment = "production"
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not $env:RAILWAY_API_TOKEN) {
    Write-Error "RAILWAY_API_TOKEN is not set. Account tokens use RAILWAY_API_TOKEN (not RAILWAY_TOKEN). See deployment/README.md."
}

if (-not (Get-Command railway -ErrorAction SilentlyContinue) -and -not (Get-Command railway.cmd -ErrorAction SilentlyContinue)) {
    Write-Error "Railway CLI not found. Install: npm install -g @railway/cli"
}

$rw = if (Get-Command railway.cmd -ErrorAction SilentlyContinue) { "railway.cmd" } else { "railway" }

& $rw whoami

if ($ProjectId) {
    & $rw link -p $ProjectId -e $Environment
}

& $rw up --detach

Write-Host "Deploy started. Check dashboard for URL and logs."
