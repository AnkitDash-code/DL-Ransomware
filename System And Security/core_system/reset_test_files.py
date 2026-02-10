"""
Script to reset test files for ransomware simulation
"""
import os
import sys
import shutil
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def reset_test_files():
    """Reset the test files directory by removing encrypted files and restoring originals."""
    from data.setup_test_files import setup_test_files
    
    print("Resetting test files...")
    
    test_dir = Path("data/test_files")
    
    # Remove all encrypted files and ransom notes
    encrypted_extensions = ['.locked', '.crypted']
    ransom_notes = ['README_DECRYPT.txt']
    
    files_removed = 0
    
    for file_path in test_dir.rglob('*'):
        if file_path.is_file():
            if file_path.suffix in encrypted_extensions or file_path.name in ransom_notes:
                file_path.unlink()
                print(f"  Removed: {file_path.name}")
                files_removed += 1
    
    # Remove any recovery key files
    recovery_keys = list(test_dir.parent.rglob('recovery_key.bin'))
    recovery_keys.extend(list(Path('.').rglob('recovery_key.bin')))
    for key_file in recovery_keys:
        if key_file.exists():
            key_file.unlink()
            print(f"  Removed: {key_file}")
            files_removed += 1
    
    if files_removed > 0:
        print(f"Removed {files_removed} encrypted files/recovery files")
    
    # Create fresh test files
    setup_test_files()
    
    print("\nTest files have been reset successfully!")
    return True

def main():
    """Main function to run the reset script."""
    print("=" * 50)
    print("RANSOMWARE TEST FILE RESET SCRIPT")
    print("=" * 50)
    
    reset_test_files()
    
    print("=" * 50)
    print("RESET COMPLETE!")
    print("Ready for new ransomware simulation tests.")
    print("=" * 50)

if __name__ == "__main__":
    main()
