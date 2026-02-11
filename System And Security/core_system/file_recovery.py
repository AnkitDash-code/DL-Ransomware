"""
FILE RECOVERY TOOL
Recovers files encrypted by the real virus scripts
Requires the encryption key for decryption
"""

import os
import sys
from cryptography.fernet import Fernet
from pathlib import Path

class FileRecoveryTool:
    def __init__(self):
        self.supported_extensions = ['.core_encrypted', '.backup_encrypted']
        
    def recover_files(self):
        """Recover encrypted files using provided key"""
        print('=== FILE RECOVERY TOOL ===')
        print()
        
        # Get encryption key from user
        key_input = input('Enter the encryption key: ').strip()
        
        if not key_input:
            print('[ERROR] No key provided!')
            return False
            
        try:
            # Validate key format
            key_bytes = key_input.encode()
            if len(key_bytes) != 44 or not key_input.endswith('='):
                # Try to fix padding
                padding_needed = 4 - (len(key_bytes) % 4)
                if padding_needed != 4:
                    key_input = key_input + ('=' * padding_needed)
                key_bytes = key_input.encode()
            
            # Test key validity
            cipher = Fernet(key_bytes)
            test_data = b'Test decryption'
            encrypted = cipher.encrypt(test_data)
            decrypted = cipher.decrypt(encrypted)
            
            if decrypted != test_data:
                raise ValueError('Decryption test failed')
                
            print('[KEY] Valid encryption key accepted')
            print()
            
        except Exception as e:
            print(f'[ERROR] Invalid key format: {e}')
            print('Keys should be 44 characters ending with =')
            return False
        
        # Find encrypted files
        encrypted_files = self._find_encrypted_files()
        
        if not encrypted_files:
            print('[INFO] No encrypted files found to recover')
            return True
            
        print(f'[FOUND] {len(encrypted_files)} encrypted files to recover:')
        for filepath, ext in encrypted_files:
            original_name = filepath.name[:-len(ext)]
            print(f'  - {filepath.name} -> {original_name}')
        print()
        
        # Confirm recovery
        confirm = input('Proceed with file recovery? (y/N): ').strip().lower()
        if confirm != 'y':
            print('[CANCELLED] Recovery cancelled by user')
            return False
        
        # Perform recovery
        recovered_count = 0
        failed_count = 0
        
        for encrypted_path, extension in encrypted_files:
            try:
                # Read encrypted file
                with open(encrypted_path, 'rb') as f:
                    encrypted_data = f.read()
                
                # Decrypt data
                decrypted_data = cipher.decrypt(encrypted_data)
                
                # Create original filename
                original_filename = encrypted_path.name[:-len(extension)]
                original_path = encrypted_path.parent / original_filename
                
                # Write decrypted file
                with open(original_path, 'wb') as f:
                    f.write(decrypted_data)
                
                # Remove encrypted file
                encrypted_path.unlink()
                
                print(f'[RECOVERED] {encrypted_path.name} -> {original_filename}')
                recovered_count += 1
                
            except Exception as e:
                print(f'[FAILED] {encrypted_path.name}: {e}')
                failed_count += 1
        
        # Summary
        print()
        print('=' * 50)
        print('FILE RECOVERY COMPLETE')
        print('=' * 50)
        print(f'Successfully recovered: {recovered_count} files')
        print(f'Failed to recover: {failed_count} files')
        if failed_count > 0:
            print('Failed files remain encrypted - check the error messages above')
        print('=' * 50)
        
        return recovered_count > 0
    
    def _find_encrypted_files(self):
        """Find all encrypted files in common locations"""
        encrypted_files = []
        
        # Check core system test files
        core_test_dir = Path(r'C:\Users\Kanhaiya\System And Security\core_system\data\test_files')
        if core_test_dir.exists():
            for ext in self.supported_extensions:
                for file_path in core_test_dir.glob(f'*{ext}'):
                    encrypted_files.append((file_path, ext))
        
        # Check backup directory
        backup_dir = Path(r'D:\Backup')
        if backup_dir.exists():
            for ext in self.supported_extensions:
                for file_path in backup_dir.glob(f'*{ext}'):
                    encrypted_files.append((file_path, ext))
        
        return encrypted_files

# Run the recovery tool
if __name__ == "__main__":
    recovery_tool = FileRecoveryTool()
    success = recovery_tool.recover_files()

    if success:
        print('\n[SUCCESS] File recovery completed!')
    else:
        print('\n[WARNING] Some files may not have been recovered')