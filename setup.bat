@echo off
echo ================================
echo Gmail Stock Email Sender Setup
echo ================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found!
echo.

echo Installing dependencies...
pip install -r requirements.txt --quiet

echo.
echo Deleting old database...
if exist customers.db del customers.db

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo Starting application...
python main.py

pause
