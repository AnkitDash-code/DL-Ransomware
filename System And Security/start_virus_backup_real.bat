@echo off
REM VIRUS SIMULATOR FOR BACKUP DIRECTORY - REAL FILE ENCRYPTION
REM Actually encrypts files in D:\Backup directory
REM Uses real encryption with Fernet - files can be recovered with key

title Virus Simulator - Backup Directory Real Encryption
echo ==================================================
echo   REAL RANSOMWARE ATTACK - BACKUP DIRECTORY
echo   Target: D:\Backup
echo ==================================================
echo WARNING: This will actually encrypt real files!
echo Files will be encrypted with Fernet encryption.
echo Recovery key will be displayed for decryption.
echo ==================================================
echo.

REM Check if D:\Backup exists, create if not
if not exist "D:\Backup" (
    echo Creating D:\Backup directory...
    mkdir "D:\Backup" >nul 2>&1
    if exist "D:\Backup" (
        echo [SUCCESS] D:\Backup directory created
        echo Creating sample backup files for encryption...
        
        REM Create sample backup files
        echo Critical system backup data for restoration. > "D:\Backup\system_backup.dat"
        echo Financial records and accounting data backup. > "D:\Backup\financial_backup.db"
        echo Personal document archives and family records. > "D:\Backup\personal_docs.zip"
        echo Work project files and development backups. > "D:\Backup\project_backup.tar"
        echo Photo collection and media file archives. > "D:\Backup\media_backup.iso"
        
        echo [FILES] Created sample backup files for encryption demo
    ) else (
        echo [ERROR] Could not create D:\Backup directory!
        echo Please create D:\Backup manually or run start_antivirus_backup.bat first
        pause
        exit /b 1
    )
)

cd /d "C:\Users\Kanhaiya\System And Security\core_system"

echo Starting real file encryption attack on backup directory...
echo Target directory: D:\Backup
echo.

python real_encrypt_backup.py

echo.
echo ==================================================
echo REAL backup directory encryption attack completed!
echo Files in D:\Backup have been encrypted
echo Recovery key displayed above - SAVE IT FOR DECRYPTION
echo Use backup_decryptor.py to recover files
echo ==================================================
pause