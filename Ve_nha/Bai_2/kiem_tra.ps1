$ErrorActionPreference = 'Stop'
Set-Location (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent)
# Includes authentication and ACL checks on isolated test brokers.
& .\.venv\Scripts\python.exe tests\integration.py
if ($LASTEXITCODE -ne 0) { throw 'MQTT verification failed; see reports/test-results.json' }
