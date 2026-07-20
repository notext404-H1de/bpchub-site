@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist "tools\hugo\hugo.exe" (
  echo 请先双击 setup_windows.bat。
  pause
  exit /b 1
)

start "" "http://localhost:1313"
"tools\hugo\hugo.exe" server --buildDrafts --disableFastRender

