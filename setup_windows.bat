@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo 正在安装本项目专用的 Hugo，不会修改 Windows 系统目录...
powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\install_hugo.ps1"
if errorlevel 1 (
  echo.
  echo 安装失败，请保存上方完整错误截图。
  pause
  exit /b 1
)

echo.
echo 安装完成。下一步双击 preview_windows.bat 预览网站。
pause

