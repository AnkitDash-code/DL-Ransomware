"""
Educational File Association Infection Simulator
Demonstrates how ransomware can spread through file associations
WARNING: This is for EDUCATIONAL PURPOSES ONLY in a controlled environment!
"""
import os
import sys
import platform
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class EducationalSpreader:
    """
    Educational simulator demonstrating file association infection concepts.
    This simulates how ransomware spreads without creating actual malware.
    """
    
    def __init__(self):
        self.platform = platform.system().lower()
        self.infected_files = []
        self.simulation_log = []
    
    def demonstrate_file_association_attack(self):
        """Simulate changing file associations (educational demo)."""
        print(f"\n[PLATFORM] Running on: {platform.system()} {platform.release()}")
        print("[SIMULATION] Demonstrating file association infection...")
        
        # Platform-specific demonstrations
        if self.platform == "windows":
            self._simulate_windows_association()
        elif self.platform == "linux":
            self._simulate_linux_association()
        elif self.platform == "darwin":  # macOS
            self._simulate_macos_association()
        else:
            print(f"[INFO] Platform {self.platform} simulation not implemented")
    
    def _simulate_windows_association(self):
        """Simulate Windows file association changes."""
        print("\n[WINDOWS SIMULATION]")
        print("  Demonstrating registry-based file association infection:")
        
        associations = {
            ".txt": "notepad.exe",
            ".doc": "winword.exe", 
            ".pdf": "acrobat.exe",
            ".jpg": "photoshop.exe"
        }
        
        for ext, handler in associations.items():
            print(f"    Would modify: HKEY_CLASSES_ROOT\\{ext}\\shell\\open\\command")
            print(f"    From: {handler} \"%1\"")
            print(f"    To:   malicious_handler.exe \"%1\"")
            self.simulation_log.append(f"Simulated infection of {ext} association")
    
    def _simulate_linux_association(self):
        """Simulate Linux file association changes."""
        print("\n[LINUX SIMULATION]")
        print("  Demonstrating MIME-type association infection:")
        
        mime_types = {
            "text/plain": "gedit",
            "application/pdf": "evince",
            "image/jpeg": "eog"
        }
        
        for mime, handler in mime_types.items():
            print(f"    Would modify: ~/.local/share/applications/mimeapps.list")
            print(f"    From: {mime}={handler}.desktop")
            print(f"    To:   {mime}=malicious.desktop")
            self.simulation_log.append(f"Simulated infection of {mime} association")
    
    def _simulate_macos_association(self):
        """Simulate macOS file association changes."""
        print("\n[MACOS SIMULATION]")
        print("  Demonstrating UTI (Uniform Type Identifier) infection:")
        
        utis = {
            "public.plain-text": "TextEdit",
            "com.adobe.pdf": "Preview",
            "public.jpeg": "Preview"
        }
        
        for uti, handler in utis.items():
            print(f"    Would modify: ~/Library/Preferences/com.apple.LaunchServices.plist")
            print(f"    From: {uti} -> {handler}")
            print(f"    To:   {uti} -> MaliciousApp")
            self.simulation_log.append(f"Simulated infection of {uti} association")
    
    def demonstrate_polymorphic_spreading(self):
        """Simulate polymorphic code spreading."""
        print("\n[POLYMORPHIC SPREADING SIMULATION]")
        print("  Demonstrating how ransomware mutates to avoid detection:")
        
        mutation_techniques = [
            "Code obfuscation through variable renaming",
            "Control flow flattening",
            "String encryption with different keys",
            "Adding junk code to change file hashes",
            "Using different packing/compression methods"
        ]
        
        for i, technique in enumerate(mutation_techniques, 1):
            print(f"    {i}. {technique}")
            self.simulation_log.append(f"Simulated polymorphic technique: {technique}")
    
    def demonstrate_cross_platform_infection(self):
        """Simulate cross-platform infection vectors."""
        print("\n[CROSS-PLATFORM INFECTION SIMULATION]")
        print("  Demonstrating multi-platform infection vectors:")
        
        vectors = {
            "Document Macros": ["Word .docm", "Excel .xlsm", "PowerPoint .pptm"],
            "Script Files": ["Python .py", "JavaScript .js", "Batch .bat/.sh"],
            "Portable Documents": ["PDF with embedded JavaScript"],
            "Archive Files": ["ZIP/TAR with autorun scripts"],
            "Configuration Files": [".ini", ".cfg", ".xml with executable content"]
        }
        
        for vector, file_types in vectors.items():
            print(f"\n  {vector}:")
            for file_type in file_types:
                print(f"    - {file_type}")
                self.simulation_log.append(f"Simulated infection vector: {vector} -> {file_type}")
    
    def run_complete_simulation(self):
        """Run the complete educational simulation."""
        print("=" * 70)
        print("  EDUCATIONAL RANSOMWARE SPREADING SIMULATOR")
        print("  WARNING: This demonstrates infection concepts only!")
        print("=" * 70)
        
        self.demonstrate_file_association_attack()
        self.demonstrate_polymorphic_spreading()
        self.demonstrate_cross_platform_infection()
        
        print("\n" + "=" * 70)
        print("  SIMULATION COMPLETE")
        print("=" * 70)
        print(f"\n  Total simulated infections: {len(self.simulation_log)}")
        print("  No actual system modifications were made.")
        print("  This is purely educational/demonstration code.")
        print("=" * 70)
        
        return self.simulation_log

def main():
    """Run the educational spreading simulator."""
    spreader = EducationalSpreader()
    spreader.run_complete_simulation()

if __name__ == "__main__":
    main()
