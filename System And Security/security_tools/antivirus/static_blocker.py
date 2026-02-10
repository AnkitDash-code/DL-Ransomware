"""
Static File Blocking Module for Antivirus
Implements signature-based and hash-based file blocking
"""
import os
import sys
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Set, Optional

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class StaticFileBlocker:
    """
    Implements static file blocking based on signatures, hashes, and patterns.
    Provides real-time file scanning and blocking capabilities.
    """
    
    def __init__(self, block_list_path: str = None):
        self.block_list_path = block_list_path or "antivirus/block_list.json"
        self.signatures = set()  # Known malicious signatures
        self.hashes = {}  # Hash -> threat name mapping
        self.patterns = set()  # Filename/path patterns
        self.extensions = set()  # Blocked file extensions
        self.process_names = set()  # Blocked process names
        
        self.blocked_files = []
        self.blocked_processes = []
        self.scan_stats = {
            "files_scanned": 0,
            "files_blocked": 0,
            "hash_matches": 0,
            "signature_matches": 0,
            "pattern_matches": 0
        }
        
        self._load_block_lists()
        self._initialize_default_blocks()
    
    def _load_block_lists(self):
        """Load block lists from configuration file."""
        try:
            if os.path.exists(self.block_list_path):
                with open(self.block_list_path, 'r') as f:
                    config = json.load(f)
                
                self.signatures = set(config.get("signatures", []))
                self.hashes = config.get("hashes", {})
                self.patterns = set(config.get("patterns", []))
                self.extensions = set(config.get("extensions", []))
                self.process_names = set(config.get("process_names", []))
                
                print(f"[BLOCKER] Loaded block lists from {self.block_list_path}")
                print(f"  Signatures: {len(self.signatures)}")
                print(f"  Hashes: {len(self.hashes)}")
                print(f"  Patterns: {len(self.patterns)}")
                print(f"  Extensions: {len(self.extensions)}")
                print(f"  Processes: {len(self.process_names)}")
            else:
                # If no block list exists, try to load threat database
                self._load_threat_database()
        except Exception as e:
            print(f"[BLOCKER] Failed to load block lists: {e}")
            self._initialize_default_blocks()
    
    def _load_threat_database(self):
        """Load comprehensive threat database."""
        try:
            database_path = os.path.join(os.path.dirname(__file__), "threat_database.json")
            if os.path.exists(database_path):
                with open(database_path, 'r') as f:
                    db = json.load(f)
                
                print("[BLOCKER] Loading threat database...")
                
                # Load ransomware families
                for family_data in db.get("ransomware_families", {}).values():
                    for pattern in family_data.get("file_patterns", []):
                        self.patterns.add(pattern)
                    for process in family_data.get("process_names", []):
                        self.process_names.add(process.lower())
                    for hash_val in family_data.get("known_hashes", {}):
                        self.hashes[hash_val] = f"Ransomware: {list(family_data.get('known_hashes', {}).keys())[0]}"
                
                # Load trojan families
                for family_data in db.get("trojan_families", {}).values():
                    for pattern in family_data.get("file_patterns", []):
                        self.patterns.add(pattern)
                    for process in family_data.get("process_names", []):
                        self.process_names.add(process.lower())
                
                # Load generic indicators
                generic = db.get("generic_indicators", {})
                self.extensions.update(generic.get("suspicious_extensions", []))
                self.patterns.update(generic.get("suspicious_filenames", []))
                self.process_names.update(generic.get("suspicious_process_names", []))
                
                print("[BLOCKER] Threat database loaded successfully")
                
        except Exception as e:
            print(f"[BLOCKER] Failed to load threat database: {e}")
            self._initialize_default_blocks()
    
    def _initialize_default_blocks(self):
        """Initialize with default known malicious patterns."""
        # Common ransomware extensions to block
        self.extensions.update([
            ".locked", ".crypt", ".encrypted", ".vault", 
            ".ezz", ".xyz", ".zzz", ".abc", ".aaa",
            ".karl", ".locky", ".zepto", ".cryptolocker"
        ])
        
        # Suspicious filename patterns
        self.patterns.update([
            "READ_ME_NOW", "DECRYPT_INSTRUCTIONS", "HOW_TO_RECOVER",
            "FILES_ENCRYPTED", "*_INSTRUCTIONS.txt", "*_RECOVERY_KEY.*",
            "bitcoin_address", "payment_instructions"
        ])
        
        # Known malicious process names
        self.process_names.update([
            "ransomware.exe", "locker.exe", "encryptor.exe",
            "cryptolocker.exe", "teslacrypt.exe", "reveton.exe"
        ])
        
        # Some example hashes (these would be real malware hashes in practice)
        self.hashes.update({
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": "Empty file (demo)",
            "d41d8cd98f00b204e9800998ecf8427e": "MD5 of empty string (demo)"
        })
    
    def save_block_lists(self):
        """Save current block lists to file."""
        try:
            config = {
                "signatures": list(self.signatures),
                "hashes": self.hashes,
                "patterns": list(self.patterns),
                "extensions": list(self.extensions),
                "process_names": list(self.process_names)
            }
            
            os.makedirs(os.path.dirname(self.block_list_path), exist_ok=True)
            with open(self.block_list_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"[BLOCKER] Saved block lists to {self.block_list_path}")
        except Exception as e:
            print(f"[BLOCKER] Failed to save block lists: {e}")
    
    def add_signature(self, signature: str, threat_name: str = "Unknown"):
        """Add a signature to the block list."""
        self.signatures.add(signature)
        print(f"[BLOCKER] Added signature: {signature} ({threat_name})")
    
    def add_hash(self, file_hash: str, threat_name: str = "Unknown"):
        """Add a file hash to the block list."""
        self.hashes[file_hash] = threat_name
        print(f"[BLOCKER] Added hash: {file_hash} ({threat_name})")
    
    def add_pattern(self, pattern: str):
        """Add a filename pattern to block."""
        self.patterns.add(pattern)
        print(f"[BLOCKER] Added pattern: {pattern}")
    
    def add_extension(self, extension: str):
        """Add a file extension to block."""
        self.extensions.add(extension.lower())
        print(f"[BLOCKER] Added extension: {extension}")
    
    def add_process_name(self, process_name: str):
        """Add a process name to block."""
        self.process_names.add(process_name.lower())
        print(f"[BLOCKER] Added process name: {process_name}")
    
    def calculate_file_hash(self, file_path: str) -> Optional[str]:
        """Calculate SHA256 hash of a file."""
        try:
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                # Read file in chunks for large files
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except:
            return None
    
    def check_file_signature(self, file_path: str) -> bool:
        """Check if file contains known malicious signatures."""
        try:
            with open(file_path, 'rb') as f:
                content = f.read(1024)  # Read first 1KB
            
            # Check for string signatures
            content_str = content.decode('utf-8', errors='ignore')
            for signature in self.signatures:
                if signature in content_str:
                    return True
            return False
        except:
            return False
    
    def check_file_hash(self, file_path: str) -> Optional[str]:
        """Check if file hash matches known malicious hashes."""
        file_hash = self.calculate_file_hash(file_path)
        if file_hash and file_hash in self.hashes:
            return self.hashes[file_hash]
        return None
    
    def check_filename_patterns(self, file_path: str) -> bool:
        """Check if filename matches blocked patterns."""
        filename = os.path.basename(file_path).lower()
        
        for pattern in self.patterns:
            pattern = pattern.lower()
            if "*" in pattern:
                # Simple wildcard matching
                prefix, suffix = pattern.split("*", 1)
                if filename.startswith(prefix) and filename.endswith(suffix):
                    return True
            else:
                if pattern in filename:
                    return True
        return False
    
    def check_file_extension(self, file_path: str) -> bool:
        """Check if file extension is blocked."""
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.extensions
    
    def should_block_file(self, file_path: str) -> tuple[bool, str]:
        """
        Check if a file should be blocked.
        Returns (should_block: bool, reason: str)
        """
        self.scan_stats["files_scanned"] += 1
        
        # Check hash
        threat_name = self.check_file_hash(file_path)
        if threat_name:
            self.scan_stats["hash_matches"] += 1
            self.scan_stats["files_blocked"] += 1
            self.blocked_files.append(file_path)
            return True, f"Known malicious hash ({threat_name})"
        
        # Check signature
        if self.check_file_signature(file_path):
            self.scan_stats["signature_matches"] += 1
            self.scan_stats["files_blocked"] += 1
            self.blocked_files.append(file_path)
            return True, "Contains malicious signature"
        
        # Check filename patterns
        if self.check_filename_patterns(file_path):
            self.scan_stats["pattern_matches"] += 1
            self.scan_stats["files_blocked"] += 1
            self.blocked_files.append(file_path)
            return True, "Matches blocked filename pattern"
        
        # Check extension
        if self.check_file_extension(file_path):
            self.scan_stats["files_blocked"] += 1
            self.blocked_files.append(file_path)
            return True, f"Blocked extension: {os.path.splitext(file_path)[1]}"
        
        return False, "File is clean"
    
    def should_block_process(self, process_name: str) -> bool:
        """Check if a process should be blocked."""
        return process_name.lower() in self.process_names
    
    def scan_directory(self, directory: str, recursive: bool = True) -> Dict:
        """Scan a directory for blocked files."""
        print(f"[BLOCKER] Scanning directory: {directory}")
        
        blocked_in_dir = []
        total_files = 0
        
        try:
            path = Path(directory)
            pattern = "**/*" if recursive else "*"
            
            for file_path in path.glob(pattern):
                if file_path.is_file():
                    total_files += 1
                    should_block, reason = self.should_block_file(str(file_path))
                    if should_block:
                        blocked_in_dir.append({
                            "file": str(file_path),
                            "reason": reason
                        })
            
            print(f"[BLOCKER] Scan complete: {total_files} files, {len(blocked_in_dir)} blocked")
            
        except Exception as e:
            print(f"[BLOCKER] Scan failed: {e}")
        
        return {
            "directory": directory,
            "total_files": total_files,
            "blocked_files": blocked_in_dir,
            "stats": self.scan_stats.copy()
        }
    
    def get_statistics(self) -> Dict:
        """Get blocking statistics."""
        return {
            "block_lists": {
                "signatures": len(self.signatures),
                "hashes": len(self.hashes),
                "patterns": len(self.patterns),
                "extensions": len(self.extensions),
                "processes": len(self.process_names)
            },
            "scan_stats": self.scan_stats.copy(),
            "blocked_files": len(self.blocked_files),
            "blocked_processes": len(self.blocked_processes)
        }

# Global blocker instance
_static_blocker = None

def get_static_blocker() -> StaticFileBlocker:
    """Get or create the global static blocker instance."""
    global _static_blocker
    if _static_blocker is None:
        _static_blocker = StaticFileBlocker()
    return _static_blocker

def main():
    """Test the static file blocker."""
    print("=" * 60)
    print("STATIC FILE BLOCKER - TESTING")
    print("=" * 60)
    
    blocker = get_static_blocker()
    
    # Test with current directory
    test_dir = "."
    results = blocker.scan_directory(test_dir, recursive=False)
    
    print(f"\nScan Results for {test_dir}:")
    print(f"  Total files scanned: {results['total_files']}")
    print(f"  Files blocked: {len(results['blocked_files'])}")
    
    if results['blocked_files']:
        print("\nBlocked files:")
        for item in results['blocked_files']:
            print(f"  - {item['file']}: {item['reason']}")
    
    print(f"\nStatistics:")
    stats = blocker.get_statistics()
    print(f"  Block lists loaded: {stats['block_lists']}")
    print(f"  Scan statistics: {stats['scan_stats']}")

if __name__ == "__main__":
    main()
