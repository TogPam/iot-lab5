$ErrorActionPreference = 'Stop'
Set-Location (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent)
& .\.venv\Scripts\python.exe -m Tren_lop.Bai_3.check_connection @args
if ($LASTEXITCODE -ne 0) { throw 'Exercise failed; check broker connection and arguments.' }
