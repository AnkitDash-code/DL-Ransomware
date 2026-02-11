@echo off
REM FILE RECOVERY TOOL - DECRYPT ENCRYPTED FILES
REM Recovers files encrypted by the real virus scripts
REM Requires the encryption key for decryption

title File Recovery Tool - Decrypt Encrypted Files
echo ==================================================
echo   FILE RECOVERY TOOL
echo   Decrypt Files Encrypted by Ransomware Simulation
echo ==================================================
echo This tool recovers files encrypted by the virus scripts
echo You will need the encryption key to decrypt files
echo ==================================================
echo.

cd /d "C:\Users\Kanhaiya\System And Security\core_system"

echo Starting file recovery process...
echo.

python file_recovery.py

echo.
echo ==================================================
echo File recovery process completed
echo Check the results above for recovery status
echo ==================================================
pause