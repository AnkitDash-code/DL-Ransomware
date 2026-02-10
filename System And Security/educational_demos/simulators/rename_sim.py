"""
Benign Rename Simulator
Simulates bulk file renaming operations (metadata only, no content changes)
"""
import os
import sys
import time
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TEST_FILES_DIR, DEMO_DELAY
from monitor.monitor import BehaviorMonitor, MonitoredFileOperations


class RenameSimulator:
    """
    Simulates benign bulk file renaming operations.
    Behavior pattern:
    - Only metadata operations (no file content read/write)
    - No encryption, no high entropy data
    - Simple rename operations
    """
    
    def __init__(self, source_dir: str = None, delay: float = None):
        self.source_dir = source_dir or TEST_FILES_DIR
        self.delay = delay if delay is not None else DEMO_DELAY
        self.monitor = BehaviorMonitor()
        self.ops = MonitoredFileOperations(self.monitor)
        self.renamed_files = []
    
    def display_banner(self):
        """Display simulator banner."""
        print("\n" + "=" * 60)
        print("  BENIGN RENAME SIMULATOR")
        print("=" * 60)
        print(f"\n  Target: {self.source_dir}")
        print(f"  Delay per file: {self.delay}s")
        print("\n" + "-" * 60)
    
    def get_source_files(self) -> list:
        """Get list of files to rename."""
        print("\n[SCAN] Scanning directory...")
        
        files = self.ops.list_directory(self.source_dir)
        
        # Filter to actual files (exclude backup, archives)
        source_files = []
        for f in files:
            if os.path.isfile(f):
                # Skip special files
                if 'backup' in f or f.endswith(('.zip', '.gz', '.locked')):
                    continue
                source_files.append(f)
        
        print(f"        Found {len(source_files)} files")
        return source_files
    
    def rename_with_timestamp(self, file_path: str) -> str:
        """Rename file by adding timestamp prefix."""
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"{timestamp}_{filename}"
        new_path = os.path.join(directory, new_filename)
        
        # Log the rename operation (metadata only)
        self.monitor.log_operation(
            api_call="MoveFile",
            file_path=file_path,
            params={"new_path": new_path, "operation": "rename"}
        )
        
        # Perform rename
        os.rename(file_path, new_path)
        
        return new_path
    
    def rename_with_prefix(self, file_path: str, prefix: str = "organized_") -> str:
        """Rename file by adding a prefix."""
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        
        new_filename = f"{prefix}{filename}"
        new_path = os.path.join(directory, new_filename)
        
        self.monitor.log_operation(
            api_call="MoveFile",
            file_path=file_path,
            params={"new_path": new_path, "operation": "add_prefix"}
        )
        
        os.rename(file_path, new_path)
        
        return new_path
    
    def rename_to_lowercase(self, file_path: str) -> str:
        """Rename file to lowercase."""
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        
        new_filename = filename.lower()
        
        if new_filename == filename:
            return file_path  # Already lowercase
        
        new_path = os.path.join(directory, new_filename)
        
        self.monitor.log_operation(
            api_call="MoveFile",
            file_path=file_path,
            params={"new_path": new_path, "operation": "lowercase"}
        )
        
        os.rename(file_path, new_path)
        
        return new_path
    
    def run(self, method: str = "timestamp"):
        """
        Execute the rename simulation.
        
        Args:
            method: 'timestamp', 'prefix', or 'lowercase'
        """
        self.display_banner()
        self.monitor.clear_log()
        
        # Get files to rename
        source_files = self.get_source_files()
        
        if not source_files:
            print("\n[INFO] No files found to rename.")
            return False
        
        print(f"\n[RENAME] Renaming {len(source_files)} files (method: {method})...")
        
        for i, file_path in enumerate(source_files, 1):
            filename = os.path.basename(file_path)
            print(f"         [{i}/{len(source_files)}] {filename}")
            
            try:
                if method == "timestamp":
                    new_path = self.rename_with_timestamp(file_path)
                elif method == "prefix":
                    new_path = self.rename_with_prefix(file_path)
                else:  # lowercase
                    new_path = self.rename_to_lowercase(file_path)
                
                if new_path != file_path:
                    self.renamed_files.append({
                        "original": file_path,
                        "new": new_path
                    })
                    print(f"                -> {os.path.basename(new_path)}")
                
                time.sleep(self.delay)
                
            except Exception as e:
                print(f"         [ERROR] Failed to rename: {e}")
        
        print("\n" + "=" * 60)
        print("  RENAME COMPLETE")
        print("=" * 60)
        print(f"\n  Files renamed: {len(self.renamed_files)}")
        print(f"  Operations logged: {self.monitor.operation_count}")
        
        return True
    
    def restore_names(self):
        """Restore original file names."""
        print("\n[RESTORE] Restoring original names...")
        
        for file_info in self.renamed_files:
            try:
                if os.path.exists(file_info['new']):
                    os.rename(file_info['new'], file_info['original'])
                    print(f"         Restored: {os.path.basename(file_info['original'])}")
            except Exception as e:
                print(f"         [ERROR] {e}")
        
        print("[RESTORE] Done")


def main():
    """Run the rename simulator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Benign Rename Simulator")
    parser.add_argument("--source", type=str, default=TEST_FILES_DIR,
                        help="Target directory")
    parser.add_argument("--delay", type=float, default=DEMO_DELAY,
                        help="Delay between operations")
    parser.add_argument("--method", type=str, 
                        choices=['timestamp', 'prefix', 'lowercase'],
                        default='timestamp', help="Rename method")
    parser.add_argument("--restore", action="store_true",
                        help="Restore original names after simulation")
    
    args = parser.parse_args()
    
    simulator = RenameSimulator(args.source, args.delay)
    success = simulator.run(method=args.method)
    
    if success and args.restore:
        input("\nPress Enter to restore original names...")
        simulator.restore_names()


if __name__ == "__main__":
    main()
