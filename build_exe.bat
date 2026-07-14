@echo off
echo ================================
echo Build Standalone Executable
echo ================================
echo.

echo Installing PyInstaller...
pip install pyinstaller --quiet

echo.
echo Building executable...
pyinstaller --onefile --windowed --name "GmailStockSender" --icon=NONE main.py

echo.
echo ================================
echo Build Complete!
echo ================================
echo.
echo Executable location: dist\GmailStockSender.exe
echo.
echo Copy GmailStockSender.exe to any Windows computer to use.
echo.

pause
