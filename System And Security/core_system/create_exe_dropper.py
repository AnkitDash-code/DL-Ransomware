#!/usr/bin/env python3
"""
EXE PACKAGER FOR BACKUP ENCRYPTION DROPPER
Creates standalone executable from Python script
"""

import os
import sys
import subprocess
from pathlib import Path

def create_executable():
    """Create standalone executable using PyInstaller"""
    
    print("=" * 60)
    print("CREATING STANDALONE EXECUTABLE")
    print("=" * 60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("[FOUND] PyInstaller is available")
    except ImportError:
        print("[INSTALLING] PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Get the script path
    script_path = Path("simulators/backup_encryptor.py")
    if not script_path.exists():
        print(f"[ERROR] Script not found: {script_path}")
        return False
    
    print(f"[SOURCE] Using script: {script_path}")
    
    # Create executable
    print("[BUILDING] Creating standalone executable...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window (optional)
        "--name", "BackupFolderEncryptor",
        "--distpath", ".",  # Output to current directory
        str(script_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("[SUCCESS] Executable created successfully!")
            print("[LOCATION] Check current directory for BackupFolderEncryptor.exe")
            return True
        else:
            print(f"[ERROR] Build failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] Exception during build: {e}")
        return False

def create_simple_exe_alternative():
    """Alternative method using cx_Freeze or auto-py-to-exe"""
    print("\n" + "=" * 60)
    print("ALTERNATIVE EXE CREATION METHODS")
    print("=" * 60)
    
    print("Option 1: Using cx_Freeze")
    print("  pip install cx_Freeze")
    print("  cxfreeze simulators/backup_encryptor.py --target-dir dist")
    
    print("\nOption 2: Using auto-py-to-exe (GUI tool)")
    print("  pip install auto-py-to-exe")
    print("  auto-py-to-exe")
    
    print("\nOption 3: Manual batch wrapper (already created)")
    print("  backup_encryptor_dropper.bat")
    
    print("\nOption 4: PowerShell script (already created)")
    print("  backup_encryptor_dropper.ps1")

def main():
    """Main function"""
    print("Backup Folder Encryption Dropper - EXE Packager")
    print("Choose your preferred method:")
    print("1. Create standalone EXE using PyInstaller")
    print("2. Show alternative methods")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        create_executable()
    elif choice == "2":
        create_simple_exe_alternative()
    else:
        print("Exiting...")

if __name__ == "__main__":
    main()