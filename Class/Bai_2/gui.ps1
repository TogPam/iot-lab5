$ErrorActionPreference = 'Stop'
Set-Location (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent)
& .\tools\mosquitto\mosquitto_pub.exe -h 127.0.0.1 -t gateway/test -m 'Hello Local MQTT'
