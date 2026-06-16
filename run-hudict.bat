@echo off
cd /d "%~dp0"
if exist "HUDict.exe" (
  "HUDict.exe"
) else (
  ".venv\Scripts\hudict.exe"
)
