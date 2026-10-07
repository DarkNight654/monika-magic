@echo off
cd /d "%~dp0"
python nhac.py
if errorlevel 1 (
    py nhac.py
)
pause