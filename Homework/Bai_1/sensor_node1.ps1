$ErrorActionPreference = 'Stop'
Set-Location (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent)
& .\.venv\Scripts\python.exe -m Ve_nha.Bai_1.sensor_simulator --node node1 @args
