"""
Threat Database Loader for Static File Blocking
Loads comprehensive ransomware and trojan database for blocking
"""
import os
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from antivirus.static_blocker import StaticFileBlocker, get_static_blocker

def load_threat_database(database_path: str = None):
    """
    Load threat database and populate static blocker.
    
    Args:
        database_path: Path to threat database JSON file
        
    Returns:
        StaticFileBlocker instance populated with threat data
    """
    if database_path is None:
        database_path = "antivirus/threat_database.json"
    
    # Get blocker instance
    blocker = get_static_blocker()
    
    print("=" * 60)
    print("LOADING THREAT DATABASE")
    print("=" * 60)
    
    try:
        # Load database
        with open(database_path, 'r') as f:
            db = json.load(f)
        
        print(f"[DATABASE] Loaded from: {database_path}")
        
        # Load ransomware families
        if "ransomware_families" in db:
            ransomware_count = 0
            for family_name, family_data in db["ransomware_families"].items():
                print(f"\n[RANSOMWARE] Loading {family_name}:")
                
                # Add file patterns
                for pattern in family_data.get("file_patterns", []):
                    blocker.add_pattern(pattern)
                    ransomware_count += 1
                    print(f"  Added pattern: {pattern}")
                
                # Add process names
                for process in family_data.get("process_names", []):
                    blocker.add_process_name(process)
                    ransomware_count += 1
                    print(f"  Added process: {process}")
                
                # Add known hashes
                for hash_val, description in family_data.get("known_hashes", {}).items():
                    blocker.add_hash(hash_val, f"{family_name}: {description}")
                    ransomware_count += 1
                    print(f"  Added hash: {hash_val[:16]}... ({description})")
            
            print(f"[RANSOMWARE] Added {ransomware_count} indicators")
        
        # Load trojan families
        if "trojan_families" in db:
            trojan_count = 0
            for family_name, family_data in db["trojan_families"].items():
                print(f"\n[TROJAN] Loading {family_name}:")
                
                # Add file patterns
                for pattern in family_data.get("file_patterns", []):
                    blocker.add_pattern(pattern)
                    trojan_count += 1
                    print(f"  Added pattern: {pattern}")
                
                # Add process names
                for process in family_data.get("process_names", []):
                    blocker.add_process_name(process)
                    trojan_count += 1
                    print(f"  Added process: {process}")
            
            print(f"[TROJAN] Added {trojan_count} indicators")
        
        # Load generic indicators
        if "generic_indicators" in db:
            generic = db["generic_indicators"]
            generic_count = 0
            
            print("\n[GENERIC] Loading generic indicators:")
            
            # Add suspicious extensions
            for ext in generic.get("suspicious_extensions", []):
                blocker.add_extension(ext)
                generic_count += 1
                print(f"  Added extension: {ext}")
            
            # Add suspicious filenames
            for pattern in generic.get("suspicious_filenames", []):
                blocker.add_pattern(pattern)
                generic_count += 1
                print(f"  Added filename pattern: {pattern}")
            
            # Add suspicious process names
            for process in generic.get("suspicious_process_names", []):
                blocker.add_process_name(process)
                generic_count += 1
                print(f"  Added process pattern: {process}")
            
            print(f"[GENERIC] Added {generic_count} indicators")
        
        # Load block lists
        if "block_lists" in db:
            block_lists = db["block_lists"]
            block_count = 0
            
            print("\n[BLOCK LISTS] Loading additional block lists:")
            
            # Add malicious hashes
            for hash_val, description in block_lists.get("malicious_hashes", {}).items():
                blocker.add_hash(hash_val, description)
                block_count += 1
                print(f"  Added hash: {hash_val[:16]}... ({description})")
            
            print(f"[BLOCK LISTS] Added {block_count} items")
        
        # Save updated block lists
        blocker.save_block_lists()
        
        # Show statistics
        stats = blocker.get_statistics()
        print("\n" + "=" * 60)
        print("THREAT DATABASE LOADING COMPLETE")
        print("=" * 60)
        print(f"Total signatures: {stats['block_lists']['signatures']}")
        print(f"Total hashes: {stats['block_lists']['hashes']}")
        print(f"Total patterns: {stats['block_lists']['patterns']}")
        print(f"Total extensions: {stats['block_lists']['extensions']}")
        print(f"Total processes: {stats['block_lists']['processes']}")
        print("=" * 60)
        
        return blocker
        
    except FileNotFoundError:
        print(f"[ERROR] Database file not found: {database_path}")
        return blocker
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in database: {e}")
        return blocker
    except Exception as e:
        print(f"[ERROR] Failed to load database: {e}")
        return blocker

def analyze_dataset(dataset_path: str = None):
    """
    Analyze the realistic ransomware dataset and extract threat indicators.
    
    Args:
        dataset_path: Path to ransomware dataset CSV
        
    Returns:
        Dictionary with extracted indicators
    """
    if dataset_path is None:
        dataset_path = "ransomware_dataset_realistic.csv"
    
    try:
        import pandas as pd
        
        print(f"\n[DATASET] Analyzing: {dataset_path}")
        
        # Load dataset
        df = pd.read_csv(dataset_path)
        
        # Get unique sources (ransomware families)
        families = df['source'].unique()
        print(f"[DATASET] Found {len(families)} ransomware families:")
        for family in families:
            if family not in ['Office', 'Utility', 'Browser', 'Game', 'System']:
                print(f"  - {family}")
        
        # Extract behavioral indicators
        indicators = {
            "families": [],
            "common_apis": [],
            "file_behaviors": []
        }
        
        # For actual ransomware samples, extract API call patterns
        ransomware_samples = df[df['label'] == 1]  # Assuming 1 = malicious
        
        if len(ransomware_samples) > 0:
            print(f"\n[DATASET] Analyzing {len(ransomware_samples)} ransomware samples...")
            
            # Get average API call counts for ransomware
            api_columns = [col for col in df.columns if col not in ['file_name', 'label', 'source']]
            
            avg_calls = ransomware_samples[api_columns].mean()
            top_apis = avg_calls.nlargest(10)
            
            print("[DATASET] Top 10 API calls in ransomware:")
            for api, count in top_apis.items():
                print(f"  {api}: {count:.1f}")
                indicators["common_apis"].append(api)
        
        return indicators
        
    except Exception as e:
        print(f"[DATASET] Error analyzing dataset: {e}")
        return {}

def create_comprehensive_database():
    """
    Create a comprehensive threat database combining:
    1. Predefined threat database
    2. Indicators from realistic dataset
    3. Additional known ransomware families
    """
    print("=" * 60)
    print("CREATING COMPREHENSIVE THREAT DATABASE")
    print("=" * 60)
    
    # Load existing database
    blocker = load_threat_database()
    
    # Analyze dataset for additional indicators
    dataset_indicators = analyze_dataset()
    
    # Add dataset-derived indicators
    if dataset_indicators.get("common_apis"):
        print("\n[ENHANCEMENT] Adding dataset-derived indicators...")
        for api in dataset_indicators["common_apis"][:5]:  # Top 5 APIs
            # Create behavioral signatures based on API combinations
            signature = f"High {api} usage with file operations"
            blocker.add_signature(signature)
            print(f"  Added behavioral signature: {signature}")
    
    # Add additional known ransomware families
    additional_families = {
        "CryptoLocker": {
            "patterns": ["*.locked", "DECRYPT_INSTRUCTION.TXT"],
            "processes": ["cryptolocker.exe"],
            "extensions": [".locked"]
        },
        "Cryptowall": {
            "patterns": ["*_DECRYPT_INFO_*", "HELP_DECRYPT.PNG"],
            "processes": ["cryptowall.exe"],
            "extensions": [".enc"]
        },
        "Petya": {
            "patterns": ["README_FOR_DECRYPT.txt"],
            "processes": ["petya.exe", "perfc.dat"],
            "extensions": []
        }
    }
    
    print("\n[ENHANCEMENT] Adding additional ransomware families:")
    for family, data in additional_families.items():
        print(f"\n  {family}:")
        for pattern in data["patterns"]:
            blocker.add_pattern(pattern)
            print(f"    Added pattern: {pattern}")
        for process in data["processes"]:
            blocker.add_process_name(process)
            print(f"    Added process: {process}")
        for ext in data["extensions"]:
            blocker.add_extension(ext)
            print(f"    Added extension: {ext}")
    
    # Save enhanced database
    blocker.save_block_lists()
    
    # Final statistics
    stats = blocker.get_statistics()
    print("\n" + "=" * 60)
    print("COMPREHENSIVE DATABASE CREATED")
    print("=" * 60)
    print(f"Total signatures: {stats['block_lists']['signatures']}")
    print(f"Total hashes: {stats['block_lists']['hashes']}")
    print(f"Total patterns: {stats['block_lists']['patterns']}")
    print(f"Total extensions: {stats['block_lists']['extensions']}")
    print(f"Total processes: {stats['block_lists']['processes']}")
    print("=" * 60)
    
    return blocker

def main():
    """Main function to run database loading/enhancement."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Threat Database Loader")
    parser.add_argument("--load", action="store_true", help="Load existing database")
    parser.add_argument("--enhance", action="store_true", help="Create comprehensive database")
    parser.add_argument("--analyze", action="store_true", help="Analyze dataset only")
    parser.add_argument("--database", type=str, help="Custom database path")
    parser.add_argument("--dataset", type=str, help="Custom dataset path")
    
    args = parser.parse_args()
    
    if args.analyze:
        analyze_dataset(args.dataset)
    elif args.enhance:
        create_comprehensive_database()
    elif args.load:
        load_threat_database(args.database)
    else:
        # Default: create comprehensive database
        create_comprehensive_database()

if __name__ == "__main__":
    main()
