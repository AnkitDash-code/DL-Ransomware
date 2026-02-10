"""
Behavior Monitor Module for Zero-Day Ransomware Detection
Logs file operations and API calls for real-time analysis
"""
import os
import sys
import time
import json
import math
import threading
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Optional, Callable

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    BEHAVIORAL_LOG_PATH, TIME_WINDOW_SECONDS, 
    API_CATEGORIES, MONITOR_DIR
)


class BehaviorMonitor:
    """
    Monitors and logs behavioral events from file operations.
    Used by both simulators and the detection system.
    """
    
    def __init__(self, log_path: str = None):
        self.log_path = log_path or BEHAVIORAL_LOG_PATH
        self.lock = threading.Lock()
        self._ensure_log_directory()
        self.start_time = time.time()
        self.operation_count = 0
        
    def _ensure_log_directory(self):
        """Ensure the log directory exists."""
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        
    def log_operation(self, api_call: str, file_path: str = None, 
                      params: Dict = None, pid: int = None):
        """
        Log a behavioral event.
        
        Args:
            api_call: Name of the API/operation (e.g., 'WriteFile', 'ReadFile')
            file_path: Path of the file being operated on
            params: Additional parameters (e.g., data_size, entropy)
            pid: Process ID (defaults to current process)
        """
        timestamp = datetime.now().isoformat()
        pid = pid or os.getpid()
        
        log_entry = {
            "timestamp": timestamp,
            "pid": pid,
            "api_call": api_call,
            "file_path": file_path or "",
            "params": params or {}
        }
        
        with self.lock:
            with open(self.log_path, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            self.operation_count += 1
    
    def clear_log(self):
        """Clear the behavioral log file."""
        with self.lock:
            with open(self.log_path, 'w') as f:
                f.write('')
            self.operation_count = 0
            self.start_time = time.time()
    
    def get_recent_operations(self, max_lines: int = 100) -> List[Dict]:
        """
        Get recent operations from the log.
        
        Args:
            max_lines: Maximum number of recent lines to return
            
        Returns:
            List of log entry dictionaries
        """
        operations = []
        
        if not os.path.exists(self.log_path):
            return operations
        
        with self.lock:
            with open(self.log_path, 'r') as f:
                lines = f.readlines()
        
        # Get last N lines
        recent_lines = lines[-max_lines:] if len(lines) > max_lines else lines
        
        for line in recent_lines:
            line = line.strip()
            if line:
                try:
                    operations.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        
        return operations


class FeatureExtractor:
    """
    Extracts behavioral features from operation logs for ML inference.
    Features based on the research papers:
    - API call counts (especially crypto and file operations)
    - Write/Read ratio
    - Entropy of data
    - Extension changes
    """
    
    def __init__(self):
        self.api_categories = API_CATEGORIES
        
    def calculate_entropy(self, data: bytes) -> float:
        """Calculate Shannon entropy of data."""
        if not data or len(data) == 0:
            return 0.0
        
        # Count byte frequencies
        freq = defaultdict(int)
        for byte in data:
            freq[byte] += 1
        
        # Calculate entropy
        entropy = 0.0
        data_len = len(data)
        for count in freq.values():
            if count > 0:
                p = count / data_len
                entropy -= p * math.log2(p)
        
        return entropy
    
    def extract_features_from_operations(self, operations: List[Dict]) -> Dict:
        """
        Extract feature vector from a list of operations.
        
        Args:
            operations: List of operation log entries
            
        Returns:
            Dictionary of features
        """
        features = {
            # API counts by category
            "crypto_api_count": 0,
            "file_write_count": 0,
            "file_read_count": 0,
            "file_delete_count": 0,
            "file_create_count": 0,
            "registry_count": 0,
            "process_count": 0,
            
            # Derived features
            "total_operations": len(operations),
            "write_read_ratio": 0.0,
            "avg_entropy": 0.0,
            "extension_changes": 0,
            "unique_files": 0,
            "operations_per_second": 0.0,
        }
        
        if not operations:
            return features
        
        # Track files and entropies
        files_seen = set()
        entropies = []
        extension_changes = 0
        
        # Process each operation
        for op in operations:
            api_call = op.get("api_call", "")
            file_path = op.get("file_path", "")
            params = op.get("params", {})
            
            # Count by API category
            api_lower = api_call.lower()
            
            for category, apis in self.api_categories.items():
                if any(api.lower() in api_lower for api in apis):
                    if category == "crypto":
                        features["crypto_api_count"] += 1
                    elif category == "file_write":
                        features["file_write_count"] += 1
                    elif category == "file_read":
                        features["file_read_count"] += 1
                    elif category == "file_delete":
                        features["file_delete_count"] += 1
                    elif category == "file_create":
                        features["file_create_count"] += 1
                    elif category == "registry":
                        features["registry_count"] += 1
                    elif category == "process":
                        features["process_count"] += 1
            
            # Track unique files
            if file_path:
                files_seen.add(file_path)
            
            # Track entropy if available
            if "entropy" in params:
                entropies.append(params["entropy"])
            
            # Track extension changes
            if params.get("extension_changed"):
                extension_changes += 1
        
        # Calculate derived features
        features["unique_files"] = len(files_seen)
        features["extension_changes"] = extension_changes
        
        if entropies:
            features["avg_entropy"] = sum(entropies) / len(entropies)
        
        # Write/Read ratio
        read_count = features["file_read_count"]
        write_count = features["file_write_count"]
        if read_count > 0:
            features["write_read_ratio"] = write_count / read_count
        elif write_count > 0:
            features["write_read_ratio"] = float(write_count)  # High ratio if writes but no reads
        
        # Operations per second
        if len(operations) >= 2:
            try:
                first_ts = datetime.fromisoformat(operations[0]["timestamp"])
                last_ts = datetime.fromisoformat(operations[-1]["timestamp"])
                duration = (last_ts - first_ts).total_seconds()
                if duration > 0:
                    features["operations_per_second"] = len(operations) / duration
            except (ValueError, KeyError):
                pass
        
        return features
    
    def features_to_vector(self, features: Dict) -> List[float]:
        """
        Convert feature dictionary to a vector for ML model.
        
        Args:
            features: Feature dictionary from extract_features_from_operations
            
        Returns:
            List of feature values
        """
        # Define feature order (must match training)
        feature_order = [
            "crypto_api_count",
            "file_write_count",
            "file_read_count",
            "file_delete_count",
            "file_create_count",
            "registry_count",
            "process_count",
            "total_operations",
            "write_read_ratio",
            "avg_entropy",
            "extension_changes",
            "unique_files",
            "operations_per_second",
        ]
        
        return [features.get(f, 0.0) for f in feature_order]
    
    def get_top_contributors(self, features: Dict, top_n: int = 3) -> List[tuple]:
        """
        Get the top N features contributing to ransomware detection.
        
        Returns:
            List of (feature_name, value, explanation) tuples
        """
        # Feature importance weights (based on research papers)
        importance = {
            "crypto_api_count": (5.0, "Cryptographic API calls detected"),
            "file_write_count": (4.0, "High volume of file writes"),
            "write_read_ratio": (4.0, "Write-heavy operation pattern"),
            "avg_entropy": (3.5, "High entropy data (encryption)"),
            "extension_changes": (3.0, "File extensions being modified"),
            "file_delete_count": (2.5, "Files being deleted"),
            "operations_per_second": (2.0, "Rapid file operations"),
        }
        
        # Calculate weighted scores
        scores = []
        for feat, (weight, explanation) in importance.items():
            value = features.get(feat, 0)
            if value > 0:
                scores.append((feat, value, weight * value, explanation))
        
        # Sort by weighted score
        scores.sort(key=lambda x: x[2], reverse=True)
        
        # Return top N
        return [(name, value, exp) for name, value, _, exp in scores[:top_n]]


class MonitoredFileOperations:
    """
    Context manager for monitored file operations.
    Wraps standard file operations with automatic logging.
    """
    
    def __init__(self, monitor: BehaviorMonitor):
        self.monitor = monitor
        self.entropy_calculator = FeatureExtractor()
        
    def read_file(self, file_path: str) -> bytes:
        """Read a file and log the operation."""
        with open(file_path, 'rb') as f:
            data = f.read()
        
        entropy = self.entropy_calculator.calculate_entropy(data)
        self.monitor.log_operation(
            api_call="ReadFile",
            file_path=file_path,
            params={"size": len(data), "entropy": entropy}
        )
        
        return data
    
    def write_file(self, file_path: str, data: bytes, 
                   original_path: str = None) -> None:
        """Write to a file and log the operation."""
        # Check for extension change
        extension_changed = False
        if original_path:
            orig_ext = os.path.splitext(original_path)[1]
            new_ext = os.path.splitext(file_path)[1]
            extension_changed = orig_ext != new_ext
        
        entropy = self.entropy_calculator.calculate_entropy(data)
        
        with open(file_path, 'wb') as f:
            f.write(data)
        
        self.monitor.log_operation(
            api_call="WriteFile",
            file_path=file_path,
            params={
                "size": len(data), 
                "entropy": entropy,
                "extension_changed": extension_changed
            }
        )
    
    def delete_file(self, file_path: str) -> None:
        """Delete a file and log the operation."""
        if os.path.exists(file_path):
            os.remove(file_path)
        
        self.monitor.log_operation(
            api_call="DeleteFile",
            file_path=file_path,
            params={}
        )
    
    def create_file(self, file_path: str) -> None:
        """Create/touch a file and log the operation."""
        with open(file_path, 'a'):
            pass
        
        self.monitor.log_operation(
            api_call="CreateFile",
            file_path=file_path,
            params={}
        )
    
    def list_directory(self, dir_path: str) -> List[str]:
        """List directory contents and log the operation."""
        files = []
        
        for root, dirs, filenames in os.walk(dir_path):
            for filename in filenames:
                files.append(os.path.join(root, filename))
        
        self.monitor.log_operation(
            api_call="FindFirstFile",  # Windows API name for dir listing
            file_path=dir_path,
            params={"file_count": len(files)}
        )
        
        return files
    
    def generate_random_key(self, size: int = 32) -> bytes:
        """Generate random key material and log the crypto operation."""
        key = os.urandom(size)
        
        self.monitor.log_operation(
            api_call="CryptGenRandom",
            file_path="",
            params={"key_size": size}
        )
        
        return key


# Global monitor instance for easy access
_global_monitor = None


def get_monitor() -> BehaviorMonitor:
    """Get or create the global monitor instance."""
    global _global_monitor
    if _global_monitor is None:
        _global_monitor = BehaviorMonitor()
    return _global_monitor


def get_monitored_ops() -> MonitoredFileOperations:
    """Get monitored file operations with the global monitor."""
    return MonitoredFileOperations(get_monitor())


if __name__ == "__main__":
    # Test the monitor
    print("Testing Behavior Monitor...")
    
    monitor = BehaviorMonitor()
    monitor.clear_log()
    
    # Simulate some operations
    ops = MonitoredFileOperations(monitor)
    
    print("\n[TEST] Logging sample operations...")
    ops.generate_random_key(32)
    monitor.log_operation("WriteFile", "test.txt", {"size": 1024, "entropy": 7.8})
    monitor.log_operation("WriteFile", "test2.txt", {"size": 2048, "entropy": 7.9})
    monitor.log_operation("ReadFile", "config.txt", {"size": 512, "entropy": 4.2})
    monitor.log_operation("DeleteFile", "test.txt")
    
    # Extract features
    extractor = FeatureExtractor()
    operations = monitor.get_recent_operations()
    features = extractor.extract_features_from_operations(operations)
    
    print("\n[TEST] Extracted Features:")
    for name, value in features.items():
        print(f"       {name}: {value}")
    
    print("\n[TEST] Top Contributors:")
    contributors = extractor.get_top_contributors(features)
    for name, value, explanation in contributors:
        print(f"       {name} ({value}): {explanation}")
    
    print("\n[TEST] Monitor test complete!")
