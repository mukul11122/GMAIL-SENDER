@echo off
title Create Distribution Package
echo.
echo ================================================================
echo    Creating Distribution Package for Gmail Stock Email Sender
echo ================================================================
echo.

:: Get current directory
set "CURRENT_DIR=%~dp0"
cd /d "%CURRENT_DIR%"

:: Create package folder
set "PACKAGE_DIR=%CURRENT_DIR%package"
if exist "%PACKAGE_DIR%" rmdir /s /q "%PACKAGE_DIR%"
mkdir "%PACKAGE_DIR%"

echo [1/4] Copying executable...
copy "dist\GmailStockSender.exe" "%PACKAGE_DIR%\GmailStockSender.exe" >nul

echo [2/4] Copying README...
copy "README.md" "%PACKAGE_DIR%\README.md" >nul

echo [3/4] Creating sample CSV...
(
echo email,name,company
echo customer1@example.com,John Smith,ABC Corp
echo customer2@example.com,Jane Doe,XYZ Ltd
) > "%PACKAGE_DIR%\sample_customers.csv"

echo [4/4] Copying installer...
copy "install.bat" "%PACKAGE_DIR%\install.bat" >nul

:: Create Quick Start Guide
echo Creating Quick Start Guide...
(
echo ========================================
echo GMAIL STOCK EMAIL SENDER - QUICK START
echo ========================================
echo.
echo INSTALLATION:
echo 1. Double-click "install.bat"
echo 2. Click "Yes" when asked for administrator permission
echo 3. Wait for installation to complete
echo 4. Find "Gmail Stock Sender" on your desktop
echo.
echo FIRST TIME SETUP:
echo 1. Go to Gmail Accounts tab
echo 2. Add your Gmail accounts
echo 3. Use App Passwords (NOT regular password)
echo    - Go to https://myaccount.google.com/
echo    - Enable 2-Step Verification
echo    - Create App Password for Mail
echo    - Copy 16-character password
echo.
echo ADD CUSTOMERS:
echo 1. Go to Customers tab
echo 2. Click "Upload CSV/Excel"
echo 3. CSV format: email, name, company
echo    (only email is required)
echo.
echo SEND EMAILS:
echo 1. Go to Stock Data tab - upload stock file
echo 2. Go to Send Emails tab
echo 3. Select stock file as attachment
echo 4. Click "Send Emails"
echo.
echo DAILY LIMITS:
echo - Each Gmail account: 450 emails/day
echo - Use multiple accounts for more capacity
echo.
echo SUPPORT:
echo - Check README.md for detailed instructions
echo.
) > "%PACKAGE_DIR%\QUICK_START.txt"

:: Create ZIP file using PowerShell
echo.
echo Creating ZIP package...
powershell -Command "Compress-Archive -Path '%PACKAGE_DIR%\*' -DestinationPath '%CURRENT_DIR%GmailStockSender_Package.zip' -Force"

echo.
echo ================================================================
echo    PACKAGE CREATED SUCCESSFULLY!
echo ================================================================
echo.
echo Package location: %CURRENT_DIR%GmailStockSender_Package.zip
echo.
echo Package contents:
echo - GmailStockSender.exe  ^(Main application^)
echo - install.bat            ^(Installer for Windows^)
echo - README.md              ^(Documentation^)
echo - sample_customers.csv   ^(Sample customer list^)
echo - QUICK_START.txt        ^(Quick start guide^)
echo.
echo To distribute:
echo 1. Copy "GmailStockSender_Package.zip" to USB drive
echo 2. On target computer, extract ZIP file
echo 3. Double-click "install.bat"
echo.
pause
