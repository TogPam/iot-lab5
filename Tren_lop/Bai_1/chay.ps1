$ErrorActionPreference = 'Stop'
Set-Location (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent)
& .\tools\mosquitto\mosquitto.exe -c Tren_lop\Bai_1\mosquitto.conf -v
if ($LASTEXITCODE -ne 0) { throw 'Broker failed. Stop the demo first if port 1883 is occupied.' }
