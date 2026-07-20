@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist "tools\hugo\hugo.exe" (
  echo 请先双击 setup_windows.bat。
  pause
  exit /b 1
)

set "PYTHON_CMD="
where py >nul 2>nul
if not errorlevel 1 set "PYTHON_CMD=py -3"
if not defined PYTHON_CMD (
  where python >nul 2>nul
  if not errorlevel 1 set "PYTHON_CMD=python"
)

if defined PYTHON_CMD (
  call %PYTHON_CMD% "scripts\check_content.py"
  if errorlevel 1 (
    echo 内容检查没有通过。
    pause
    exit /b 1
  )
) else (
  echo 提示：未找到 Python，本地内容检查已跳过；GitHub 发布时仍会自动检查。
)

"tools\hugo\hugo.exe" --gc --minify
if errorlevel 1 (
  echo Hugo 构建失败。
  pause
  exit /b 1
)

if defined PYTHON_CMD (
  call %PYTHON_CMD% "scripts\check_build.py" "public"
  if errorlevel 1 (
    echo 生成站点检查没有通过。
    pause
    exit /b 1
  )
)

echo.
echo 构建成功，静态文件位于 public 文件夹。
pause
