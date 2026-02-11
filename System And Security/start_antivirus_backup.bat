@echo off
REM START ANTIVIRUS SYSTEM - BACKUP DIRECTORY MONITORING
REM Launches antivirus guardian monitoring D:\Backup directory
REM Includes GUI dashboard for visual monitoring

title Antivirus System - Backup Directory Monitoring
echo ==================================================
echo   ZERO-DAY RANSOMWARE GUARDIAN
echo   Monitoring: D:\Backup Directory
echo ==================================================
echo Target Directory: D:\Backup
echo Log Location: C:\Users\Kanhaiya\System And Security\security_tools\monitor\behavioral_trace.log
echo Dashboard: Streamlit web interface will open in browser
echo ==================================================
echo.

REM Check if D:\Backup exists, create if not
if not exist "D:\Backup" (
    echo Creating D:\Backup directory...
    mkdir "D:\Backup" >nul 2>&1
    if exist "D:\Backup" (
        echo [SUCCESS] D:\Backup directory created
        echo Creating sample files for testing...
        
        REM Create sample files in D:\Backup
        echo This is a test document for backup encryption. > "D:\Backup\test_document.txt"
        echo Financial data backup file contents. > "D:\Backup\financial_backup.csv"
        echo System configuration backup. > "D:\Backup\system_config.json"
        echo Personal photos archive. > "D:\Backup\photos_backup.zip"
        echo Work project files backup. > "D:\Backup\project_backup.rar"
        
        echo [FILES] Created sample backup files for testing
    ) else (
        echo [WARNING] Could not create D:\Backup directory
        echo Using security_tools test directory instead...
        set "BACKUP_DIR=C:\Users\Kanhaiya\System And Security\security_tools\data\test_files"
        goto start_monitoring
    )
    set "BACKUP_DIR=D:\Backup"
) else (
    echo [INFO] D:\Backup directory already exists
    set "BACKUP_DIR=D:\Backup"
)

:start_monitoring
echo.
echo Starting guardian daemon for backup directory monitoring...
cd /d "C:\Users\Kanhaiya\System And Security\security_tools"

REM Start the guardian daemon monitoring D:\Backup
start "Antivirus Guardian - Backup" python antivirus/guardian_daemon.py

REM Wait for daemon initialization
timeout /t 3 /nobreak >nul

REM Start the GUI dashboard
echo Starting GUI Dashboard...
python antivirus/dashboard.py

echo.
echo ==================================================
echo Monitoring D:\Backup directory for ransomware activity
echo Place test files in D:\Backup to demonstrate detection
echo ==================================================
pause