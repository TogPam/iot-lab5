$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$ProgressPreference = 'SilentlyContinue'
foreach ($folder in @('downloads','tools','logs','reports')) {
    New-Item -ItemType Directory -Force -Path $folder | Out-Null
}
if (-not (Test-Path '.venv\Scripts\python.exe')) { python -m venv .venv }
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Python dependency installation failed' }
if (-not (Test-Path 'tools\mosquitto\mosquitto.exe')) {
    Invoke-WebRequest 'https://www.7-zip.org/a/7zr.exe' -OutFile 'downloads\7zr.exe'
    Invoke-WebRequest 'https://www.7-zip.org/a/7z2600-x64.exe' -OutFile 'downloads\7z2600-x64.exe'
    Invoke-WebRequest 'https://mosquitto.org/files/binary/win64/mosquitto-2.1.2-install-windows-x64.exe' -OutFile 'downloads\mosquitto-2.1.2-install-windows-x64.exe'
    & .\downloads\7zr.exe x .\downloads\7z2600-x64.exe '-otools\7zip' -y
    if ($LASTEXITCODE -ne 0) { throw '7-Zip extraction failed' }
    & .\tools\7zip\7z.exe x .\downloads\mosquitto-2.1.2-install-windows-x64.exe '-otools\mosquitto' -y
    if ($LASTEXITCODE -ne 0) { throw 'Mosquitto extraction failed' }
}
npm.cmd ci --prefix "$PWD\node-red" --cache "$PWD\.npm-cache"
if ($LASTEXITCODE -ne 0) { throw 'Node-RED installation failed' }
& .\.venv\Scripts\python.exe scripts\prepare.py
if ($LASTEXITCODE -ne 0) { throw 'Configuration preparation failed' }
Write-Host 'Setup complete. Run: powershell -ExecutionPolicy Bypass -File scripts\start.ps1'
