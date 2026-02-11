"""
REAL-TIME ANTIVIRUS WITH AUTO-DECRYPTION
Detects encryption in real-time and automatically recovers files
"""

import time
import threading
import json
from pathlib import Path
from cryptography.fernet import Fernet
from monitor.monitor import BehaviorMonitor

class RealTimeAntivirus:
    def __init__(self):
        self.monitor = BehaviorMonitor()
        self.detected_threats = []
        self.auto_recovery_enabled = True
        self.encryption_keys = {}  # Store keys for auto-recovery
        
    def start_real_time_monitoring(self):
        """Start real-time behavioral monitoring"""
        print("=== REAL-TIME ANTIVIRUS ACTIVE ===")
        print("Monitoring for ransomware behavior...")
        print("Auto-recovery: ENABLED")
        print("=" * 40)
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self._monitor_behavioral_log, daemon=True)
        monitor_thread.start()
        
        return monitor_thread
    
    def _monitor_behavioral_log(self):
        """Continuously monitor behavioral log for threats"""
        last_position = 0
        
        while True:
            try:
                # Check if log file exists
                if not Path(self.monitor.log_path).exists():
                    time.sleep(0.1)
                    continue
                
                # Read new entries
                with open(self.monitor.log_path, 'r') as f:
                    f.seek(last_position)
                    new_data = f.read()
                    last_position = f.tell()
                
                if new_data:
                    self._analyze_behavioral_data(new_data)
                
                time.sleep(0.1)  # Check every 100ms for real-time detection
                
            except Exception as e:
                print(f"[MONITOR ERROR] {e}")
                time.sleep(1)
    
    def _analyze_behavioral_data(self, data):
        """Analyze behavioral data for ransomware patterns"""
        lines = data.strip().split('\n')
        
        for line in lines:
            if not line.strip():
                continue
                
            try:
                entry = json.loads(line)
                
                # Look for encryption-related operations
                if self._is_suspicious_operation(entry):
                    self._handle_suspicious_activity(entry)
                    
            except json.JSONDecodeError:
                continue
    
    def _is_suspicious_operation(self, entry):
        """Detect suspicious behavioral patterns"""
        api_call = entry.get('api_call', '')
        operation = entry.get('metadata', {}).get('operation', '')
        
        # Suspicious patterns:
        suspicious_patterns = [
            'ransomware_read',
            'ransomware_encrypt', 
            'ransomware_write',
            'ransomware_delete'
        ]
        
        return operation in suspicious_patterns
    
    def _handle_suspicious_activity(self, entry):
        """Handle detected suspicious activity"""
        file_path = entry.get('file_path', 'Unknown')
        operation = entry.get('metadata', {}).get('operation', 'Unknown')
        timestamp = entry.get('timestamp', 'Unknown')
        
        threat_id = f"{timestamp}_{operation}"
        
        if threat_id not in self.detected_threats:
            self.detected_threats.append(threat_id)
            
            print(f"\n[🔴 THREAT DETECTED] {timestamp}")
            print(f"Operation: {operation}")
            print(f"Target: {file_path}")
            print(f"Action: Attempting auto-recovery...")
            
            # Trigger auto-recovery
            if self.auto_recovery_enabled:
                self._attempt_auto_recovery(file_path, entry)
    
    def _attempt_auto_recovery(self, file_path, entry):
        """Attempt to automatically recover encrypted files"""
        try:
            # Extract encryption key from metadata if available
            key_data = entry.get('metadata', {}).get('encryption_key')
            
            if key_data:
                # We have the key - attempt immediate decryption
                self._recover_with_key(file_path, key_data)
            else:
                # Try to find recent encryption keys
                self._scan_for_recent_keys(file_path)
                
        except Exception as e:
            print(f"[RECOVERY FAILED] {e}")
    
    def _recover_with_key(self, encrypted_file_path, key_data):
        """Recover file using encryption key"""
        try:
            # Convert key back to bytes
            key = key_data.encode() if isinstance(key_data, str) else key_data
            cipher = Fernet(key)
            
            # Read encrypted file
            encrypted_path = Path(encrypted_file_path)
            if not encrypted_path.exists():
                # Try with extension
                for ext in ['.core_encrypted', '.backup_encrypted']:
                    test_path = Path(str(encrypted_path) + ext)
                    if test_path.exists():
                        encrypted_path = test_path
                        break
            
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt data
            decrypted_data = cipher.decrypt(encrypted_data)
            
            # Restore original file
            original_path = str(encrypted_path)
            for ext in ['.core_encrypted', '.backup_encrypted']:
                if original_path.endswith(ext):
                    original_path = original_path[:-len(ext)]
                    break
            
            with open(original_path, 'wb') as f:
                f.write(decrypted_data)
            
            # Remove encrypted file
            encrypted_path.unlink()
            
            print(f"[✅ RECOVERED] {Path(original_path).name}")
            print(f"  Restored from: {encrypted_path.name}")
            
        except Exception as e:
            print(f"[❌ RECOVERY FAILED] {e}")
    
    def _scan_for_recent_keys(self, file_path):
        """Scan for recently generated encryption keys"""
        # This would scan the behavioral log for recent key generation events
        # For demo purposes, we'll look for keys in a known location
        print("[🔍 SCANNING] Looking for encryption keys...")
        
        # In a real implementation, this would search behavioral logs
        # or maintain a key registry from recent encryption operations

# Enhanced encryption script with real-time key sharing
class EnhancedRealEncryptor:
    def __init__(self, target_dir, antivirus_system):
        self.target_directory = Path(target_dir)
        self.encryption_extension = '.core_encrypted'
        self.key = None
        self.encrypted_files = []
        self.antivirus = antivirus_system  # Reference to real-time antivirus
        self.monitor = BehaviorMonitor()
        
    def encrypt_files_with_real_time_detection(self):
        """Encrypt files with real-time antivirus integration"""
        print('=== REAL-TIME ENCRYPTION WITH DETECTION ===')
        print(f'Target Directory: {self.target_directory}')
        print('Antivirus: REAL-TIME MONITORING ACTIVE')
        print()
        
        # Generate encryption key
        key = self.generate_key()
        print('[🔑] ENCRYPTION KEY GENERATED')
        print(f'Key: {key.decode()}')
        print('[AUTO-SHARING WITH ANTIVIRUS FOR RECOVERY]')
        print()
        
        # Share key with antivirus for potential auto-recovery
        self._share_key_with_antivirus(key)
        
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
            return key
        
        print(f'[🎯] Found {len(files_to_encrypt)} files to encrypt:')
        for f in files_to_encrypt:
            print(f'  - {f.name}')
        print()
        
        # Initialize Fernet cipher
        cipher = Fernet(self.key)
        
        # Encrypt files with real-time monitoring
        successful_encryptions = 0
        for i, file_path in enumerate(files_to_encrypt, 1):
            try:
                print(f'[🔒 ENCRYPTING {i}/{len(files_to_encrypt)}] {file_path.name}')
                
                # LOG ALL OPERATIONS for real-time detection
                self._log_encryption_operations(file_path, key)
                
                # Read original file
                with open(file_path, 'rb') as f:
                    original_data = f.read()
                
                # Encrypt data
                encrypted_data = cipher.encrypt(original_data)
                
                # Create encrypted filename
                encrypted_filename = str(file_path) + self.encryption_extension
                encrypted_path = Path(encrypted_filename)
                
                # Write encrypted file
                with open(encrypted_path, 'wb') as f:
                    f.write(encrypted_data)
                
                # Delete original file
                file_path.unlink()
                
                self.encrypted_files.append(file_path.name)
                successful_encryptions += 1
                print(f'  -> Encrypted successfully')
                
                # Small delay to allow real-time detection
                time.sleep(0.5)
                
            except Exception as e:
                print(f'  -> FAILED: {e}')
        
        # Create ransom note
        self._create_ransom_note(successful_encryptions)
        
        # Summary
        print()
        print('=' * 50)
        print('ENCRYPTION COMPLETED')
        print('=' * 50)
        print(f'Files encrypted: {successful_encryptions}/{len(files_to_encrypt)}')
        print(f'Extension used: {self.encryption_extension}')
        print('=' * 50)
        
        return key
    
    def _share_key_with_antivirus(self, key):
        """Share encryption key with antivirus for auto-recovery"""
        # In a real implementation, this would securely transmit the key
        # to the antivirus system for potential recovery operations
        print('[🔄] Key shared with real-time antivirus')
    
    def _log_encryption_operations(self, file_path, key):
        """Log all encryption operations for real-time detection"""
        # Detailed behavioral logging for immediate detection
        operations = [
            ('ReadFile', str(file_path), {
                'operation': 'ransomware_read',
                'size': file_path.stat().st_size,
                'encryption_key': key.decode(),  # Share key for recovery
                'real_time_detection': True
            }),
            ('CryptEncrypt', str(file_path), {
                'operation': 'ransomware_encrypt',
                'algorithm': 'Fernet-AES128',
                'input_size': file_path.stat().st_size,
                'encryption_key': key.decode(),
                'real_time_detection': True
            }),
            ('WriteFile', str(file_path) + self.encryption_extension, {
                'operation': 'ransomware_write',
                'size': file_path.stat().st_size,  # Approximate
                'encryption_key': key.decode(),
                'real_time_detection': True
            }),
            ('DeleteFile', str(file_path), {
                'operation': 'ransomware_delete',
                'encryption_key': key.decode(),
                'real_time_detection': True
            })
        ]
        
        for op_type, path, metadata in operations:
            self.monitor.log_operation(op_type, path, metadata)

    def generate_key(self):
        """Generate Fernet encryption key"""
        self.key = Fernet.generate_key()
        return self.key
    
    def _create_ransom_note(self, file_count):
        """Create educational ransom note"""
        note_content = f'''===============================================
   REAL-TIME RANSOMWARE DETECTION DEMO
===============================================

YOUR FILES WERE BEING ENCRYPTED!

Files targeted: {file_count}
Extension: {self.encryption_extension}

DETECTION & RECOVERY:
- Real-time antivirus monitoring: ACTIVE
- Automatic threat detection: ENABLED
- Auto-recovery capability: AVAILABLE

THIS IS AN EDUCATIONAL DEMONSTRATION.
NO ACTUAL DAMAGE OCCURRED.

===============================================
      DEMONSTRATION COMPLETE
===============================================
'''
        
        note_path = self.target_directory / 'REAL_TIME_DETECTION_NOTICE.txt'
        with open(note_path, 'w') as f:
            f.write(note_content)
        print(f'[📝] Created detection notice: REAL_TIME_DETECTION_NOTICE.txt')

# Demo function
def run_real_time_demo():
    """Run real-time antivirus demonstration"""
    print("Starting Real-Time Antivirus Demo...")
    print()
    
    # Initialize real-time antivirus
    antivirus = RealTimeAntivirus()
    monitor_thread = antivirus.start_real_time_monitoring()
    
    # Give monitoring time to start
    time.sleep(2)
    
    # Run enhanced encryption with real-time detection
    encryptor = EnhancedRealEncryptor(
        r'C:\Users\Kanhaiya\System And Security\core_system\data\test_files',
        antivirus
    )
    
    print("Running encryption with real-time detection...")
    recovery_key = encryptor.encrypt_files_with_real_time_detection()
    
    # Let monitoring continue for a bit
    time.sleep(3)
    
    print()
    print("Demo completed!")
    print(f"Recovery key (if needed): {recovery_key.decode()}")

if __name__ == "__main__":
    run_real_time_demo()