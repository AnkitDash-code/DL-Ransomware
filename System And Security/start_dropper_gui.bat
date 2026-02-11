@echo off
REM START GUI DROPPER CREATOR
REM Launches the Advanced Dropper Creator GUI with professional features
REM Creates PS1, BAT, and EXE droppers for educational demonstrations

title GUI Dropper Creator - Advanced Security Tool
echo ==================================================
echo   ADVANCED DROPPER CREATOR GUI
echo   Professional Security Tool for Educational Use
echo ==================================================
echo Features:
echo - Create PowerShell (.ps1) droppers
echo - Create Batch (.bat) droppers  
echo - Create Executable (.exe) droppers
echo - Pre-generated encryption keys
echo - Target directory selection
echo - Professional dropper templates
echo ==================================================
echo.

cd /d "C:\Users\Kanhaiya\System And Security\core_system"

echo Starting Advanced Dropper Creator GUI...
echo Target directory defaults to: D:\Backup
echo Output directory: Current working directory
echo.

python advanced_dropper_creator_gui.py

echo.
echo ==================================================
echo GUI dropper creator closed
echo Created droppers can be used for educational demonstrations
echo ==================================================
pause