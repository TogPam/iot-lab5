$ErrorActionPreference = 'Stop'
Set-Location (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent)
& .\tools\mosquitto\mosquitto_sub.exe -h 127.0.0.1 -t gateway/test -v
