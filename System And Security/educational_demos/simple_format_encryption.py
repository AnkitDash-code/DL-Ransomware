#!/usr/bin/env python3
"""
SIMPLE FILE ENCRYPTION FOR EDUCATIONAL PURPOSES
Encrypts common file formats (text, documents, images) without Python files
"""

import os
import sys
from pathlib import Path
from cryptography.fernet import Fernet

def create_simple_encryption_demo():
    """Create encryption demo for simple file formats only"""
    
    print("=" * 60)
    print("SIMPLE FILE FORMAT ENCRYPTION DEMO")
    print("=" * 60)
    print("Encrypting common file types: TXT, DOC, JPG, PNG, CSV, etc.")
    print("Avoiding Python files to minimize security software interference")
    print("=" * 60)
    
    # Create demo directory
    demo_dir = Path("simple_format_encryption")
    demo_dir.mkdir(exist_ok=True)
    
    # Create sample files in common formats (NO Python files)
    sample_files = {
        "important_notes.txt": """PROJECT: CYBERSECURITY RESEARCH
==============================

RESEARCH OBJECTIVES:
1. Analyze malware behavior patterns
2. Study encryption techniques used by ransomware
3. Develop detection algorithms
4. Create educational simulations
5. Document findings for academic publication

CURRENT STATUS:
- Literature review completed
- Initial dataset collection in progress
- Methodology design underway
- Preliminary results promising

NEXT STEPS:
- Expand sample dataset
- Implement machine learning models
- Conduct comprehensive testing
- Prepare conference presentation
""",
        "budget_spreadsheet.csv": """Category,Amount,Department,Quarter,Status
Software Licenses,5000,IT,Q1,Approved
Hardware Equipment,15000,IT,Q1,Pending
Training Programs,8000,HR,Q1,Approved
Cloud Services,12000,IT,Q1,Active
Security Tools,10000,IT,Q1,Requested
Conference Travel,3000,Research,Q1,Approved
""",
        "team_members.xlsx": """Name,Role,Experience,Years,Specialty
Alice Johnson,Lead Researcher,Senior,8,Malware Analysis
Bob Smith,Data Scientist,Intermediate,5,Machine Learning
Carol Davis,Security Analyst,Senior,10,Threat Intelligence
David Wilson,Developer,Junior,2,Tool Development
Eva Brown,Researcher,Intermediate,4,Behavioral Analysis
""",
        "research_findings.doc": """CYBERSECURITY RESEARCH FINDINGS
===============================

EXECUTIVE SUMMARY:
Our research has identified several key patterns in modern ransomware behavior that distinguish them from traditional malware. The analysis focused on behavioral characteristics rather than signatures, enabling detection of previously unknown variants.

KEY DISCOVERIES:
1. File access patterns show distinct clustering
2. Process creation sequences exhibit predictable structures
3. Network communication follows specific timing patterns
4. Registry modifications occur in consistent sequences

METHODOLOGY:
- Collected 10,000+ malware samples
- Extracted behavioral features using custom tools
- Applied machine learning classification algorithms
- Validated results against known malware databases

IMPLICATIONS:
These findings suggest that behavioral analysis can provide early warning systems for zero-day ransomware variants before signature-based detection becomes available.

RECOMMENDATIONS:
1. Implement real-time behavioral monitoring
2. Develop adaptive detection algorithms
3. Create comprehensive threat intelligence feeds
4. Establish rapid response protocols
""",
        "presentation_slides.ppt": """CYBERSECURITY RESEARCH PRESENTATION
==================================

SLIDE 1: TITLE
Modern Ransomware Detection Through Behavioral Analysis

SLIDE 2: INTRODUCTION
Overview of current threat landscape and research objectives

SLIDE 3: METHODOLOGY
Data collection, feature extraction, and analysis techniques

SLIDE 4: KEY FINDINGS
Primary discoveries and their significance

SLIDE 5: TECHNICAL DETAILS
Algorithm performance and validation results

SLIDE 6: IMPLICATIONS
Impact on cybersecurity practices and future research

SLIDE 7: CONCLUSIONS
Summary of contributions and next steps

SLIDE 8: QUESTIONS
Discussion and audience engagement
""",
        "family_photo.jpg": b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.' ",
        "logo_design.png": b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xff\xa1\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x07tIME\x07\xdb\x0c\x11\x0c\x05\x1f\x85\x1f/"
    }
    
    # Create original files
    print("[1] CREATING SAMPLE FILES IN COMMON FORMATS")
    print("-" * 50)
    created_files = []
    for filename, content in sample_files.items():
        file_path = demo_dir / filename
        if isinstance(content, str):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            with open(file_path, 'wb') as f:
                f.write(content)
        created_files.append(file_path)
        print(f"✅ Created: {filename}")
    
    # Show sample content
    print("\n[2] SAMPLE ORIGINAL CONTENT:")
    print("-" * 50)
    with open(demo_dir / "important_notes.txt", 'r') as f:
        content = f.read()
        print("important_notes.txt (first 150 chars):")
        print(content[:150] + "...")
    
    # Generate encryption key
    print("\n[3] GENERATING ENCRYPTION KEY")
    print("-" * 50)
    key = Fernet.generate_key()
    key_file = demo_dir / "recovery_key.key"
    with open(key_file, 'wb') as f:
        f.write(key)
    print(f"✅ Encryption key generated and saved: {key_file.name}")
    print(f"Key (first 20 chars): {key.decode()[:20]}...")
    
    # Encrypt files with proper cryptographic encryption
    print("\n[4] APPLYING CRYPTOGRAPHIC ENCRYPTION")
    print("-" * 50)
    cipher = Fernet(key)
    encrypted_count = 0
    
    for file_path in created_files:
        try:
            # Read original file
            with open(file_path, 'rb') as f:
                original_data = f.read()
            
            # Encrypt the data
            encrypted_data = cipher.encrypt(original_data)
            
            # Write encrypted data back to file
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)
            
            # Rename with encrypted extension
            encrypted_name = f"{file_path.name}.locked"
            encrypted_path = file_path.parent / encrypted_name
            file_path.rename(encrypted_path)
            
            encrypted_count += 1
            print(f"✅ Encrypted: {file_path.name} → {encrypted_name}")
            
        except Exception as e:
            print(f"❌ Failed to encrypt {file_path.name}: {e}")
    
    # Create educational ransom note
    create_educational_note(demo_dir, encrypted_count)
    
    # Verification
    print("\n" + "=" * 60)
    print("ENCRYPTION DEMONSTRATION COMPLETE")
    print("=" * 60)
    print(f"✅ Files created: {len(created_files)}")
    print(f"✅ Files encrypted: {encrypted_count}")
    print(f"✅ Encryption key saved: recovery_key.key")
    print(f"✅ Files renamed with .locked extension")
    print("=" * 60)
    
    # Test readability of encrypted files
    print("\n[5] VERIFYING ENCRYPTION EFFECTIVENESS")
    print("-" * 50)
    encrypted_file = demo_dir / "important_notes.txt.locked"
    try:
        with open(encrypted_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print("❌ File still readable as text!")
        print("Content preview:", content[:100])
    except UnicodeDecodeError:
        print("✅ SUCCESS: File properly encrypted!")
        print("   Shows UnicodeDecodeError - cannot read as text")
    except Exception as e:
        print(f"Error testing file readability: {e}")
    
    print("\n" + "=" * 60)
    print("EDUCATIONAL TAKEAWAYS:")
    print("=" * 60)
    print("✅ Common file formats (documents, images, data) encrypted")
    print("✅ No Python files included (minimizes security interference)")
    print("✅ Files are truly unreadable without decryption key")
    print("✅ Demonstrates real ransomware behavior safely")
    print("✅ Shows why backups and security are essential")
    print("=" * 60)

def create_educational_note(directory, file_count):
    """Create educational ransom note"""
    note_content = f"""===============================================
    EDUCATIONAL FILE ENCRYPTION SIMULATION
===============================================

⚠️  YOUR FILES HAVE BEEN ENCRYPTED ⚠️

This is an educational demonstration of how ransomware works.
In a real attack, your files would be permanently inaccessible.

📁 Files affected: {file_count}
📍 Location: {directory}
🔑 Recovery key available: recovery_key.key

ENCRYPTED FILE TYPES:
- Text documents (.txt.locked)
- Spreadsheets (.csv.locked, .xlsx.locked)  
- Word documents (.doc.locked)
- Presentation files (.ppt.locked)
- Images (.jpg.locked, .png.locked)

HOW THIS WORKS EDUCATIONALLY:
1. Files were encrypted using Fernet symmetric encryption
2. Original files are completely unrecoverable without the key
3. This demonstrates why backups are critical for security
4. The recovery key is saved separately for educational purposes

RECOVERY PROCESS:
1. Locate the recovery_key.key file
2. Use the decryption tool to restore your files
3. This shows why having backups is essential

===============================================
        EDUCATIONAL SECURITY RESEARCH
===============================================

This simulation demonstrates:
✅ How ransomware makes files truly inaccessible
✅ Why encryption keys are critical for recovery  
✅ The importance of regular backups
✅ How security researchers analyze encrypted files

No actual harm was done - this is purely educational!
"""

    note_path = directory / "HOW_TO_RECOVER_FILES.txt"
    with open(note_path, 'w') as f:
        f.write(note_content)
    print(f"✅ Created educational instruction file: {note_path.name}")

if __name__ == "__main__":
    try:
        create_simple_encryption_demo()
    except Exception as e:
        print(f"[ERROR] Encryption demo failed: {e}")
        import traceback
        traceback.print_exc()