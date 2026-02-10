"""
Benign Backup Simulator
Simulates normal backup operations (heavy read/write, low entropy)
"""
import os
import sys
import time
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TEST_FILES_DIR, DEMO_DELAY
from monitor.monitor import BehaviorMonitor, MonitoredFileOperations


class BackupSimulator:
    """
    Simulates benign backup operations.
    Behavior pattern:
    - Read files from source
    - Write exact copies to destination
    - No encryption, no file deletion, no extension changes
    """
    
    def __init__(self, source_dir: str = None, dest_dir: str = None, delay: float = None):
        self.source_dir = source_dir or TEST_FILES_DIR
        self.dest_dir = dest_dir or os.path.join(TEST_FILES_DIR, "backup")
        self.delay = delay if delay is not None else DEMO_DELAY
        self.monitor = BehaviorMonitor()
        self.ops = MonitoredFileOperations(self.monitor)
        self.backed_up_files = []
    
    def display_banner(self):
        """Display simulator banner."""
        print("\n" + "=" * 60)
        print("  BENIGN BACKUP SIMULATOR")
        print("=" * 60)
        print(f"\n  Source: {self.source_dir}")
        print(f"  Destination: {self.dest_dir}")
        print(f"  Delay per file: {self.delay}s")
        print("\n" + "-" * 60)
    
    def prepare_destination(self):
        """Create destination directory if it doesn't exist."""
        os.makedirs(self.dest_dir, exist_ok=True)
        self.ops.create_file(os.path.join(self.dest_dir, ".backup_marker"))
    
    def get_source_files(self) -> list:
        """Get list of files to backup."""
        print("\n[SCAN] Scanning source directory...")
        
        files = self.ops.list_directory(self.source_dir)
        
        # Filter out backup directory and non-files
        source_files = []
        for f in files:
            if self.dest_dir not in f and os.path.isfile(f):
                source_files.append(f)
        
        print(f"        Found {len(source_files)} files to backup")
        return source_files
    
    def backup_file(self, file_path: str) -> bool:
        """Backup a single file."""
        try:
            # Read source file
            data = self.ops.read_file(file_path)
            
            # Calculate relative path
            rel_path = os.path.relpath(file_path, self.source_dir)
            dest_path = os.path.join(self.dest_dir, rel_path)
            
            # Create destination subdirectory if needed
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            # Write to destination (same content, same extension)
            self.ops.write_file(dest_path, data)
            
            self.backed_up_files.append({
                "source": file_path,
                "destination": dest_path,
                "size": len(data)
            })
            
            return True
            
        except Exception as e:
            print(f"        [ERROR] Failed to backup {file_path}: {e}")
            return False
    
    def run(self):
        """Execute the backup simulation."""
        self.display_banner()
        self.monitor.clear_log()
        
        # Prepare destination
        self.prepare_destination()
        
        # Get files to backup
        source_files = self.get_source_files()
        
        if not source_files:
            print("\n[INFO] No files found to backup.")
            return False
        
        # Backup files
        print(f"\n[BACKUP] Backing up {len(source_files)} files...")
        
        for i, file_path in enumerate(source_files, 1):
            filename = os.path.basename(file_path)
            print(f"         [{i}/{len(source_files)}] Copying: {filename}")
            
            if self.backup_file(file_path):
                time.sleep(self.delay)
        
        # Summary
        total_size = sum(f['size'] for f in self.backed_up_files)
        
        print("\n" + "=" * 60)
        print("  BACKUP COMPLETE")
        print("=" * 60)
        print(f"\n  Files backed up: {len(self.backed_up_files)}")
        print(f"  Total size: {total_size:,} bytes")
        print(f"  Destination: {self.dest_dir}")
        print(f"  Operations logged: {self.monitor.operation_count}")
        
        return True
    
    def cleanup(self):
        """Remove backup directory."""
        if os.path.exists(self.dest_dir):
            shutil.rmtree(self.dest_dir)
            print(f"[CLEANUP] Removed backup directory: {self.dest_dir}")


def main():
    """Run the backup simulator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Benign Backup Simulator")
    parser.add_argument("--source", type=str, default=TEST_FILES_DIR,
                        help="Source directory to backup")
    parser.add_argument("--dest", type=str, default=None,
                        help="Destination directory")
    parser.add_argument("--delay", type=float, default=DEMO_DELAY,
                        help="Delay between file operations")
    parser.add_argument("--cleanup", action="store_true",
                        help="Clean up backup after simulation")
    
    args = parser.parse_args()
    
    simulator = BackupSimulator(args.source, args.dest, args.delay)
    success = simulator.run()
    
    if success and args.cleanup:
        input("\nPress Enter to clean up backup...")
        simulator.cleanup()


if __name__ == "__main__":
    main()
