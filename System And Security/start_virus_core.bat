@echo off
REM VIRUS SIMULATOR FOR CORE SYSTEM MONITORING
REM Runs comprehensive ransomware demo against core_system test files
REM Educational purposes only

title Virus Simulator - Core System Target
echo ==================================================
echo   RANSOMWARE SIMULATOR - CORE SYSTEM
echo   Target: C:\Users\Kanhaiya\System And Security\core_system\data\test_files
echo ==================================================
echo This runs the comprehensive ransomware simulator
echo against the core system test files directory
echo Features: C2 communication, victim management, payment workflow
echo ==================================================
echo.

cd /d "C:\Users\Kanhaiya\System And Security\educational_demos"

echo Running comprehensive ransomware simulation on core system files...
echo Target directory: ..\core_system\data\test_files
echo.

python comprehensive_ransomware_simulator.py

echo.
echo ==================================================
echo Core system attack simulation completed
echo Check antivirus dashboard for detection alerts
echo ==================================================
pause