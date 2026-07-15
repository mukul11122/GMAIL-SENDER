@echo off
title Create Portable Package
echo.
echo Creating portable package (no installation needed)...
echo.

cd /d "%~dp0"

if exist "GmailStockSender_Portable" rmdir /s /q "GmailStockSender_Portable"
mkdir "GmailStockSender_Portable"

echo [1/5] Copying executable...
copy "dist\GmailStockSender.exe" "GmailStockSender_Portable\GmailStockSender.exe" >nul

echo [2/5] Creating sample customers CSV...
echo store_code,email,mobile_number > "GmailStockSender_Portable\sample_customers.csv"
echo STORE001,customer1@example.com,9876543210 >> "GmailStockSender_Portable\sample_customers.csv"
echo STORE002,customer2@example.com,9876543211 >> "GmailStockSender_Portable\sample_customers.csv"
echo STORE003,customer3@example.com,9876543212 >> "GmailStockSender_Portable\sample_customers.csv"

echo [3/5] Creating quick start guide...
(
echo ========================================
echo GMAIL STOCK EMAIL SENDER - QUICK START
echo ========================================
echo.
echo HOW TO USE:
echo.
echo STEP 1 - ADD GMAIL ACCOUNTS:
echo   1. Open GmailStockSender.exe
echo   2. Go to "Gmail Accounts" tab
echo   3. Enter your Gmail address
echo   4. Enter App Password ^(NOT regular password^)
echo      - Go to https://myaccount.google.com/
echo      - Enable 2-Step Verification
echo      - Search "App Passwords"
echo      - Create new app password for Mail
echo      - Copy the 16-character password
echo   5. Click "Add Account"
echo.
echo STEP 2 - ADD CUSTOMERS:
echo   1. Go to "Customers" tab
echo   2. Click "Upload CSV/Excel"
echo   3. Select your CSV file
echo   4. Format: store_code, email, mobile_number
echo.
echo STEP 3 - SEND EMAILS:
echo   1. Go to "Send Emails" tab
echo   2. Select Gmail account from dropdown
echo   3. Click "Select File" to attach stock file
echo   4. Click "SEND NOW"
echo.
echo DAILY LIMITS:
echo   - 450 emails per Gmail account per day
echo   - Add multiple accounts for more capacity
echo.
echo TIPS:
echo   - Gmail accounts are saved forever
echo   - Customer data is saved in database
echo   - You can track sent history
echo.
) > "GmailStockSender_Portable\QUICK_START.txt"

echo [4/5] Creating start batch file...
(
echo @echo off
echo start "" "GmailStockSender.exe"
) > "GmailStockSender_Portable\START.bat"

echo [5/5] Creating ZIP package...
powershell -Command "Compress-Archive -Path 'GmailStockSender_Portable\*' -DestinationPath 'GmailStockSender_Portable.zip' -Force"

echo.
echo ================================================
echo   PORTABLE PACKAGE CREATED!
echo ================================================
echo.
echo Package: GmailStockSender_Portable.zip
echo.
echo INSTRUCTIONS:
echo   1. Copy GmailStockSender_Portable.zip to computer
echo   2. Extract with WinRAR or right-click ^> Extract All
echo   3. Double-click GmailStockSender.exe to run
echo   4. NO INSTALLATION NEEDED!
echo.
echo ================================================
pause
