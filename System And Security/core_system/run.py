"""
Zero-Day Ransomware Detection System - Main Runner
Provides convenient commands to run different parts of the system
"""
import os
import sys
import argparse
import subprocess

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)


def print_banner():
    """Print the project banner."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║     ZERO-DAY RANSOMWARE DETECTION SYSTEM                     ║
║     Deep Learning Behavioral Analysis                         ║
╚══════════════════════════════════════════════════════════════╝
    """)


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n[RUNNING] {description}...")
    print(f"[CMD] {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, cwd=PROJECT_ROOT)
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def setup():
    """Setup the project (install deps, create test files)."""
    print("\n=== PROJECT SETUP ===\n")
    
    # Install dependencies
    print("[1/3] Installing dependencies...")
    run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                "Installing Python packages")
    
    # Create test files
    print("\n[2/3] Creating test files...")
    run_command([sys.executable, "data/setup_test_files.py"],
                "Setting up test files")
    
    # Download dataset (optional)
    print("\n[3/3] Dataset setup...")
    print("      To download the RISS dataset, run:")
    print("      python data/download_data.py")
    
    print("\n=== SETUP COMPLETE ===")
    print("\nNext steps:")
    print("  1. Run: python run.py download   (download RISS dataset)")
    print("  2. Run: python run.py train      (train the model)")
    print("  3. Run: python run.py dashboard  (start the dashboard)")


def download_dataset():
    """Download the RISS dataset."""
    run_command([sys.executable, "data/download_data.py"],
                "Downloading RISS dataset")


def preprocess():
    """Run data preprocessing."""
    run_command([sys.executable, "model/preprocess.py"],
                "Preprocessing data")


def train():
    """Train the 1D-CNN model."""
    run_command([sys.executable, "model/train_cnn.py"],
                "Training ransomware detection model")


def dashboard():
    """Start the Streamlit dashboard."""
    print("\n[INFO] Starting Streamlit dashboard...")
    print("[INFO] Open http://localhost:8501 in your browser")
    print("[INFO] Press Ctrl+C to stop\n")
    
    run_command([sys.executable, "-m", "streamlit", "run", 
                 "../security_tools/antivirus/dashboard.py", "--server.headless", "true"],
                "Streamlit Dashboard")


def guardian():
    """Start the guardian daemon (CLI mode)."""
    run_command([sys.executable, "../security_tools/antivirus/guardian_daemon.py"],
                "Guardian Daemon")


def ransomware(variant='A', restore=False):
    """Run ransomware simulation."""
    cmd = [sys.executable, "simulators/ransomware_sim.py", 
           "--variant", variant, "--no-popup"]
    if restore:
        cmd.append("--restore")
    
    run_command(cmd, f"Ransomware Simulation (Variant {variant})")


def benign(simulator='backup'):
    """Run benign simulation."""
    sim_map = {
        'backup': 'simulators/backup_sim.py',
        'compress': 'simulators/compress_sim.py',
        'rename': 'simulators/rename_sim.py'
    }
    
    if simulator not in sim_map:
        print(f"[ERROR] Unknown simulator: {simulator}")
        print(f"[INFO] Available: {', '.join(sim_map.keys())}")
        return
    
    run_command([sys.executable, sim_map[simulator]],
                f"Benign Simulation ({simulator})")


def spreading():
    """Run spreading simulation."""
    run_command([sys.executable, "simulators/spreading_sim.py"],
                "Educational Spreading Simulation")


def payload_drop():
    """Run payload dropper simulation."""
    run_command([sys.executable, "simulators/payload_dropper.py"],
                "Educational Payload Dropping")


def interactive_injector():
    """Run interactive file selector ransomware injector."""
    # Use correct path to educational_demos
    cmd = [sys.executable, "../educational_demos/simulators/interactive_injector.py"]
    run_command(cmd, "Interactive File Selector Injector")


def targeted_injector(target_dir="data/test_files"):
    """Run targeted ransomware injector on test files."""
    cmd = [sys.executable, "simulators/targeted_injector.py", "--target", target_dir]
    run_command(cmd, f"Targeted Ransomware Injection ({target_dir})")


def load_database():
    """Load threat database for static blocking."""
    run_command([sys.executable, "../security_tools/antivirus/load_database.py", "--enhance"],
                "Loading Threat Database")


def linux_ransomware():
    """Run portable Linux ransomware simulation."""
    run_command([sys.executable, "simulators/linux_ransomware.py"],
                "Portable Linux Ransomware Simulation")


def injector(emulator='qemu'):
    """Run injector simulation."""
    cmd = [sys.executable, "simulators/injector_sim.py", "--emulator", emulator]
    run_command(cmd, f"Educational Injector Simulation ({emulator})")


def comprehensive_simulation():
    """Run comprehensive ransomware management simulation."""
    cmd = [sys.executable, "../educational_demos/comprehensive_ransomware_simulator.py"]
    run_command(cmd, "Comprehensive Ransomware Management Simulation")

def backup_encryptor():
    """Run backup folder encryption dropper."""
    cmd = [sys.executable, "simulators/backup_encryptor.py"]
    run_command(cmd, "Backup Folder Encryption Dropper")

def backup_encryptor_exe():
    """Create standalone EXE for backup encryption."""
    cmd = [sys.executable, "create_exe_dropper.py"]
    run_command(cmd, "Create Standalone EXE Dropper")

def backup_decryptor():
    """Run backup folder decryption tool."""
    cmd = [sys.executable, "simulators/backup_decryptor.py"]
    run_command(cmd, "Backup Folder Decryption Tool")

def advanced_dropper_gui():
    """Run advanced dropper creator GUI."""
    cmd = [sys.executable, "advanced_dropper_creator_gui.py"]
    run_command(cmd, "Advanced Dropper Creator GUI")

def create_backup_exe():
    """Create standalone backup folder encryption EXE."""
    cmd = [sys.executable, "create_backup_exe.py"]
    run_command(cmd, "Create Backup Folder Encryption EXE")


def payload_cleanup():
    """Cleanup payload dropper markers."""
    run_command([sys.executable, "simulators/payload_dropper.py", "--cleanup"],
                "Cleaning up payload markers")


def demo():
    """Run the full demo sequence."""
    print_banner()
    print("\n=== DEMO SEQUENCE ===\n")
    print("This will run through the demo sequence:")
    print("  1. Setup test files")
    print("  2. Start dashboard (in background)")
    print("  3. Run benign backup simulation")
    print("  4. Run ransomware simulation")
    print("\nOpen the dashboard at: http://localhost:8501")
    
    input("\nPress Enter to start the demo...")
    
    # Setup test files
    run_command([sys.executable, "data/setup_test_files.py"],
                "Setting up test files")
    
    print("\n[INFO] Please start the dashboard in a separate terminal:")
    print("       python run.py dashboard")
    print("\nThen run these commands to see the demo:")
    print("  python run.py benign backup    (benign - low threat)")
    print("  python run.py attack           (ransomware - high threat)")


def reset():
    """Reset the test environment."""
    import sys
    sys.path.insert(0, '../security_tools')
    from monitor.monitor import BehaviorMonitor
    
    print("\n=== RESETTING ENVIRONMENT ===\n")
    
    # Clear behavioral log
    monitor = BehaviorMonitor()
    monitor.clear_log()
    print("[OK] Behavioral log cleared")
    
    # Reset test files
    run_command([sys.executable, "data/setup_test_files.py", "--cleanup"],
                "Removing old test files")
    run_command([sys.executable, "data/setup_test_files.py"],
                "Creating fresh test files")
    
    print("\n=== RESET COMPLETE ===")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Zero-Day Ransomware Detection System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=r"""
Commands:
  setup       Setup the project (install deps, create test files)
  download    Download the RISS ransomware dataset
  preprocess  Run data preprocessing
  train       Train the 1D-CNN model
  dashboard   Start the Streamlit dashboard
  guardian    Start the guardian daemon (CLI mode)
  attack      Run ransomware simulation
  benign      Run benign simulation (backup/compress/rename)
  spreading   Run educational spreading simulation (cross-platform concepts)
  payload     Run educational payload dropper simulation
  payload-cleanup  Cleanup payload dropper markers
  database    Load comprehensive threat database
  interactive Run interactive file selector injector (GUI)
  fixed       Run fixed professional dropper creator (GUI)
  enhanced    Run enhanced professional dropper creator (GUI)
  targeted    Run targeted ransomware injection on test files
  linux       Run portable Linux ransomware simulation
  injector    Run educational injector simulation (emulator integration)
  comprehensive Run complete ransomware management simulation (C2 + victim tracking)
  backup      Run backup folder encryption dropper (targets D:\Backup)
  backup-exe  Create standalone EXE dropper for backup encryption
  decrypt     Run backup folder decryption tool (requires encryption key)
  dropper-gui Run advanced dropper creator GUI (creates PS1/BAT/EXE droppers)
  backup-exe-create Create standalone backup folder encryption EXE dropper
  demo        Run the full demo sequence
  reset       Reset the test environment

Examples:
  python run.py setup           # First-time setup
  python run.py train           # Train the model
  python run.py dashboard       # Start the dashboard
  python run.py attack          # Simulate ransomware
  python run.py benign backup   # Simulate backup operation
  python run.py spreading       # Demonstrate spreading concepts
  python run.py payload         # Simulate payload dropping
  python run.py database        # Load threat database for blocking
  python run.py interactive     # Run interactive file selector (GUI)
  python run.py targeted        # Run targeted injection on test files
  python run.py linux           # Run portable Linux ransomware
  python run.py injector        # Demonstrate injection techniques
  python run.py injector docker # Inject into Docker environment
  python run.py comprehensive  # Run complete management simulation
  python run.py backup         # Run backup folder encryption dropper
  python run.py backup-exe     # Create standalone EXE dropper
  python run.py decrypt        # Run backup folder decryption tool
  python run.py dropper-gui    # Run advanced dropper creator GUI
  python run.py backup-exe-create # Create standalone EXE dropper
        """
    )
    
    parser.add_argument('command', nargs='?', default='help',
                        help='Command to run')
    parser.add_argument('args', nargs='*', help='Additional arguments')
    parser.add_argument('--variant', type=str, default='A',
                        help='Ransomware variant (A or B)')
    parser.add_argument('--restore', action='store_true',
                        help='Restore files after ransomware simulation')
    
    args = parser.parse_args()
    
    print_banner()
    
    commands = {
        'setup': setup,
        'download': download_dataset,
        'preprocess': preprocess,
        'train': train,
        'dashboard': dashboard,
        'guardian': guardian,
        'attack': lambda: ransomware(args.variant, args.restore),
        'ransomware': lambda: ransomware(args.variant, args.restore),
        'benign': lambda: benign(args.args[0] if args.args else 'backup'),
        'spreading': spreading,
        'payload': payload_drop,
        'payload-cleanup': payload_cleanup,
        'database': load_database,
        'interactive': interactive_injector,
        'fixed': fixed_interactive,  # Fixed professional dropper creator
        'enhanced': enhanced_interactive,  # Enhanced professional dropper creator
        'targeted': lambda: targeted_injector(args.args[0] if args.args else 'data/test_files'),
        'linux': linux_ransomware,
        'injector': lambda: injector(args.args[0] if args.args else 'qemu'),
        'comprehensive': comprehensive_simulation,
        'backup': backup_encryptor,  # Backup folder encryption dropper
        'backup-exe': backup_encryptor_exe,  # Create standalone EXE
        'decrypt': backup_decryptor,  # Backup folder decryption tool
        'dropper-gui': advanced_dropper_gui,  # Advanced dropper creator GUI
        'backup-exe-create': create_backup_exe,  # Create standalone EXE dropper
        'demo': demo,
        'reset': reset,
        'help': lambda: parser.print_help()
    }
    
    if args.command in commands:
        commands[args.command]()
    else:
        print(f"[ERROR] Unknown command: {args.command}")
        parser.print_help()


def fixed_interactive():
    """Run fixed interactive dropper creator."""
    print("[RUNNING] Fixed Interactive Professional Dropper Creator...")
    cmd = [sys.executable, "fixed_interactive_injector.py"]
    print(f"[CMD] {' '.join(cmd)}")
    subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))

def enhanced_interactive():
    """Run enhanced interactive dropper creator with professional features."""
    print("[RUNNING] Enhanced Interactive Professional Dropper Creator...")
    cmd = [sys.executable, "enhanced_interactive_injector.py"]
    print(f"[CMD] {' '.join(cmd)}")
    subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    main()
