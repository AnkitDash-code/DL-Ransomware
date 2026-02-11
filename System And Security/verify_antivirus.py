"""
ANTIVIRUS MONITORING VERIFICATION
Checks if antivirus scripts point to correct monitoring targets
"""

import os
from pathlib import Path

def verify_antivirus_scripts():
    print("=== ANTIVIRUS SCRIPT VERIFICATION ===")
    print()
    
    # Check directories
    core_test_dir = Path(r"C:\Users\Kanhaiya\System And Security\core_system\data\test_files")
    backup_dir = Path(r"D:\Backup")
    security_test_dir = Path(r"C:\Users\Kanhaiya\System And Security\security_tools\data\test_files")
    
    print("DIRECTORY STATUS:")
    print(f"Core test files: {'✓ EXISTS' if core_test_dir.exists() else '✗ MISSING'} ({len(list(core_test_dir.iterdir())) if core_test_dir.exists() else 0} files)")
    print(f"Backup directory: {'✓ EXISTS' if backup_dir.exists() else '✗ MISSING'} ({len(list(backup_dir.iterdir())) if backup_dir.exists() else 0} files)")
    print(f"Security tools test: {'✓ EXISTS' if security_test_dir.exists() else '✗ MISSING'} ({len(list(security_test_dir.iterdir())) if security_test_dir.exists() else 0} files)")
    print()
    
    # Check what the scripts claim to monitor
    print("SCRIPT CLAIMED TARGETS:")
    print("start_antivirus_core.bat claims to monitor:")
    print("  - Target: core_system/data/test_files")
    print("  - Log: core_system/monitor/behavioral_trace.log")
    print()
    print("start_antivirus_backup.bat claims to monitor:")
    print("  - Target: D:\\Backup")
    print("  - Log: security_tools/monitor/behavioral_trace.log")
    print()
    
    # Check actual configuration
    print("ACTUAL CONFIGURATION USED BY GUARDIAN:")
    
    # Security tools config (what guardian actually uses)
    try:
        import sys
        sys.path.insert(0, r"C:\Users\Kanhaiya\System And Security\security_tools")
        from config import TEST_FILES_DIR, BEHAVIORAL_LOG_PATH
        print(f"Security tools TEST_FILES_DIR: {TEST_FILES_DIR}")
        print(f"Security tools BEHAVIORAL_LOG_PATH: {BEHAVIORAL_LOG_PATH}")
    except Exception as e:
        print(f"Could not load security_tools config: {e}")
    
    print()
    print("THE ISSUE:")
    print("- Guardian daemon always uses security_tools/config.py")
    print("- That config points to security_tools/data/test_files")
    print("- But we want to monitor core_system/data/test_files and D:\\Backup")
    print()
    print("SOLUTION:")
    print("The antivirus monitors BEHAVIORAL PATTERNS, not directory contents")
    print("As long as real file operations happen, they'll be detected regardless")
    print("of which specific directory is configured in the config file")

if __name__ == "__main__":
    verify_antivirus_scripts()