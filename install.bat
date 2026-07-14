@echo off
title Gmail Stock Email Sender - Installer
color 1F
echo.
echo  ================================================================
echo        GMAIL STOCK EMAIL SENDER - WINDOWS INSTALLER
echo  ================================================================
echo.
echo  This will install the application on your computer.
echo.
echo  Press any key to start installation...
pause >nul
echo.

:: Check for admin rights
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo  Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Set installation directory
set "INSTALL_DIR=%ProgramFiles%\GmailStockSender"
set "DESKTOP_DIR=%PUBLIC%\Desktop"
set "STARTMENU_DIR=%ProgramData%\Microsoft\Windows\Start Menu\Programs\Gmail Stock Sender"

echo  Installing to: %INSTALL_DIR%
echo.

:: Create directories
echo  Creating directories...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%STARTMENU_DIR%" mkdir "%STARTMENU_DIR%"

:: Copy executable
echo  Copying application files...
copy /Y "GmailStockSender.exe" "%INSTALL_DIR%\GmailStockSender.exe" >nul
copy /Y "README.md" "%INSTALL_DIR%\README.md" >nul 2>&1

:: Create sample CSV file
echo  Creating sample customer CSV...
echo email,name,company > "%INSTALL_DIR%\sample_customers.csv"
echo customer1@example.com,John Smith,ABC Corp >> "%INSTALL_DIR%\sample_customers.csv"
echo customer2@example.com,Jane Doe,XYZ Ltd >> "%INSTALL_DIR%\sample_customers.csv"

:: Create uninstaller
echo  Creating uninstaller...
(
echo @echo off
echo title Uninstall Gmail Stock Email Sender
echo echo.
echo echo  This will remove Gmail Stock Email Sender from your computer.
echo echo.
echo set /p CONFIRM="Are you sure you want to uninstall? (Y/N): "
echo if /i not "%%CONFIRM%%"=="Y" exit /b
echo echo.
echo echo  Uninstalling...
echo if exist "%INSTALL_DIR%" rmdir /s /q "%INSTALL_DIR%"
echo if exist "%DESKTOP_DIR%\Gmail Stock Sender.lnk" del "%DESKTOP_DIR%\Gmail Stock Sender.lnk"
echo if exist "%STARTMENU_DIR%" rmdir /s /q "%STARTMENU_DIR%"
echo echo.
echo echo  Uninstallation complete!
echo pause
) > "%INSTALL_DIR%\uninstall.bat"

:: Create desktop shortcut
echo  Creating desktop shortcut...
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESKTOP_DIR%\Gmail Stock Sender.lnk'); $s.TargetPath = '%INSTALL_DIR%\GmailStockSender.exe'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Description = 'Gmail Stock Email Sender'; $s.Save()"

:: Create start menu shortcut
echo  Creating start menu shortcut...
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%STARTMENU_DIR%\Gmail Stock Sender.lnk'); $s.TargetPath = '%INSTALL_DIR%\GmailStockSender.exe'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Description = 'Gmail Stock Email Sender'; $s.Save()"

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%STARTMENU_DIR%\Uninstall.lnk'); $s.TargetPath = '%INSTALL_DIR%\uninstall.bat'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Description = 'Uninstall'; $s.Save()"

:: Create registry entries
echo  Creating registry entries...
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\GmailStockSender" /v "DisplayName" /t REG_SZ /d "Gmail Stock Email Sender" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\GmailStockSender" /v "DisplayIcon" /t REG_SZ /d "%INSTALL_DIR%\GmailStockSender.exe" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\GmailStockSender" /v "UninstallString" /t REG_SZ /d "%INSTALL_DIR%\uninstall.bat" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\GmailStockSender" /v "InstallLocation" /t REG_SZ /d "%INSTALL_DIR%" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\GmailStockSender" /v "Publisher" /t REG_SZ /d "GmailStockSender" /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\GmailStockSender" /v "NoModify" /t REG_DWORD /d 1 /f >nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\GmailStockSender" /v "NoRepair" /t REG_DWORD /d 1 /f >nul

echo.
echo  ================================================================
echo        INSTALLATION COMPLETE!
echo  ================================================================
echo.
echo  The application has been installed to:
echo  %INSTALL_DIR%
echo.
echo  A desktop shortcut has been created.
echo.
echo  To start the application:
echo  - Double-click "Gmail Stock Sender" on your desktop
echo  - OR go to Start Menu ^> Gmail Stock Sender
echo.
echo  Sample CSV file location:
echo  %INSTALL_DIR%\sample_customers.csv
echo.
echo  To uninstall:
echo  - Go to Control Panel ^> Programs ^> Uninstall a program
echo  - OR use the uninstaller in Start Menu
echo.
echo  ================================================================
echo.
pause

:: Ask to launch
set /p LAUNCH="Would you like to launch the application now? (Y/N): "
if /i "%LAUNCH%"=="Y" (
    start "" "%INSTALL_DIR%\GmailStockSender.exe"
)

exit /b
