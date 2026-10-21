$ErrorActionPreference = 'Stop'
Set-Location (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent)
$listening = Get-NetTCPConnection -State Listen -LocalPort 1880 -ErrorAction SilentlyContinue
if (-not $listening) {
    & .\.venv\Scripts\python.exe scripts\manage.py start
    if ($LASTEXITCODE -ne 0) { throw 'Dashboard startup failed; see logs/' }
}
Write-Host 'Dashboard: http://127.0.0.1:1880/dashboard/gateway'
Write-Host 'Node-RED editor: http://127.0.0.1:1880/'
