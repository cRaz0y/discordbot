@echo off
echo Discord Bot Setup for Windows
echo ==============================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python is installed
echo.

REM Run setup script
echo Running setup...
python setup.py

echo.
echo Setup complete! Press any key to exit...
pause >nul
