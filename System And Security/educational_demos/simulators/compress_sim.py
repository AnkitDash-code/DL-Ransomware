"""
Benign Compression Simulator
Simulates normal file compression (high entropy output, different API pattern)
"""
import os
import sys
import time
import zipfile
import gzip

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TEST_FILES_DIR, DEMO_DELAY
from monitor.monitor import BehaviorMonitor, MonitoredFileOperations


class CompressionSimulator:
    """
    Simulates benign compression operations.
    Behavior pattern:
    - Read files from source
    - Create compressed archive (high entropy, but predictable pattern)
    - No file deletion, no crypto APIs, creates single output file
    """
    
    def __init__(self, source_dir: str = None, delay: float = None):
        self.source_dir = source_dir or TEST_FILES_DIR
        self.delay = delay if delay is not None else DEMO_DELAY
        self.monitor = BehaviorMonitor()
        self.ops = MonitoredFileOperations(self.monitor)
        self.compressed_files = []
    
    def display_banner(self):
        """Display simulator banner."""
        print("\n" + "=" * 60)
        print("  BENIGN COMPRESSION SIMULATOR")
        print("=" * 60)
        print(f"\n  Source: {self.source_dir}")
        print(f"  Delay per file: {self.delay}s")
        print("\n" + "-" * 60)
    
    def get_source_files(self) -> list:
        """Get list of files to compress."""
        print("\n[SCAN] Scanning source directory...")
        
        files = self.ops.list_directory(self.source_dir)
        
        # Filter to actual files (exclude archives)
        source_files = []
        for f in files:
            if os.path.isfile(f) and not f.endswith(('.zip', '.gz', '.tar')):
                source_files.append(f)
        
        print(f"        Found {len(source_files)} files to compress")
        return source_files
    
    def compress_to_zip(self, files: list) -> str:
        """Create a ZIP archive of the files."""
        archive_path = os.path.join(self.source_dir, "archive.zip")
        
        print(f"\n[ZIP] Creating ZIP archive: {archive_path}")
        
        # Log archive creation
        self.monitor.log_operation(
            api_call="CreateFile",
            file_path=archive_path,
            params={"type": "archive"}
        )
        
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in files:
                filename = os.path.basename(file_path)
                print(f"       Adding: {filename}")
                
                # Read file (logged)
                data = self.ops.read_file(file_path)
                
                # Add to archive
                arcname = os.path.relpath(file_path, self.source_dir)
                zipf.writestr(arcname, data)
                
                self.compressed_files.append({
                    "source": file_path,
                    "size": len(data)
                })
                
                time.sleep(self.delay)
        
        # Log final write
        archive_size = os.path.getsize(archive_path)
        self.monitor.log_operation(
            api_call="WriteFile",
            file_path=archive_path,
            params={"size": archive_size, "type": "compressed_archive"}
        )
        
        return archive_path
    
    def compress_individual_gzip(self, files: list) -> list:
        """Create individual gzip files."""
        gzip_files = []
        
        print(f"\n[GZIP] Creating individual GZIP files...")
        
        for i, file_path in enumerate(files, 1):
            filename = os.path.basename(file_path)
            gzip_path = file_path + ".gz"
            
            print(f"       [{i}/{len(files)}] Compressing: {filename}")
            
            # Read original
            data = self.ops.read_file(file_path)
            
            # Compress and write
            with gzip.open(gzip_path, 'wb') as gz:
                gz.write(data)
            
            # Log the write
            gz_size = os.path.getsize(gzip_path)
            self.monitor.log_operation(
                api_call="WriteFile",
                file_path=gzip_path,
                params={"size": gz_size, "compression": "gzip"}
            )
            
            gzip_files.append(gzip_path)
            self.compressed_files.append({
                "source": file_path,
                "compressed": gzip_path,
                "original_size": len(data),
                "compressed_size": gz_size
            })
            
            time.sleep(self.delay)
        
        return gzip_files
    
    def run(self, method: str = "zip"):
        """
        Execute the compression simulation.
        
        Args:
            method: 'zip' for single archive, 'gzip' for individual files
        """
        self.display_banner()
        self.monitor.clear_log()
        
        # Get files to compress
        source_files = self.get_source_files()
        
        if not source_files:
            print("\n[INFO] No files found to compress.")
            return False
        
        # Compress based on method
        if method == "zip":
            output = self.compress_to_zip(source_files)
            print(f"\n       Archive created: {output}")
        else:
            outputs = self.compress_individual_gzip(source_files)
            print(f"\n       Created {len(outputs)} compressed files")
        
        # Calculate compression stats
        original_total = sum(f.get('size', f.get('original_size', 0)) 
                           for f in self.compressed_files)
        
        print("\n" + "=" * 60)
        print("  COMPRESSION COMPLETE")
        print("=" * 60)
        print(f"\n  Files compressed: {len(self.compressed_files)}")
        print(f"  Original total: {original_total:,} bytes")
        print(f"  Operations logged: {self.monitor.operation_count}")
        
        return True
    
    def cleanup(self):
        """Remove created archive files."""
        # Remove zip archive
        zip_path = os.path.join(self.source_dir, "archive.zip")
        if os.path.exists(zip_path):
            os.remove(zip_path)
            print(f"[CLEANUP] Removed: {zip_path}")
        
        # Remove gzip files
        for f in self.compressed_files:
            if 'compressed' in f and os.path.exists(f['compressed']):
                os.remove(f['compressed'])
                print(f"[CLEANUP] Removed: {f['compressed']}")


def main():
    """Run the compression simulator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Benign Compression Simulator")
    parser.add_argument("--source", type=str, default=TEST_FILES_DIR,
                        help="Source directory to compress")
    parser.add_argument("--delay", type=float, default=DEMO_DELAY,
                        help="Delay between file operations")
    parser.add_argument("--method", type=str, choices=['zip', 'gzip'], 
                        default='zip', help="Compression method")
    parser.add_argument("--cleanup", action="store_true",
                        help="Clean up archives after simulation")
    
    args = parser.parse_args()
    
    simulator = CompressionSimulator(args.source, args.delay)
    success = simulator.run(method=args.method)
    
    if success and args.cleanup:
        input("\nPress Enter to clean up archives...")
        simulator.cleanup()


if __name__ == "__main__":
    main()
