"""
Script to download and extract the RISS Ransomware Dataset
"""
import os
import sys
import zipfile
import requests
from io import BytesIO

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import RAW_DATA_DIR, DATASET_URL, DATASET_ZIP


def download_dataset():
    """Download the RISS ransomware dataset from GitHub."""
    print("=" * 60)
    print("RISS Ransomware Dataset Downloader")
    print("=" * 60)
    
    # Create directories if they don't exist
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    
    # Check if already downloaded
    if os.path.exists(os.path.join(RAW_DATA_DIR, "RansomwareData.csv")):
        print("[INFO] Dataset already exists. Skipping download.")
        return True
    
    print(f"\n[INFO] Downloading dataset from:")
    print(f"       {DATASET_URL}")
    print(f"\n[INFO] This may take a few minutes...")
    
    try:
        # Download the zip file
        response = requests.get(DATASET_URL, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        # Save to file
        with open(DATASET_ZIP, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r[DOWNLOAD] {percent:.1f}% ({downloaded}/{total_size} bytes)", end="")
        
        print(f"\n\n[SUCCESS] Downloaded to: {DATASET_ZIP}")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to download: {e}")
        print("\n[INFO] Please download manually from:")
        print("       https://github.com/rissgrouphub/ransomwaredataset2016")
        print(f"       Extract to: {RAW_DATA_DIR}")
        return False
    
    # Extract the zip file
    print("\n[INFO] Extracting dataset...")
    try:
        with zipfile.ZipFile(DATASET_ZIP, 'r') as zip_ref:
            zip_ref.extractall(RAW_DATA_DIR)
        print(f"[SUCCESS] Extracted to: {RAW_DATA_DIR}")
        
        # List extracted files
        print("\n[INFO] Extracted files:")
        for f in os.listdir(RAW_DATA_DIR):
            filepath = os.path.join(RAW_DATA_DIR, f)
            size = os.path.getsize(filepath)
            print(f"       - {f} ({size:,} bytes)")
            
    except Exception as e:
        print(f"[ERROR] Failed to extract: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("Dataset setup complete!")
    print("=" * 60)
    return True


def verify_dataset():
    """Verify that the dataset files exist and are valid."""
    print("\n[INFO] Verifying dataset...")
    
    required_files = ["RansomwareData.csv"]
    optional_files = ["VariableNames.txt", "IDS.txt", "Family Names ID.txt"]
    
    # Check for main data file (could be .csv or in extracted folder)
    data_found = False
    data_path = None
    
    # Check various possible locations
    possible_paths = [
        os.path.join(RAW_DATA_DIR, "RansomwareData.csv"),
        os.path.join(RAW_DATA_DIR, "ransomwaredata.csv"),
        os.path.join(RAW_DATA_DIR, "data.csv"),
    ]
    
    # Also check in subdirectories
    for root, dirs, files in os.walk(RAW_DATA_DIR):
        for f in files:
            if f.lower().endswith('.csv'):
                possible_paths.append(os.path.join(root, f))
    
    for path in possible_paths:
        if os.path.exists(path):
            data_found = True
            data_path = path
            print(f"[OK] Found data file: {path}")
            break
    
    if not data_found:
        print("[WARNING] Main dataset CSV not found.")
        print("[INFO] You may need to manually extract the dataset.")
        return None
    
    return data_path


if __name__ == "__main__":
    success = download_dataset()
    if success:
        data_path = verify_dataset()
        if data_path:
            print(f"\n[READY] Dataset is ready at: {data_path}")
        else:
            print("\n[ACTION] Please check the data/raw folder and ensure CSV file exists.")
