"""
ENHANCED DASHBOARD WITH ACTIVE INTERVENTION INTEGRATION
Combines traditional monitoring with active intervention status
"""

import os
import sys
import time
import json
import threading
from datetime import datetime
from pathlib import Path

# Add paths for imports
sys.path.insert(0, r"C:\Users\Kanhaiya\System And Security\core_system")
sys.path.insert(0, r"C:\Users\Kanhaiya\System And Security")

from active_intervention_antivirus import ActiveInterventionAntivirus
from monitor.monitor import BehaviorMonitor

class IntegratedDashboardBackend:
    def __init__(self):
        self.active_antivirus = ActiveInterventionAntivirus()
        self.behavior_monitor = BehaviorMonitor()
        self.dashboard_data = {
            'threats_detected': 0,
            'operations_blocked': 0,
            'files_recovered': 0,
            'recovery_keys': {},
            'blocked_operations': [],
            'current_status': 'ACTIVE',
            'last_update': datetime.now().isoformat()
        }
        
    def start_integration(self):
        """Start integrated monitoring"""
        print("🚀 Starting Integrated Dashboard Backend...")
        
        # Start active antivirus monitoring
        detection_thread, intervention_thread = self.active_antivirus.start_active_protection()
        
        # Start data collection thread
        data_thread = threading.Thread(target=self._collect_dashboard_data, daemon=True)
        data_thread.start()
        
        return detection_thread, intervention_thread, data_thread
    
    def _collect_dashboard_data(self):
        """Collect data for dashboard display"""
        while True:
            try:
                # Update dashboard data from active antivirus
                self.dashboard_data.update({
                    'threats_detected': len(self.active_antivirus.recovery_keys),
                    'operations_blocked': len(self.active_antivirus.blocked_operations),
                    'files_recovered': self._count_recovered_files(),
                    'recovery_keys': dict(self.active_antivirus.recovery_keys),
                    'blocked_operations': list(self.active_antivirus.blocked_operations),
                    'current_status': 'ACTIVE' if self.active_antivirus.intervention_active else 'STOPPED',
                    'last_update': datetime.now().isoformat()
                })
                
                # Also collect from behavioral monitor
                recent_ops = self.behavior_monitor.get_recent_operations(20)
                self.dashboard_data['recent_operations'] = [
                    {
                        'timestamp': op.get('timestamp', ''),
                        'operation': op.get('api_call', ''),
                        'file': op.get('file_path', ''),
                        'threat': self._is_operation_threatening(op)
                    }
                    for op in recent_ops
                ]
                
                time.sleep(1)  # Update every second
                
            except Exception as e:
                print(f"[DASHBOARD ERROR] {e}")
                time.sleep(2)
    
    def _count_recovered_files(self):
        """Count successfully recovered files"""
        # In a real implementation, this would track actual recovery operations
        # For now, we'll estimate based on blocked operations that had keys
        return min(len(self.active_antivirus.blocked_operations), 
                  len(self.active_antivirus.recovery_keys))
    
    def _is_operation_threatening(self, operation):
        """Determine if an operation is threatening"""
        metadata = operation.get('metadata', {})
        operation_type = metadata.get('operation', '')
        
        threatening_patterns = [
            'ransomware_read',
            'ransomware_encrypt', 
            'ransomware_write',
            'ransomware_delete'
        ]
        
        return operation_type in threatening_patterns
    
    def get_dashboard_data(self):
        """Get current dashboard data"""
        return self.dashboard_data.copy()
    
    def trigger_manual_recovery(self, file_path=None):
        """Trigger manual recovery for specific files"""
        if file_path:
            # Try to recover specific file
            for encrypted_ext in ['.core_encrypted', '.backup_encrypted']:
                encrypted_file = Path(file_path + encrypted_ext)
                if encrypted_file.exists() and file_path in self.active_antivirus.recovery_keys:
                    key = self.active_antivirus.recovery_keys[file_path]
                    self._attempt_recovery(encrypted_file, key, Path(file_path).name)
                    return True
        else:
            # Try to recover all files with available keys
            recovered_count = 0
            for original_file, key in self.active_antivirus.recovery_keys.items():
                for ext in ['.core_encrypted', '.backup_encrypted']:
                    encrypted_file = Path(original_file + ext)
                    if encrypted_file.exists():
                        if self._attempt_recovery(encrypted_file, key, Path(original_file).name):
                            recovered_count += 1
                            break
            return recovered_count > 0
    
    def _attempt_recovery(self, encrypted_path, key_str, original_name):
        """Attempt to recover a single file"""
        try:
            from cryptography.fernet import Fernet
            
            # Validate and decode key
            if len(key_str) != 44:
                padding_needed = 4 - (len(key_str) % 4)
                if padding_needed != 4:
                    key_str = key_str + ('=' * padding_needed)
            
            key = key_str.encode()
            cipher = Fernet(key)
            
            # Read and decrypt
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = cipher.decrypt(encrypted_data)
            
            # Write original file
            original_path = encrypted_path.parent / original_name
            with open(original_path, 'wb') as f:
                f.write(decrypted_data)
            
            # Remove encrypted file
            encrypted_path.unlink()
            
            print(f"✅ RECOVERED: {original_name}")
            self.dashboard_data['files_recovered'] += 1
            return True
            
        except Exception as e:
            print(f"❌ Recovery failed for {original_name}: {e}")
            return False

# Enhanced dashboard function for Streamlit
def get_enhanced_dashboard_data():
    """Get integrated dashboard data for Streamlit"""
    backend = getattr(get_enhanced_dashboard_data, 'backend', None)
    if backend is None:
        backend = IntegratedDashboardBackend()
        get_enhanced_dashboard_data.backend = backend
        backend.start_integration()
    
    return backend.get_dashboard_data()

def trigger_dashboard_recovery(file_path=None):
    """Trigger recovery from dashboard"""
    backend = getattr(get_enhanced_dashboard_data, 'backend', None)
    if backend:
        return backend.trigger_manual_recovery(file_path)
    return False

# Test the integration
if __name__ == "__main__":
    print("=== INTEGRATED DASHBOARD BACKEND TEST ===")
    
    backend = IntegratedDashboardBackend()
    detection_thread, intervention_thread, data_thread = backend.start_integration()
    
    print("Backend started, collecting data...")
    time.sleep(3)
    
    # Test data collection
    data = backend.get_dashboard_data()
    print(f"Threats detected: {data['threats_detected']}")
    print(f"Operations blocked: {data['operations_blocked']}")
    print(f"Files recovered: {data['files_recovered']}")
    print(f"Status: {data['current_status']}")
    
    print("\nIntegration backend ready for dashboard use!")