@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist "tools\hugo\hugo.exe" (
  echo 请先双击 setup_windows.bat。
  pause
  exit /b 1
)

echo 可用栏目：skincare、hair-care、body-care、guides
set /p SECTION=请输入栏目：
set /p SLUG=请输入英文文件名（例如 best-body-lotion-dry-skin）：

"tools\hugo\hugo.exe" new content "%SECTION%/%SLUG%.md"
if errorlevel 1 (
  echo 创建失败。
) else (
  echo 已创建 content\%SECTION%\%SLUG%.md
)
pause

