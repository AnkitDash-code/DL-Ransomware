@echo off
REM START ANTIVIRUS SYSTEM - CORE SYSTEM MONITORING WITH ACTIVE INTERVENTION
REM Launches antivirus guardian with active protection and GUI dashboard
REM Features real-time threat detection, automatic blocking, and recovery

title Antivirus System - Active Protection with GUI
echo ==================================================
echo   ZERO-DAY RANSOMWARE GUARDIAN + ACTIVE INTERVENTION
echo   Monitoring: Core System Test Files
echo   Protection: Real-Time Threat Blocking
echo   Recovery: Automatic File Restoration
echo ==================================================
echo Target Directory: C:\Users\Kanhaiya\System And Security\core_system\data\test_files
echo Log Location: C:\Users\Kanhaiya\System And Security\core_system\monitor\behavioral_trace.log
echo Dashboard: Streamlit web interface will open in browser
echo Protection Level: ACTIVE INTERVENTION ENABLED
echo ==================================================
echo.

cd /d "C:\Users\Kanhaiya\System And Security\core_system"

REM Copy monitor components if not present
if not exist "monitor" (
    echo Setting up monitor directory...
    xcopy "..\security_tools\monitor" "monitor\" /E /I /Y >nul
)

REM Start the ENHANCED guardian daemon with integrated active intervention
echo Starting Enhanced Guardian Daemon with Real-Time Intervention...
start "Antivirus Guardian - Core" python run.py guardian

REM Wait for daemon initialization
timeout /t 3 /nobreak >nul

REM Start the GUI dashboard
echo Starting GUI Dashboard...
python run.py dashboard

echo.
echo ==================================================
echo ANTIVIRUS SYSTEM ACTIVE
echo - Traditional behavioral monitoring: RUNNING
echo - Active intervention protection: ENABLED  
echo - GUI dashboard: AVAILABLE IN BROWSER
echo - Real-time threat blocking: ACTIVE
echo ==================================================
pause