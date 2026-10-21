$ErrorActionPreference = 'Stop'
Set-Location (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent)
& .\.venv\Scripts\python.exe -m Ve_nha.Bai_1.aggregator @args
if ($LASTEXITCODE -ne 0) { throw 'Exercise failed; check broker connection and arguments.' }
