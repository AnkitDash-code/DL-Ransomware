"""
Setup Test Files for Demo
Creates sample files in the test_files directory for ransomware simulation
"""
import os
import sys
import random
import string

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TEST_FILES_DIR


def create_sample_text_file(filepath, content):
    """Create a text file with given content."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Created: {os.path.basename(filepath)}")


def create_sample_binary_file(filepath, size=1024):
    """Create a binary file with random content."""
    with open(filepath, 'wb') as f:
        f.write(os.urandom(size))
    print(f"  Created: {os.path.basename(filepath)} ({size} bytes)")


def setup_test_files():
    """Create sample test files for the demo."""
    print("\n" + "=" * 60)
    print("  SETTING UP TEST FILES")
    print("=" * 60)
    
    # Create test files directory
    os.makedirs(TEST_FILES_DIR, exist_ok=True)
    print(f"\n  Target directory: {TEST_FILES_DIR}\n")
    
    # Sample document content
    documents = {
        "Thesis.txt": """
CHAPTER 1: INTRODUCTION

This thesis explores the application of deep learning techniques for 
real-time detection of zero-day ransomware attacks. Traditional signature-based
antivirus solutions fail to detect novel malware variants, creating a critical
security gap in modern computing environments.

Our approach leverages behavioral analysis and 1D Convolutional Neural Networks
to identify ransomware based on its operational patterns rather than static
signatures, enabling detection of previously unseen ransomware families.

Keywords: Ransomware, Deep Learning, Zero-Day Detection, Behavioral Analysis
""",
        
        "Budget.txt": """
ANNUAL BUDGET REPORT 2026

Department: Information Technology
Period: January - December 2026

SUMMARY:
- Total Budget: $500,000
- Hardware: $150,000
- Software Licenses: $100,000
- Cloud Services: $120,000
- Security Systems: $80,000
- Training: $50,000

This document contains confidential financial information.
""",
        
        "Notes.txt": """
PROJECT NOTES - RANSOMWARE DETECTION SYSTEM

TODO:
[x] Implement 1D-CNN model architecture
[x] Create behavioral monitoring system
[x] Build Streamlit dashboard
[ ] Conduct extensive testing
[ ] Prepare presentation slides

IMPORTANT: Remember to demonstrate zero-day detection capability!
""",
        
        "Contacts.txt": """
IMPORTANT CONTACTS

John Smith - Project Supervisor
Email: john.smith@university.edu
Phone: +1 (555) 123-4567

Security Team Lead
Email: security@company.com
Emergency: +1 (555) 911-0000

This file contains personal information - CONFIDENTIAL
""",
        
        "Research_Data.txt": """
EXPERIMENTAL RESULTS - RANSOMWARE DETECTION

Model: 1D-CNN with Chi-Squared Feature Selection
Dataset: RISS Ransomware Dataset (1524 samples)
Features: 50 (reduced from 16,382)

RESULTS:
- Training Accuracy: 98.5%
- Validation Accuracy: 96.2%
- Zero-Day Test Accuracy: 94.1%
- False Positive Rate: 2.3%
- Inference Time: 45ms

Conclusion: The model successfully detects unseen ransomware families.
""",
    }
    
    # Create text documents
    print("  Creating text documents...")
    for filename, content in documents.items():
        filepath = os.path.join(TEST_FILES_DIR, filename)
        create_sample_text_file(filepath, content)
    
    # Create some binary files (simulating images, etc.)
    print("\n  Creating binary files...")
    binary_files = [
        ("Family_Photo.jpg", 2048),
        ("Vacation.png", 1536),
        ("Screenshot.bmp", 1024),
        ("Presentation.pptx", 3072),
        ("Spreadsheet.xlsx", 2560),
    ]
    
    for filename, size in binary_files:
        filepath = os.path.join(TEST_FILES_DIR, filename)
        create_sample_binary_file(filepath, size)
    
    # Create a subdirectory with more files
    subdir = os.path.join(TEST_FILES_DIR, "Documents")
    os.makedirs(subdir, exist_ok=True)
    
    print("\n  Creating files in Documents subdirectory...")
    sub_files = [
        ("Report.docx", 1800),
        ("Analysis.pdf", 2200),
        ("Data.csv", 512),
    ]
    
    for filename, size in sub_files:
        filepath = os.path.join(subdir, filename)
        create_sample_binary_file(filepath, size)
    
    # Summary
    total_files = len(documents) + len(binary_files) + len(sub_files)
    
    print("\n" + "=" * 60)
    print("  TEST FILES SETUP COMPLETE")
    print("=" * 60)
    print(f"\n  Total files created: {total_files}")
    print(f"  Location: {TEST_FILES_DIR}")
    print("\n  Files are ready for ransomware simulation demo.")
    print("=" * 60 + "\n")
    
    return True


def cleanup_test_files():
    """Remove test files and reset the directory."""
    import shutil
    
    print("\n[CLEANUP] Removing test files...")
    
    if os.path.exists(TEST_FILES_DIR):
        # Remove all files
        for item in os.listdir(TEST_FILES_DIR):
            item_path = os.path.join(TEST_FILES_DIR, item)
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception as e:
                print(f"  [ERROR] Failed to remove {item}: {e}")
        
        print("[CLEANUP] Test files removed.")
    else:
        print("[CLEANUP] Test directory doesn't exist.")


def list_test_files():
    """List all test files."""
    print("\n  Current test files:")
    print("  " + "-" * 40)
    
    if not os.path.exists(TEST_FILES_DIR):
        print("  (No test files directory)")
        return
    
    for root, dirs, files in os.walk(TEST_FILES_DIR):
        level = root.replace(TEST_FILES_DIR, '').count(os.sep)
        indent = '  ' * (level + 1)
        
        for f in files:
            filepath = os.path.join(root, f)
            size = os.path.getsize(filepath)
            print(f"{indent}{f} ({size:,} bytes)")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup test files for demo")
    parser.add_argument("--cleanup", action="store_true", help="Remove test files")
    parser.add_argument("--list", action="store_true", help="List test files")
    
    args = parser.parse_args()
    
    if args.cleanup:
        cleanup_test_files()
    elif args.list:
        list_test_files()
    else:
        setup_test_files()
