@echo off
title Paytm Merchant AI Teammate - Launching...
color 0b
echo ======================================================
echo    Paytm Merchant AI Teammate - Team Cortex Code
echo    Track 3: Autonomous AI Teammates (HackBriven 2026)
echo ======================================================
echo.
echo Starting application server and opening your browser...
echo.

cd /d "%~dp0"

:: Check if python is in PATH, otherwise use the specific Python 3.14 installation
where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    python -m streamlit run app.py --server.headless false
) else (
    "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" -m streamlit run app.py --server.headless false
)

pause
