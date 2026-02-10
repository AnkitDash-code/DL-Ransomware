#!/usr/bin/env python3
"""
BACKUP FOLDER DECRYPTION TOOL
Decrypts files encrypted by the backup folder encryptor
"""

import os
import sys
import base64
from pathlib import Path
from cryptography.fernet import Fernet

class BackupFolderDecryptor:
    """Decrypts files in D:\Backup folder using provided key"""
    
    def __init__(self):
        self.target_directory = "D:\\Backup"
        self.encryption_extension = ".backup_locked"
        self.key = None
        
    def set_key(self, key_string):
        """Set the decryption key"""
        try:
            # Decode base64 key
            key_bytes = base64.b64decode(key_string)
            self.key = key_bytes
            return True
        except Exception as e:
            print(f"[ERROR] Invalid key format: {e}")
            return False
    
    def decrypt_backup_folder(self):
        """Decrypt all files in D:\Backup folder"""
        
        print("=" * 60)
        print("BACKUP FOLDER DECRYPTION TOOL")
        print("=" * 60)
        print(f"Target Directory: {self.target_directory}")
        print("=" * 60)
        
        # Check if target directory exists
        backup_path = Path(self.target_directory)
        if not backup_path.exists():
            print(f"[ERROR] Target directory not found: {self.target_directory}")
            return False
        
        if not self.key:
            print("[ERROR] No decryption key provided")
            return False
        
        print("[STATUS] Initializing decryption cipher...")
        try:
            cipher = Fernet(self.key)
        except Exception as e:
            print(f"[ERROR] Invalid key: {e}")
            return False
        
        print(f"[TARGET] Decrypting files in {self.target_directory}")
        
        decrypted_count = 0
        failed_count = 0
        
        # Process all encrypted files recursively
        for file_path in backup_path.rglob(f"*{self.encryption_extension}"):
            if file_path.is_file():
                try:
                    print(f"[DECRYPTING] {file_path.name}")
                    
                    # Read encrypted file content
                    with open(file_path, 'rb') as f:
                        encrypted_data = f.read()
                    
                    # Decrypt data
                    decrypted_data = cipher.decrypt(encrypted_data)
                    
                    # Write decrypted file (remove extension)
                    original_name = str(file_path)[:-len(self.encryption_extension)]
                    with open(original_name, 'wb') as f:
                        f.write(decrypted_data)
                    
                    # Remove encrypted file
                    file_path.unlink()
                    decrypted_count += 1
                    print(f"  -> Successfully decrypted")
                    
                except Exception as e:
                    print(f"  -> Failed to decrypt: {e}")
                    failed_count += 1
        
        print(f"[COMPLETE] Decryption Results:")
        print(f"  - Successfully decrypted: {decrypted_count} files")
        print(f"  - Failed to decrypt: {failed_count} files")
        
        # Remove ransom note if it exists
        note_path = backup_path / "BACKUP_ENCRYPTION_NOTICE.txt"
        if note_path.exists():
            note_path.unlink()
            print("[NOTE] Removed encryption notice file")
        
        print("=" * 60)
        print("BACKUP FOLDER DECRYPTION COMPLETE")
        print("=" * 60)
        
        return decrypted_count > 0
    
    def interactive_decrypt(self):
        """Interactive decryption with user input"""
        print("Enter the encryption key (base64 format):")
        key_input = input().strip()
        
        if not key_input:
            print("[ERROR] No key provided")
            return False
        
        if self.set_key(key_input):
            return self.decrypt_backup_folder()
        else:
            return False

def main():
    """Main execution function"""
    decryptor = BackupFolderDecryptor()
    
    # Check if key is provided as command line argument
    if len(sys.argv) > 1:
        key = sys.argv[1]
        if decryptor.set_key(key):
            decryptor.decrypt_backup_folder()
        else:
            print("Invalid key provided")
    else:
        # Interactive mode
        decryptor.interactive_decrypt()

if __name__ == "__main__":
    main()