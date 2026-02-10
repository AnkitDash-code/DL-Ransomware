"""
Educational Ransomware Injector Simulator
Demonstrates injection techniques used by ransomware in a safe, controlled manner
WARNING: This is for EDUCATIONAL PURPOSES ONLY with emulators!
"""
import os
import sys
import platform
import time
import struct
from pathlib import Path
import hashlib

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class EducationalInjector:
    """
    Educational simulator demonstrating ransomware injection techniques.
    Works with emulators for safe demonstration of infection concepts.
    """
    
    def __init__(self, target_emulator=None):
        self.target_emulator = target_emulator or "qemu"  # Default emulator
        self.injection_log = []
        self.injected_files = []
        self.emulator_commands = {
            "qemu": self._qemu_injection,
            "docker": self._docker_injection,
            "vmware": self._vmware_injection,
            "virtualbox": self._virtualbox_injection
        }
    
    def demonstrate_code_injection(self):
        """Simulate code injection techniques."""
        print("\n[CODE INJECTION SIMULATION]")
        print("  Demonstrating common injection methods:")
        
        injection_methods = [
            {
                "name": "Process Hollowing",
                "description": "Injecting code into suspended legitimate process",
                "targets": ["explorer.exe", "svchost.exe", "dllhost.exe"],
                "simulation": "Creating suspended process and replacing memory"
            },
            {
                "name": "DLL Injection", 
                "description": "Loading malicious DLL into target process",
                "targets": ["user32.dll", "kernel32.dll", "ntdll.dll"],
                "simulation": "Using SetWindowsHookEx/CreateRemoteThread"
            },
            {
                "name": "Reflective DLL Injection",
                "description": "Loading DLL without touching disk",
                "targets": ["Memory-only injection"],
                "simulation": "Direct memory allocation and execution"
            },
            {
                "name": "APC Injection",
                "description": "Asynchronous Procedure Call injection",
                "targets": ["Thread queue manipulation"],
                "simulation": "QueueUserAPC to hijack thread execution"
            }
        ]
        
        for method in injection_methods:
            print(f"\n  Method: {method['name']}")
            print(f"    Description: {method['description']}")
            print(f"    Targets: {', '.join(method['targets'])}")
            print(f"    Simulation: {method['simulation']}")
            self.injection_log.append(f"Simulated {method['name']} injection")
    
    def demonstrate_file_injection(self):
        """Simulate file-based injection techniques."""
        print("\n[FILE INJECTION SIMULATION]")
        print("  Demonstrating file infection methods:")
        
        file_types = {
            "PE Files (.exe/.dll)": {
                "methods": ["Section appending", "Entry point redirection", "Import table modification"],
                "simulation": "Modifying PE headers and sections"
            },
            "Office Documents": {
                "methods": ["Macro injection", "OLE object embedding", "VBA stomping"],
                "simulation": "Embedding malicious macros/VBA code"
            },
            "PDF Files": {
                "methods": ["JavaScript embedding", "Launch action injection", "Embedded file objects"],
                "simulation": "Adding malicious JavaScript/actions"
            },
            "Script Files": {
                "methods": ["Code prepending", "Function hooking", "Auto-execution triggers"],
                "simulation": "Inserting malicious code at beginning"
            }
        }
        
        for file_type, details in file_types.items():
            print(f"\n  {file_type}:")
            for method in details["methods"]:
                print(f"    - {method}")
            print(f"    Simulation: {details['simulation']}")
            self.injection_log.append(f"Simulated {file_type} injection")
    
    def demonstrate_memory_injection(self):
        """Simulate memory-based injection techniques."""
        print("\n[MEMORY INJECTION SIMULATION]")
        print("  Demonstrating in-memory execution:")
        
        memory_techniques = [
            {
                "name": "Process Injection",
                "technique": "WriteProcessMemory + CreateRemoteThread",
                "address_space": "Target process virtual memory",
                "simulation": "Allocating RWX memory in remote process"
            },
            {
                "name": "Thread Hijacking", 
                "technique": "SuspendThread + SetThreadContext",
                "address_space": "Existing thread registers",
                "simulation": "Redirecting execution flow to injected code"
            },
            {
                "name": "Heap Spraying",
                "technique": "Massive heap allocations",
                "address_space": "Process heap space",
                "simulation": "Filling heap with shellcode for reliable execution"
            }
        ]
        
        for tech in memory_techniques:
            print(f"\n  {tech['name']}:")
            print(f"    Technique: {tech['technique']}")
            print(f"    Address Space: {tech['address_space']}")
            print(f"    Simulation: {tech['simulation']}")
            self.injection_log.append(f"Simulated {tech['name']}")
    
    def _qemu_injection(self):
        """Simulate injection in QEMU emulator environment."""
        print("\n[QEMU EMULATOR INJECTION]")
        print("  Simulating injection in virtualized environment:")
        print("    - Modifying guest memory regions")
        print("    - Injecting code into VM processes")
        print("    - Manipulating virtual CPU registers")
        print("    - Hooking system calls in guest OS")
        
        self.injection_log.append("Simulated QEMU-based injection")
        return True
    
    def _docker_injection(self):
        """Simulate injection in Docker container environment."""
        print("\n[DOCKER CONTAINER INJECTION]")
        print("  Simulating injection in containerized environment:")
        print("    - Modifying container filesystem")
        print("    - Injecting into container processes")
        print("    - Manipulating container namespaces")
        print("    - Escaping container boundaries")
        
        self.injection_log.append("Simulated Docker-based injection")
        return True
    
    def _vmware_injection(self):
        """Simulate injection in VMware environment."""
        print("\n[VMWARE INJECTION]")
        print("  Simulating injection in VMware environment:")
        print("    - Using VMware backdoor interface")
        print("    - Modifying VM memory through hypervisor")
        print("    - Injecting into guest processes")
        print("    - Leveraging VMware tools interface")
        
        self.injection_log.append("Simulated VMware-based injection")
        return True
    
    def _virtualbox_injection(self):
        "Simulate injection in VirtualBox environment."""
        print("\n[VIRTUALBOX INJECTION]")
        print("  Simulating injection in VirtualBox environment:")
        print("    - Using VBoxManage for memory access")
        print("    - Modifying guest additions")
        print("    - Injecting through shared folders")
        print("    - Manipulating VRDP connections")
        
        self.injection_log.append("Simulated VirtualBox-based injection")
        return True
    
    def demonstrate_emulator_integration(self):
        """Demonstrate integration with different emulators."""
        print(f"\n[EMULATOR INTEGRATION: {self.target_emulator.upper()}]")
        
        if self.target_emulator in self.emulator_commands:
            success = self.emulator_commands[self.target_emulator]()
            if success:
                print(f"  [SUCCESS] Injection simulation completed for {self.target_emulator}")
            else:
                print(f"  [FAILED] Injection simulation failed for {self.target_emulator}")
        else:
            print(f"  [INFO] Emulator {self.target_emulator} not supported")
            print("  [INFO] Available emulators: qemu, docker, vmware, virtualbox")
    
    def create_injection_artifacts(self, output_dir="injection_demo"):
        """Create educational artifacts demonstrating injection concepts."""
        print(f"\n[ARTIFACT CREATION] Creating injection demonstration files...")
        
        demo_dir = Path(output_dir)
        demo_dir.mkdir(exist_ok=True)
        
        artifacts = {
            "pe_header_modification.txt": """PE Header Injection Demo
================================
This file demonstrates PE header modification techniques:

1. Entry Point Redirection
2. Section Addition
3. Import Table Manipulation
4. TLS Callback Injection

Sample offsets:
- Entry Point: 0x001A (IMAGE_NT_HEADERS.OptionalHeader.AddressOfEntryPoint)
- Sections: 0x0100+ (IMAGE_SECTION_HEADER array)
- Imports: 0x0080+ (IMAGE_DATA_DIRECTORY[1])
""",
            
            "macro_injection_demo.doc": """Document Macro Injection Demo
==============================
This simulates Office document macro injection:

Sub AutoOpen()
    ' Simulated malicious macro execution
    MsgBox "Educational macro injection demonstration"
    ' Real malware would execute payload here
End Sub

Sub Document_Open()
    ' Alternative auto-execution method
    AutoOpen
End Sub
""",
            
            "javascript_injection.pdf": """PDF JavaScript Injection Demo
==============================
This simulates PDF JavaScript injection:

<<
/Names <<
/JavaScript <<
/Names [(AutoExec) << /S/JavaScript/JS(this.print\({bUI:true,bSilent:false}\)) >>]
>>
>>
>>
""",
            
            "memory_pattern.bin": struct.pack("<IIII", 0x90909090, 0x90909090, 0x90909090, 0x90909090),
            
            "injection_report.txt": f"""Injection Simulation Report
==========================
Timestamp: {time.ctime()}
Emulator: {self.target_emulator}
Platform: {platform.system()} {platform.release()}

Simulated Techniques:
{'\\n'.join([f'- {log}' for log in self.injection_log])}

Total Simulations: {len(self.injection_log)}
Status: Educational demonstration only - no actual malware created.
"""
        }
        
        for filename, content in artifacts.items():
            filepath = demo_dir / filename
            try:
                if isinstance(content, bytes):
                    filepath.write_bytes(content)
                else:
                    filepath.write_text(content, encoding='utf-8')
                print(f"  [CREATED] {filepath}")
                self.injected_files.append(str(filepath))
            except Exception as e:
                print(f"  [ERROR] Failed to create {filepath}: {e}")
        
        print(f"\n[ARTIFACTS] Created {len(self.injected_files)} educational files in {demo_dir}")
        return self.injected_files
    
    def run_complete_injection_demo(self):
        """Run the complete educational injection demonstration."""
        print("=" * 70)
        print("  EDUCATIONAL RANSOMWARE INJECTOR SIMULATOR")
        print(f"  Target Emulator: {self.target_emulator.upper()}")
        print("  WARNING: This demonstrates injection concepts only!")
        print("=" * 70)
        
        # Demonstrate injection techniques
        self.demonstrate_code_injection()
        self.demonstrate_file_injection()
        self.demonstrate_memory_injection()
        
        # Demonstrate emulator integration
        self.demonstrate_emulator_integration()
        
        # Create educational artifacts
        artifacts = self.create_injection_artifacts()
        
        print("\n" + "=" * 70)
        print("  INJECTION SIMULATION COMPLETE")
        print("=" * 70)
        print(f"\n  Techniques demonstrated: {len(self.injection_log)}")
        print(f"  Educational artifacts created: {len(artifacts)}")
        print("  All files are harmless educational demonstrations.")
        print("=" * 70)
        
        return {
            "techniques": self.injection_log,
            "artifacts": artifacts,
            "emulator": self.target_emulator
        }

def main():
    """Run the educational injector simulator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Educational Ransomware Injector Simulator")
    parser.add_argument("--emulator", type=str, default="qemu",
                       choices=["qemu", "docker", "vmware", "virtualbox"],
                       help="Target emulator for injection simulation")
    parser.add_argument("--output-dir", type=str, default="injection_demo",
                       help="Directory for educational artifacts")
    
    args = parser.parse_args()
    
    injector = EducationalInjector(target_emulator=args.emulator)
    results = injector.run_complete_injection_demo()
    
    # Optionally show artifact contents
    if results["artifacts"]:
        print(f"\n[FILES CREATED] Educational artifacts in '{args.output_dir}':")
        for artifact in results["artifacts"]:
            print(f"  - {os.path.basename(artifact)}")

if __name__ == "__main__":
    main()
