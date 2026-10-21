$ErrorActionPreference = 'Stop'
Set-Location (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent)
& .\.venv\Scripts\python.exe scripts\mqtt_cli.py pub -t gateway/command/led -m LED_ON
