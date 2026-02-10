"""
Educational Payload Dropper Simulator
Demonstrates how ransomware drops payloads to different system locations
WARNING: This is for EDUCATIONAL PURPOSES ONLY - creates harmless marker files!
"""
import os
import sys
import platform
from pathlib import Path
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class SafePayloadDropper:
    """
    Educational simulator demonstrating payload dropping concepts.
    Creates harmless marker files to show where real malware would drop payloads.
    """
    
    def __init__(self):
        self.platform = platform.system().lower()
        self.dropped_payloads = []
        self.marker_extension = ".edu_drop"  # Educational marker extension
    
    def get_platform_payload_locations(self):
        """Get platform-specific payload drop locations."""
        locations = {
            "windows": [
                "~/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/",
                "C:/Windows/Temp/",
                "~/AppData/Local/Temp/",
                "~/Documents/",
                "~/Desktop/"
            ],
            "linux": [
                "~/.config/autostart/",
                "/tmp/",
                "~/Documents/",
                "~/Desktop/",
                "~/.local/share/applications/"
            ],
            "darwin": [  # macOS
                "~/Library/LaunchAgents/",
                "~/Library/Application Support/",
                "/tmp/",
                "~/Documents/",
                "~/Desktop/"
            ]
        }
        
        return locations.get(self.platform, [])
    
    def drop_educational_payloads(self):
        """Drop harmless educational marker files."""
        print(f"\n[PLATFORM] {platform.system()} {platform.release()}")
        print("[PAYLOAD DROP SIMULATION] Creating educational markers...")
        
        locations = self.get_platform_payload_locations()
        
        for location in locations:
            expanded_location = os.path.expanduser(location)
            Path(expanded_location).mkdir(parents=True, exist_ok=True)
            
            # Create marker file
            marker_filename = f"payload_marker_{int(time.time())}{self.marker_extension}"
            marker_path = os.path.join(expanded_location, marker_filename)
            
            try:
                with open(marker_path, 'w') as f:
                    f.write(f"""EDUCATIONAL PAYLOAD MARKER
=============================
This file simulates where ransomware would drop payloads.
Location: {location}
Timestamp: {time.ctime()}
Platform: {platform.system()}

This is NOT actual malware - just an educational demonstration.
""")
                
                print(f"  [DROPPED] {marker_path}")
                self.dropped_payloads.append({
                    "location": location,
                    "path": marker_path,
                    "timestamp": time.time()
                })
                
            except Exception as e:
                print(f"  [ERROR] Could not create marker in {location}: {e}")
    
    def demonstrate_persistence_methods(self):
        """Simulate persistence mechanism demonstrations."""
        print("\n[PERSISTENCE METHODS SIMULATION]")
        
        persistence_methods = {
            "Windows": [
                "Registry Run Keys (HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run)",
                "Startup Folder (%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup)",
                "Scheduled Tasks",
                "Service Installation",
                "WMI Event Subscription"
            ],
            "Linux": [
                "Systemd User Services (~/.config/systemd/user/)",
                "Cron Jobs (crontab -e)",
                "Autostart Desktop Entries (~/.config/autostart/)",
                "Shell Profile Modifications (~/.bashrc, ~/.zshrc)",
                "Init Scripts (/etc/init.d/)"
            ],
            "macOS": [
                "Launch Agents (~/Library/LaunchAgents/)",
                "Launch Daemons (/Library/LaunchDaemons/)",
                "Login Items (System Preferences)",
                "Cron Jobs",
                "Shell Profile Modifications"
            ]
        }
        
        platform_methods = persistence_methods.get(platform.system(), [])
        
        print(f"  Demonstrating persistence methods for {platform.system()}:")
        for i, method in enumerate(platform_methods, 1):
            print(f"    {i}. {method}")
    
    def demonstrate_privilege_escalation(self):
        """Simulate privilege escalation techniques."""
        print("\n[PRIVILEGE ESCALATION SIMULATION]")
        print("  Demonstrating common escalation vectors:")
        
        escalation_vectors = [
            "DLL Sideloading/Hijacking",
            "Service Binary Replacement", 
            "Scheduled Task Modification",
            "Registry Permissions Weakness",
            "Unquoted Service Paths",
            "AlwaysInstallElevated MSI",
            "Group Policy Modification",
            "Token Impersonation"
        ]
        
        for vector in escalation_vectors:
            print(f"    - {vector}")
    
    def cleanup_markers(self):
        """Remove all educational marker files."""
        print("\n[CLEANUP] Removing educational markers...")
        removed = 0
        
        for payload in self.dropped_payloads:
            try:
                if os.path.exists(payload["path"]):
                    os.remove(payload["path"])
                    print(f"  [REMOVED] {payload['path']}")
                    removed += 1
            except Exception as e:
                print(f"  [ERROR] Failed to remove {payload['path']}: {e}")
        
        print(f"[CLEANUP] Removed {removed} marker files")
        return removed
    
    def run_complete_demo(self):
        """Run the complete educational payload dropping demonstration."""
        print("=" * 70)
        print("  EDUCATIONAL PAYLOAD DROPPER SIMULATOR")
        print("  Creates harmless marker files to demonstrate infection vectors")
        print("=" * 70)
        
        # Drop payloads
        self.drop_educational_payloads()
        
        # Show persistence methods
        self.demonstrate_persistence_methods()
        
        # Show escalation techniques
        self.demonstrate_privilege_escalation()
        
        print("\n" + "=" * 70)
        print("  DEMONSTRATION COMPLETE")
        print("=" * 70)
        print(f"\n  Payloads dropped: {len(self.dropped_payloads)}")
        print("  All files are harmless educational markers.")
        print("  Use 'cleanup_markers()' to remove them.")
        print("=" * 70)
        
        return self.dropped_payloads

def main():
    """Run the payload dropper simulator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Educational Payload Dropper Simulator")
    parser.add_argument("--cleanup", action="store_true", 
                       help="Remove all educational marker files")
    
    args = parser.parse_args()
    
    dropper = SafePayloadDropper()
    
    if args.cleanup:
        dropper.cleanup_markers()
    else:
        dropper.run_complete_demo()

if __name__ == "__main__":
    main()
