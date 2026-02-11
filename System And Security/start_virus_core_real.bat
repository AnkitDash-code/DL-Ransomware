@echo off
REM VIRUS SIMULATOR FOR CORE SYSTEM - REAL FILE ENCRYPTION
REM Actually encrypts files in core_system/data/test_files directory
REM Uses real encryption with Fernet - ACTIVE INTERVENTION AWARE

title Virus Simulator - Core System Real Encryption
echo ==================================================
echo   REAL RANSOMWARE ATTACK - CORE SYSTEM
echo   Target: C:\Users\Kanhaiya\System And Security\core_system\data\test_files
echo   Detection: Active Intervention Monitoring
echo   Recovery: Auto-Decryption Capability
echo ==================================================
echo WARNING: This will actually encrypt real files!
echo Files will be encrypted with Fernet encryption.
echo Recovery key will be displayed for decryption.
echo ACTIVE ANTIVIRUS MAY INTERVENE AND BLOCK OPERATIONS!
echo ==================================================
echo.

cd /d "C:\Users\Kanhaiya\System And Security\core_system"

REM Check if test files exist
if not exist "data\test_files" (
    echo [ERROR] Test files directory not found!
    echo Please run setup first: python data/setup_test_files.py
    pause
    exit /b 1
)

echo Starting real file encryption attack with active antivirus awareness...
echo Target directory: data\test_files
echo.

python real_encrypt_core.py

echo.
echo ==================================================
echo REAL file encryption attempt completed!
echo Files in core_system/data\test_files were processed
echo Recovery key displayed above - SAVE IT FOR DECRYPTION
echo Active antivirus may have blocked some operations
echo ==================================================
pause