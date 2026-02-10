"""
Configuration file for Zero-Day Ransomware Detection System
"""
import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
TEST_FILES_DIR = os.path.join(DATA_DIR, "test_files")
MODEL_DIR = os.path.join(BASE_DIR, "model")
MONITOR_DIR = os.path.join(BASE_DIR, "monitor")
ANTIVIRUS_DIR = os.path.join(BASE_DIR, "antivirus")

# Dataset configuration
DATASET_URL = "https://github.com/rissgrouphub/ransomwaredataset2016/raw/main/RansomwareData.zip"
DATASET_ZIP = os.path.join(RAW_DATA_DIR, "RansomwareData.zip")

# Feature engineering
N_FEATURES = 50  # Number of features after chi-squared selection
FEATURE_SCALER_PATH = os.path.join(PROCESSED_DATA_DIR, "scaler.pkl")
FEATURE_SELECTOR_PATH = os.path.join(PROCESSED_DATA_DIR, "feature_selector.pkl")
SELECTED_FEATURES_PATH = os.path.join(PROCESSED_DATA_DIR, "selected_features.pkl")

# Ransomware families (from RISS dataset)
FAMILY_NAMES = {
    0: "Goodware",
    1: "Critroni",
    2: "CryptLocker",
    3: "CryptoWall",
    4: "KOLLAH",
    5: "Kovter",
    6: "Locker",
    7: "MATSNU",
    8: "PGPCODER",
    9: "Reveton",
    10: "TeslaCrypt",
    11: "Trojan-Ransom"
}

# Zero-day split configuration
# Training families (8 families)
TRAIN_FAMILIES = [1, 2, 3, 4, 5, 6, 7, 8]
# Test families (3 unseen families for zero-day simulation)
TEST_FAMILIES = [9, 10, 11]

# Model configuration
MODEL_PATH = os.path.join(MODEL_DIR, "ransomware_detector.h5")
EPOCHS = 50
BATCH_SIZE = 32
EARLY_STOPPING_PATIENCE = 10
VALIDATION_SPLIT = 0.2

# Monitor configuration
BEHAVIORAL_LOG_PATH = os.path.join(MONITOR_DIR, "behavioral_trace.log")
TIME_WINDOW_SECONDS = 1.0
MAX_LOG_LINES = 50

# Detection thresholds
ALERT_THRESHOLD = 0.9
WARNING_THRESHOLD = 0.7
SAFE_THRESHOLD = 0.3

# API categories for feature extraction
API_CATEGORIES = {
    "crypto": ["CryptEncrypt", "CryptDecrypt", "CryptGenKey", "CryptAcquireContext",
               "CryptCreateHash", "CryptHashData", "CryptDeriveKey", "CryptGenRandom"],
    "file_write": ["WriteFile", "NtWriteFile", "WriteFileEx", "fwrite", "write"],
    "file_read": ["ReadFile", "NtReadFile", "ReadFileEx", "fread", "read"],
    "file_delete": ["DeleteFile", "NtDeleteFile", "RemoveDirectory", "unlink"],
    "file_create": ["CreateFile", "NtCreateFile", "OpenFile", "fopen", "open"],
    "registry": ["RegSetValue", "RegCreateKey", "RegDeleteKey", "RegOpenKey"],
    "process": ["CreateProcess", "TerminateProcess", "OpenProcess", "NtTerminateProcess"]
}

# Dashboard configuration
DASHBOARD_REFRESH_INTERVAL = 0.5  # seconds
SCORE_HISTORY_LENGTH = 100

# Demo configuration
DEMO_DELAY = 0.5  # seconds between file operations for visibility

# Encryption configuration for simulator
ENCRYPTION_EXTENSION = ".locked"
RANSOM_NOTE_FILENAME = "README_DECRYPT.txt"
