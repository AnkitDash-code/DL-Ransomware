@echo off
REM REAL-TIME ANTIVIRUS MONITORING
REM Detects encryption as it happens and attempts auto-recovery

title Real-Time Antivirus - Active Protection
echo ==================================================
echo   REAL-TIME RANSOMWARE PROTECTION SYSTEM
echo   Monitoring: Live Behavioral Analysis
echo   Auto-Recovery: Enabled
echo ==================================================
echo Target Directory: C:\Users\Kanhaiya\System And Security\core_system\data\test_files
echo Protection Level: REAL-TIME DETECTION
echo Recovery Method: Automatic with Encryption Keys
echo ==================================================
echo.

cd /d "C:\Users\Kanhaiya\System And Security"

echo Starting real-time antivirus monitoring...
echo.

python real_time_antivirus.py

echo.
echo ==================================================
echo Real-time protection session completed
echo ==================================================
pause