"""
Guardian Daemon - Real-time Ransomware Detection System
Monitors behavioral logs and provides threat scores using the trained 1D-CNN model
Now with ACTIVE PROTECTION - kills malicious processes when detected!
Also includes FILE RECOVERY - attempts to decrypt files after stopping ransomware!
"""
import os
import sys
import time
import json
import signal
import psutil
import threading
import numpy as np
import glob
import base64
from datetime import datetime
from typing import Dict, List, Optional, Callable
from collections import deque
from concurrent.futures import ThreadPoolExecutor

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    MODEL_PATH, BEHAVIORAL_LOG_PATH, 
    TIME_WINDOW_SECONDS, MAX_LOG_LINES,
    ALERT_THRESHOLD, WARNING_THRESHOLD, SAFE_THRESHOLD,
    SCORE_HISTORY_LENGTH, TEST_FILES_DIR, ENCRYPTION_EXTENSION
)
from monitor.monitor import BehaviorMonitor, FeatureExtractor
from antivirus.static_blocker import StaticFileBlocker, get_static_blocker


class ThreatScorer:
    """
    Calculates threat scores using the trained model and behavioral features.
    Thread-safe implementation with model caching.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern for model caching."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self.model = None
        self.scaler = None
        self.feature_extractor = FeatureExtractor()
        self._model_lock = threading.Lock()
        self._load_model()
        self._initialized = True
    
    def _load_model(self):
        """Load the trained model and preprocessors."""
        try:
            # Try to load TensorFlow model
            if os.path.exists(MODEL_PATH):
                os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
                import tensorflow as tf
                tf.get_logger().setLevel('ERROR')
                from tensorflow.keras.models import load_model
                self.model = load_model(MODEL_PATH, compile=False)
                # Recompile to avoid warnings
                self.model.compile(optimizer='adam', loss='binary_crossentropy')
                print(f"[INFO] Model loaded from: {MODEL_PATH}")
            else:
                print(f"[WARNING] Model not found at: {MODEL_PATH}")
                print("[INFO] Using heuristic-based scoring as fallback")
        except Exception as e:
            print(f"[WARNING] Failed to load model: {e}")
            print("[INFO] Using heuristic-based scoring as fallback")
    
    def calculate_heuristic_score(self, features: Dict) -> float:
        """
        Calculate threat score using heuristics when model is unavailable.
        Based on behavioral indicators from research papers.
        """
        score = 0.0
        
        # Crypto API usage (strong indicator)
        if features.get("crypto_api_count", 0) > 0:
            score += min(features["crypto_api_count"] * 0.15, 0.45)
        
        # Write/Read ratio (ransomware is write-heavy)
        wr_ratio = features.get("write_read_ratio", 0)
        if wr_ratio > 2.0:
            score += min(wr_ratio * 0.05, 0.2)
        
        # High entropy data (encryption indicator)
        entropy = features.get("avg_entropy", 0)
        if entropy > 6.0:  # Random/encrypted data has entropy ~7-8
            score += (entropy - 6.0) * 0.1
        
        # Extension changes (ransomware modifies extensions)
        if features.get("extension_changes", 0) > 0:
            score += min(features["extension_changes"] * 0.1, 0.3)
        
        # High operation rate
        ops_per_sec = features.get("operations_per_second", 0)
        if ops_per_sec > 10:
            score += min((ops_per_sec - 10) * 0.01, 0.15)
        
        # File deletions (ransomware deletes originals)
        if features.get("file_delete_count", 0) > 0:
            score += min(features["file_delete_count"] * 0.05, 0.2)
        
        return min(score, 1.0)
    
    def calculate_ml_score(self, features: Dict) -> float:
        """
        Calculate threat score using the trained ML model.
        Thread-safe implementation.
        """
        if self.model is None:
            return self.calculate_heuristic_score(features)
        
        try:
            # Convert features to vector
            feature_vector = self.feature_extractor.features_to_vector(features)
            
            # Reshape for model input
            X = np.array(feature_vector).reshape(1, -1, 1)
            
            # Thread-safe prediction
            with self._model_lock:
                score = self.model.predict(X, verbose=0)[0][0]
            return float(score)
            
        except Exception as e:
            return self.calculate_heuristic_score(features)
    
    def get_score(self, operations: List[Dict]) -> Dict:
        """
        Calculate comprehensive threat score from operations.
        
        Returns:
            Dictionary with score and explanation
        """
        # Extract features
        features = self.feature_extractor.extract_features_from_operations(operations)
        
        # Calculate scores
        ml_score = self.calculate_ml_score(features)
        heuristic_score = self.calculate_heuristic_score(features)
        
        # Combined score (weighted average if both available)
        if self.model is not None:
            final_score = ml_score * 0.7 + heuristic_score * 0.3
        else:
            final_score = heuristic_score
        
        # Get top contributors
        contributors = self.feature_extractor.get_top_contributors(features)
        
        # Determine threat level
        if final_score >= ALERT_THRESHOLD:
            level = "CRITICAL"
        elif final_score >= WARNING_THRESHOLD:
            level = "WARNING"
        elif final_score >= SAFE_THRESHOLD:
            level = "ELEVATED"
        else:
            level = "SAFE"
        
        return {
            "score": final_score,
            "ml_score": ml_score,
            "heuristic_score": heuristic_score,
            "level": level,
            "features": features,
            "contributors": contributors,
            "timestamp": datetime.now().isoformat()
        }


class FileRecovery:
    """
    Attempts to recover files encrypted by ransomware.
    Works by:
    1. Finding encrypted files (.locked extension)
    2. Attempting decryption with captured/brute-forced keys
    3. Restoring original files
    """
    
    # Known key storage location (ransomware simulator saves key here for demo)
    KEY_STORAGE_PATH = os.path.join(os.path.dirname(BEHAVIORAL_LOG_PATH), "recovery_key.bin")
    
    def __init__(self):
        self.recovered_files = []
        self.failed_files = []
        self.encryption_extension = ENCRYPTION_EXTENSION
    
    def find_encrypted_files(self, directory: str = None) -> List[str]:
        """Find all encrypted files in the target directory or system-wide."""
        if directory:
            # Specific directory scan (for targeted recovery)
            pattern = os.path.join(directory, f"**/*{self.encryption_extension}")
            encrypted_files = glob.glob(pattern, recursive=True)
            
            # Also check for .crypted files (variant B)
            pattern2 = os.path.join(directory, "**/*.crypted")
            encrypted_files.extend(glob.glob(pattern2, recursive=True))
        else:
            # System-wide scan for encrypted files (safety measure)
            # Scan common user directories
            user_dirs = [
                os.path.expanduser("~\\Desktop"),
                os.path.expanduser("~\\Documents"),
                os.path.expanduser("~\\Downloads"),
                os.path.expanduser("~\\Pictures"),
                os.path.expanduser("~\\Music"),
                os.path.expanduser("~\\Videos"),
                TEST_FILES_DIR  # Include test files directory
            ]
            
            encrypted_files = []
            for user_dir in user_dirs:
                if os.path.exists(user_dir):
                    pattern = os.path.join(user_dir, f"**/*{self.encryption_extension}")
                    encrypted_files.extend(glob.glob(pattern, recursive=True))
                    
                    # Also check for .crypted files (variant B)
                    pattern2 = os.path.join(user_dir, "**/*.crypted")
                    encrypted_files.extend(glob.glob(pattern2, recursive=True))
        
        return encrypted_files
    
    def extract_key_from_logs(self) -> Optional[bytes]:
        """
        Attempt to extract encryption key from behavioral logs.
        In a real scenario, this would involve memory forensics.
        For demo, we check if ransomware saved a recovery key.
        """
        # Check for saved recovery key (from our simulator)
        if os.path.exists(self.KEY_STORAGE_PATH):
            try:
                with open(self.KEY_STORAGE_PATH, 'rb') as f:
                    key = f.read()
                print(f"[RECOVERY] Found encryption key in recovery storage")
                return key
            except:
                pass
        
        # Try to generate key from logged CryptGenRandom params
        # This simulates key extraction from memory/logs
        try:
            monitor = BehaviorMonitor()
            operations = monitor.get_recent_operations(200)
            
            for op in operations:
                if op.get("api_call") == "CryptGenRandom":
                    # In our simulation, we can reconstruct the key
                    # Real ransomware analysis would require memory forensics
                    key_size = op.get("params", {}).get("key_size", 32)
                    print(f"[RECOVERY] Detected key generation (size: {key_size})")
                    break
        except:
            pass
        
        return None
    
    def attempt_decryption(self, encrypted_file: str, key: bytes) -> bool:
        """
        Attempt to decrypt a single file.
        Returns True if successful.
        """
        try:
            from cryptography.fernet import Fernet, InvalidToken
            
            # Read encrypted data
            with open(encrypted_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Try decryption
            cipher = Fernet(key)
            decrypted_data = cipher.decrypt(encrypted_data)
            
            # Determine original filename
            if encrypted_file.endswith(self.encryption_extension):
                original_file = encrypted_file[:-len(self.encryption_extension)]
            elif encrypted_file.endswith('.crypted'):
                original_file = encrypted_file[:-8]  # Remove .crypted
            else:
                original_file = encrypted_file + ".recovered"
            
            # Write decrypted data
            with open(original_file, 'wb') as f:
                f.write(decrypted_data)
            
            # Remove encrypted file
            os.remove(encrypted_file)
            
            self.recovered_files.append({
                "encrypted": encrypted_file,
                "recovered": original_file,
                "size": len(decrypted_data)
            })
            
            return True
            
        except InvalidToken:
            # Wrong key
            return False
        except Exception as e:
            self.failed_files.append({
                "file": encrypted_file,
                "error": str(e)
            })
            return False
    
    def recover_all_files(self, directory: str = None, key: bytes = None) -> Dict:
        """
        Attempt to recover all encrypted files in a directory.
        
        Returns:
            Dictionary with recovery statistics
        """
        print("\n" + "=" * 60)
        print("  FILE RECOVERY SYSTEM")
        print("=" * 60)
        
        # Find encrypted files
        encrypted_files = self.find_encrypted_files(directory)
        
        if not encrypted_files:
            print("[RECOVERY] No encrypted files found.")
            return {"found": 0, "recovered": 0, "failed": 0}
        
        print(f"[RECOVERY] Found {len(encrypted_files)} encrypted file(s)")
        
        # Get decryption key
        if key is None:
            key = self.extract_key_from_logs()
        
        if key is None:
            print("[RECOVERY] Could not obtain decryption key")
            print("[RECOVERY] Attempting brute-force key recovery...")
            # For demo, try common test keys
            key = self._try_recover_key()
        
        if key is None:
            print("[RECOVERY] Key recovery failed. Manual intervention required.")
            return {
                "found": len(encrypted_files),
                "recovered": 0,
                "failed": len(encrypted_files)
            }
        
        # Attempt decryption
        print(f"\n[RECOVERY] Attempting decryption...")
        
        for i, enc_file in enumerate(encrypted_files, 1):
            filename = os.path.basename(enc_file)
            print(f"  [{i}/{len(encrypted_files)}] Decrypting: {filename}", end=" ")
            
            if self.attempt_decryption(enc_file, key):
                print("SUCCESS")
            else:
                print("FAILED")
        
        # Summary
        result = {
            "found": len(encrypted_files),
            "recovered": len(self.recovered_files),
            "failed": len(self.failed_files)
        }
        
        print(f"\n[RECOVERY] Results:")
        print(f"           Files found: {result['found']}")
        print(f"           Recovered: {result['recovered']}")
        print(f"           Failed: {result['failed']}")
        print("=" * 60 + "\n")
        
        return result
    
    def _try_recover_key(self) -> Optional[bytes]:
        """
        Attempt to recover key through various methods.
        For demo purposes, this checks common locations.
        """
        # Check if ransomware simulator left a key file
        key_locations = [
            self.KEY_STORAGE_PATH,
            os.path.join(TEST_FILES_DIR, ".key"),
            os.path.join(os.path.dirname(TEST_FILES_DIR), ".encryption_key"),
        ]
        
        for loc in key_locations:
            if os.path.exists(loc):
                try:
                    with open(loc, 'rb') as f:
                        return f.read()
                except:
                    continue
        
        return None
    
    def save_key_for_recovery(self, key: bytes):
        """Save a key for later recovery (used by simulator)."""
        os.makedirs(os.path.dirname(self.KEY_STORAGE_PATH), exist_ok=True)
        with open(self.KEY_STORAGE_PATH, 'wb') as f:
            f.write(key)


class GuardianDaemon:
    """
    Real-time monitoring daemon that watches behavioral logs
    and calculates threat scores. NOW WITH ACTIVE PROTECTION!
    Also includes automatic FILE RECOVERY after stopping ransomware!
    """
    
    def __init__(self, callback: Callable = None, active_protection: bool = True):
        self.monitor = BehaviorMonitor()
        self.scorer = ThreatScorer()
        self.recovery = FileRecovery()
        self.static_blocker = get_static_blocker()  # Static file blocking
        self.callback = callback
        self.active_protection = active_protection
        
        self.running = False
        self.score_history = deque(maxlen=SCORE_HISTORY_LENGTH)
        self.last_score = None
        self.detected_threats = []
        self.terminated_processes = []
        self.recovery_results = None
        
        self._thread = None
        self._lock = threading.Lock()
        self._executor = ThreadPoolExecutor(max_workers=4)
        
        # Faster monitoring interval for active protection
        self.check_interval = 0.2 if active_protection else TIME_WINDOW_SECONDS
    
    def start(self):
        """Start the guardian daemon."""
        if self.running:
            return
        
        self.running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        
        protection_status = "ENABLED" if self.active_protection else "DISABLED"
        
        print("\n" + "=" * 60)
        print("  GUARDIAN DAEMON - ACTIVE")
        print("=" * 60)
        print(f"  Monitoring: {BEHAVIORAL_LOG_PATH}")
        print(f"  Alert threshold: {ALERT_THRESHOLD}")
        print(f"  Check interval: {self.check_interval}s")
        print(f"  Active Protection: {protection_status}")
        print("=" * 60 + "\n")
    
    def stop(self):
        """Stop the guardian daemon."""
        self.running = False
        if self._thread:
            self._thread.join(timeout=2)
        self._executor.shutdown(wait=False)
        print("\n[INFO] Guardian daemon stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop - optimized for speed."""
        while self.running:
            try:
                # Get recent operations
                operations = self.monitor.get_recent_operations(MAX_LOG_LINES)
                
                if operations:
                    # Calculate threat score in thread pool for speed
                    future = self._executor.submit(self.scorer.get_score, operations)
                    result = future.result(timeout=1.0)
                    
                    with self._lock:
                        self.last_score = result
                        self.score_history.append({
                            "timestamp": result["timestamp"],
                            "score": result["score"],
                            "level": result["level"]
                        })
                    
                    # Check for threat and take action
                    if result["score"] >= ALERT_THRESHOLD:
                        self._handle_threat(result, operations)
                    
                    # Call callback if provided
                    if self.callback:
                        self._executor.submit(self.callback, result)
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                time.sleep(0.5)
    
    def _handle_threat(self, result: Dict, operations: List[Dict]):
        """Handle detected threat - TERMINATE MALICIOUS PROCESS AND RECOVER FILES!"""
        threat_info = {
            "timestamp": result["timestamp"],
            "score": result["score"],
            "contributors": result["contributors"]
        }
        
        self.detected_threats.append(threat_info)
        
        print("\n" + "!" * 60)
        print("  RANSOMWARE THREAT DETECTED!")
        print("!" * 60)
        print(f"  Threat Score: {result['score']:.2%}")
        print(f"  Level: {result['level']}")
        print("\n  Contributing Factors:")
        for name, value, explanation in result["contributors"]:
            print(f"    - {explanation} ({name}: {value})")
        
        # ACTIVE PROTECTION: Kill the malicious process
        if self.active_protection:
            killed = self._terminate_malicious_processes(operations)
            if killed:
                print(f"\n  ACTION TAKEN: Terminated {len(killed)} malicious process(es)!")
                self.terminated_processes.extend(killed)
                
                # Wait a moment for process to fully terminate
                time.sleep(0.5)
                
                # ATTEMPT FILE RECOVERY
                print("\n  Initiating automatic file recovery...")
                self.recovery_results = self.recovery.recover_all_files()
                
                if self.recovery_results and self.recovery_results.get("recovered", 0) > 0:
                    print(f"  FILES RECOVERED: {self.recovery_results['recovered']} file(s) restored!")
            else:
                print("\n  WARNING: Could not identify process to terminate")
        
        print("!" * 60 + "\n")
    
    def _terminate_malicious_processes(self, operations: List[Dict]) -> List[int]:
        """
        Identify and terminate malicious processes based on logged PIDs.
        Returns list of terminated PIDs.
        """
        killed_pids = []
        
        # Get unique PIDs from recent operations
        pids_in_ops = set()
        for op in operations:
            pid = op.get("pid")
            if pid and pid != os.getpid():  # Don't kill ourselves!
                pids_in_ops.add(pid)
        
        # Current process ID to avoid killing guardian
        current_pid = os.getpid()
        parent_pid = os.getppid()
        
        for pid in pids_in_ops:
            # Skip system processes and our own processes
            if pid in [current_pid, parent_pid, 0, 1, 4]:
                continue
                
            try:
                process = psutil.Process(pid)
                proc_name = process.name().lower()
                
                # Don't kill system processes or known safe processes
                safe_processes = ['python', 'streamlit', 'explorer', 'cmd', 'powershell',
                                 'code', 'system', 'services', 'svchost', 'guardian']
                
                # Check if it's a simulator (ransomware_sim)
                cmdline = ' '.join(process.cmdline()).lower()
                
                if 'ransomware' in cmdline or 'encrypt' in cmdline:
                    print(f"\n  [KILL] Terminating suspicious process: {proc_name} (PID: {pid})")
                    process.terminate()
                    
                    # Wait a bit then force kill if still alive
                    try:
                        process.wait(timeout=1)
                    except psutil.TimeoutExpired:
                        process.kill()
                    
                    killed_pids.append(pid)
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
            except Exception as e:
                continue
        
        return killed_pids
    
    def get_current_score(self) -> Optional[Dict]:
        """Get the most recent threat score."""
        with self._lock:
            return self.last_score
    
    def get_score_history(self) -> List[Dict]:
        """Get score history."""
        with self._lock:
            return list(self.score_history)
    
    def get_status(self) -> Dict:
        """Get daemon status."""
        return {
            "running": self.running,
            "threats_detected": len(self.detected_threats),
            "current_score": self.last_score,
            "history_length": len(self.score_history)
        }


# Shared daemon instance for dashboard integration
_daemon_instance = None
_daemon_lock = threading.Lock()


def get_daemon() -> GuardianDaemon:
    """Get or create the shared daemon instance."""
    global _daemon_instance
    with _daemon_lock:
        if _daemon_instance is None:
            _daemon_instance = GuardianDaemon()
        return _daemon_instance


def start_daemon():
    """Start the shared daemon."""
    daemon = get_daemon()
    daemon.start()
    return daemon


def stop_daemon():
    """Stop the shared daemon."""
    global _daemon_instance
    with _daemon_lock:
        if _daemon_instance:
            _daemon_instance.stop()
            _daemon_instance = None


def main():
    """Run the guardian daemon standalone."""
    print("\n" + "=" * 60)
    print("  ZERO-DAY RANSOMWARE GUARDIAN")
    print("  Real-time Behavioral Detection System")
    print("=" * 60)
    
    # Create daemon with console output callback
    def console_callback(result):
        score = result["score"]
        level = result["level"]
        
        # Color coding for terminal
        if level == "CRITICAL":
            status = f"[CRITICAL] {score:.1%}"
        elif level == "WARNING":
            status = f"[WARNING]  {score:.1%}"
        elif level == "ELEVATED":
            status = f"[ELEVATED] {score:.1%}"
        else:
            status = f"[SAFE]     {score:.1%}"
        
        # Simple status line
        print(f"\r{status} | Ops: {result['features'].get('total_operations', 0):3d} | "
              f"Crypto: {result['features'].get('crypto_api_count', 0)} | "
              f"Writes: {result['features'].get('file_write_count', 0)} | "
              f"Entropy: {result['features'].get('avg_entropy', 0):.1f}    ", end="")
    
    daemon = GuardianDaemon(callback=console_callback)
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n\n[INFO] Shutting down...")
        daemon.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start monitoring
    daemon.start()
    
    # Keep running
    print("\nMonitoring... (Press Ctrl+C to stop)\n")
    while daemon.running:
        time.sleep(1)


if __name__ == "__main__":
    main()
