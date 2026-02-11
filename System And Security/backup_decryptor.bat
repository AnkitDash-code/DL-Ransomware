@echo off
REM BACKUP FOLDER DECRYPTION TOOL - ROOT ACCESSIBLE VERSION
REM Decrypts files in D:\Backup folder that were encrypted by backup encryptor
REM Place this script in the root directory for easy access

title Backup Folder Decryption Tool - Root Access
echo ==================================================
echo   BACKUP FOLDER DECRYPTION TOOL
echo   Decrypt Files in D:\Backup Directory
echo ==================================================
echo This tool decrypts files encrypted by the backup folder encryptor
echo Target Directory: D:\Backup
echo Extension: .backup_locked
echo ==================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found in PATH
    echo [INFO] Please install Python or ensure it's in your system PATH
    pause
    exit /b 1
)

echo [STATUS] Starting backup folder decryption...
echo [TARGET] D:\Backup
echo.

REM Run the Python decryption script from core_system
cd /d "C:\Users\Kanhaiya\System And Security\core_system"
python simulators\backup_decryptor.py

echo.
echo ==================================================
echo DECRYPTION PROCESS COMPLETE
echo ==================================================
echo.
echo Instructions:
echo 1. When prompted, enter the encryption key (base64 format)
echo 2. The key was displayed when files were encrypted
echo 3. All .backup_locked files in D:\Backup will be decrypted
echo 4. Original files will be restored with their original names
echo.
pause