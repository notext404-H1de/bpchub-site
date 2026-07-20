@echo off
chcp 65001 >nul
cd /d "%~dp0"

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
    echo 内容检查没有通过，已停止发布。
    pause
    exit /b 1
  )
) else (
  echo 提示：未找到 Python，本地内容检查已跳过；GitHub Actions 仍会检查。
)

set /p COMMIT_MESSAGE=请输入本次更新说明（例如 Add first skincare guide）：
if "%COMMIT_MESSAGE%"=="" set COMMIT_MESSAGE=Update BPC Hub

git add .
git commit -m "%COMMIT_MESSAGE%"
if errorlevel 1 (
  echo 没有可提交的更改，或 Git 尚未配置。
  pause
  exit /b 1
)
git push
if errorlevel 1 (
  echo 推送失败，请保存上方完整错误截图。
  pause
  exit /b 1
)

echo 推送成功，GitHub Actions 将自动构建并发布网站。
pause
