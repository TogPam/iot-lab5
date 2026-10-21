$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
& .\.venv\Scripts\python.exe scripts\manage.py start
if ($LASTEXITCODE -ne 0) { throw 'Lab startup failed; see logs/' }
