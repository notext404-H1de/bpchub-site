$ErrorActionPreference = "Stop"

$Version = "0.164.0"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$InstallDir = Join-Path $ProjectRoot "tools\hugo"
$ZipPath = Join-Path $env:TEMP "hugo_extended_$Version.zip"
$DownloadUrl = "https://github.com/gohugoio/hugo/releases/download/v$Version/hugo_extended_${Version}_windows-amd64.zip"

if (Test-Path (Join-Path $InstallDir "hugo.exe")) {
    Write-Host "Hugo is already installed locally."
    & (Join-Path $InstallDir "hugo.exe") version
    exit 0
}

Write-Host "Downloading Hugo Extended $Version from the official release..."
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
Invoke-WebRequest -Uri $DownloadUrl -OutFile $ZipPath
Expand-Archive -Path $ZipPath -DestinationPath $InstallDir -Force
Remove-Item $ZipPath -Force

Write-Host "Hugo installation completed:"
& (Join-Path $InstallDir "hugo.exe") version

