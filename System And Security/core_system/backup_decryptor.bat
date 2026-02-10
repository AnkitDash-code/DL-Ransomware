@echo off
cls
echo ========================================
echo    BACKUP FOLDER DECRYPTION TOOL
echo ========================================
echo Target: D:\Backup
echo ========================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found in PATH
    echo [INFO] Please install Python or run the Python script directly
    pause
    exit /b 1
)

echo [STATUS] Starting backup folder decryption...
echo [TARGET] D:\Backup

REM Run the Python decryption script
python "%~dp0simulators\backup_decryptor.py"

echo ========================================
echo DECRYPTION PROCESS COMPLETE
echo ========================================
pause