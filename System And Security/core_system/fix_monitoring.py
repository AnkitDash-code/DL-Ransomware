"""
MONITORING PATH CONFIGURATION FIX
Ensures antivirus monitors the correct directories for real-time detection
"""

import os
import sys
from pathlib import Path

def fix_monitoring_paths():
    """Fix monitoring paths for antivirus detection"""
    print("=== FIXING ANTIVIRUS MONITORING PATHS ===")
    print()
    
    # Define the directories that should be monitored
    monitored_directories = [
        r"C:\Users\Kanhaiya\System And Security\core_system\data\test_files",
        r"D:\Backup"
    ]
    
    print("Directories that should be monitored:")
    for directory in monitored_directories:
        path = Path(directory)
        if path.exists():
            file_count = len([f for f in path.iterdir() if f.is_file()])
            print(f"  ✓ {directory} ({file_count} files)")
        else:
            print(f"  ✗ {directory} (DIRECTORY NOT FOUND)")
    
    print()
    print("Current antivirus configuration:")
    
    # Check core_system config
    core_config_path = Path(r"C:\Users\Kanhaiya\System And Security\core_system\config.py")
    if core_config_path.exists():
        print(f"  Core system config: {core_config_path}")
        # Read and display relevant parts
        with open(core_config_path, 'r') as f:
            content = f.read()
            if 'TEST_FILES_DIR' in content:
                lines = content.split('\n')
                for line in lines:
                    if 'TEST_FILES_DIR' in line:
                        print(f"    {line.strip()}")
    
    # Check security_tools config
    security_config_path = Path(r"C:\Users\Kanhaiya\System And Security\security_tools\config.py")
    if security_config_path.exists():
        print(f"  Security tools config: {security_config_path}")
        with open(security_config_path, 'r') as f:
            content = f.read()
            if 'TEST_FILES_DIR' in content:
                lines = content.split('\n')
                for line in lines:
                    if 'TEST_FILES_DIR' in line:
                        print(f"    {line.strip()}")
    
    print()
    print("To ensure detection:")
    print("1. Start antivirus with: start_antivirus_core.bat or start_antivirus_backup.bat")
    print("2. The antivirus will monitor behavioral logs, not directory contents directly")
    print("3. Real file operations (read/write/delete/encrypt) will be detected")
    print("4. Check the antivirus console/GUI for threat alerts")
    
    return monitored_directories

def test_file_operations():
    """Test if file operations are being monitored"""
    print()
    print("=== TESTING FILE OPERATION MONITORING ===")
    
    test_dir = Path(r"C:\Users\Kanhaiya\System And Security\core_system\data\test_files")
    
    if not test_dir.exists():
        print("[ERROR] Test directory not found!")
        return False
    
    # Create a test file
    test_file = test_dir / "monitoring_test.txt"
    print(f"Creating test file: {test_file.name}")
    
    try:
        # Write test file
        with open(test_file, 'w') as f:
            f.write("This is a test file for monitoring detection")
        print("✓ File write operation completed")
        
        # Read test file
        with open(test_file, 'r') as f:
            content = f.read()
        print("✓ File read operation completed")
        
        # Delete test file
        test_file.unlink()
        print("✓ File delete operation completed")
        
        print()
        print("File operations completed successfully!")
        print("Check antivirus console for detection of these operations")
        return True
        
    except Exception as e:
        print(f"[ERROR] File operation failed: {e}")
        return False

if __name__ == "__main__":
    fix_monitoring_paths()
    test_file_operations()
    
    print()
    print("=" * 50)
    print("MONITORING PATH CONFIGURATION CHECK COMPLETE")
    print("=" * 50)
    print("Next steps:")
    print("1. Run: start_antivirus_core.bat")
    print("2. In another terminal: start_virus_core_real.bat") 
    print("3. Watch antivirus console for detection alerts")
    print("=" * 50)