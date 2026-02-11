# Complete Security System Instructions

## 🛡️ System Overview

This document provides comprehensive instructions for using the Zero-Day Ransomware Detection System, including antivirus protection, virus simulation, dropper creation, and file recovery tools.

## 🎯 Overview

This document provides step-by-step instructions for executing educational ransomware simulations and detecting them using the Zero-Day Ransomware Detection System.

## ⚠️ IMPORTANT SAFETY NOTICE

**This is for EDUCATIONAL PURPOSES ONLY**
- All activities must be conducted in isolated environments
- Never run on production systems or real data
- Ensure proper backups before any testing
- Understand that these tools demonstrate real attack vectors
- All tools include built-in educational warnings
- Default target directories are safe educational locations

## 🚀 System Setup Instructions

### 1. Environment Preparation
```bash
# Navigate to project directory
cd "System And Security"

# Activate virtual environment
core_system\myenv\Scripts\activate

# Verify all dependencies are installed
pip install -r core_system/requirements.txt
```

### 2. Quick Access Tools Setup
The system provides multiple easy-access batch files in the root directory:

- **`backup_decryptor.bat`** - Decrypt backup folder files (NEW - easy access)
- **`recover_files.bat`** - General file recovery tool
- **`start_antivirus_*.bat`** - Various antivirus configurations
- **`start_virus_*.bat`** - Various virus simulation scripts
- **`start_dropper_gui.bat`** - Launch advanced dropper creator
- **`start_injector_gui.bat`** - Launch interactive file injector

### 2. Test Environment Setup
```bash
# Create isolated test directory
mkdir test_environment
cd test_environment

# Generate sample files for testing
python ../educational_demos/ransomware_process_test.py
```

## 🛡️ Antivirus System Usage

### Starting Antivirus Protection

#### 1. Core System Monitoring
```bash
# Start antivirus with active intervention for core system files
start_antivirus_core.bat

# What this does:
# - Monitors C:\Users\Kanhaiya\System And Security\core_system\data\test_files
# - Provides real-time threat detection
# - Automatically terminates malicious processes
# - Attempts file recovery during attacks
# - Opens web dashboard in browser
```

#### 2. Backup Directory Monitoring
```bash
# Monitor D:\Backup directory specifically
start_antivirus_backup.bat

# Features:
# - Watches D:\Backup for ransomware activity
# - Real-time file change detection
# - Process behavior analysis
# - Web-based dashboard interface
```

#### 3. Command-Line Monitoring
```bash
# Start monitoring via command line
python core_system/run.py monitor

# Start with dashboard
python core_system/run.py dashboard

# Check system status
python core_system/run.py status
```

### Antivirus Dashboard Features

The web dashboard (http://localhost:8501) provides:
- Real-time threat detection statistics
- Process monitoring visualization
- File system change tracking
- Intervention success metrics
- Recovery attempt results
- System resource usage

### Active Intervention Capabilities
- **Process Termination**: Automatically kills detected malicious processes
- **File Recovery**: Attempts to decrypt files during active attacks
- **Static Blocking**: Prevents known malicious patterns
- **Behavioral Analysis**: Monitors suspicious process chains

## 💀 Virus Simulation Instructions

### Method 1: Backup Folder Encryption
```bash
# Encrypt files in D:\Backup directory
python core_system/run.py backup

# Real encryption demonstration (shows actual encryption)
start_virus_backup_real.bat

# What happens:
# - Creates/uses D:\Backup directory
# - Encrypts all files with .backup_locked extension
# - Generates and displays encryption key
# - Creates ransom note
# - Shows recovery instructions
```

### Method 2: Core System Attack
```bash
# Attack core system test files
python core_system/run.py attack

# Real encryption version
start_virus_core_real.bat

# Target: core_system/data/test_files directory
# Extension: .core_encrypted
```

### Method 3: GUI-Based Dropper Creation (Recommended)

#### Step 1: Launch Dropper Creator GUI
```bash
# Easy access from root directory
start_dropper_gui.bat

# Or from core system directory
cd core_system
python run.py dropper-gui

# Alternative: Interactive file injector
cd educational_demos
python simulators/interactive_injector.py
# Or use: start_injector_gui.bat
```

#### Step 2: Create Educational Dropper
1. **Select Target Directory**: Choose which directory to encrypt when executed (default: D:\Backup)
2. **Configure Settings**:
   - Choose dropper formats (PowerShell, Batch, Executable)
   - Pre-generated encryption key provided
   - Set output directory for created droppers
3. **Key Management**:
   - Copy the displayed encryption key
   - Save key to file for later use
   - Key required for file recovery
4. **Create Dropper**: Click "Create Selected Droppers" button
5. **Verify Creation**: Check output directory for created files

### Advanced Dropper Features
- **Multiple Formats**: Create .ps1, .bat, and .exe droppers simultaneously
- **Professional Templates**: Production-ready dropper code
- **Educational Warnings**: Built-in safety notifications
- **Key Preview**: View encryption key before creation
- **Output Management**: Organized dropper storage

#### Step 3: Execute Dropper
```bash
# Run the created dropper file
python dropper_filename_dropper.py
# or double-click the batch/PowerShell dropper

# For executable droppers
./dropper_filename.exe

# Educational warning will appear before execution
```

### Dropper Execution Safety
- All droppers include educational warnings
- Default targets are safe test directories
- No real system harm intended
- Clear distinction between simulation and real attacks

### Method 4: Direct Simulation Execution

#### Using Pre-built Simulators
```bash
# Launch comprehensive ransomware simulator
python educational_demos/comprehensive_ransomware_simulator.py

# Run specific variant simulations
python educational_demos/simulators/ransomware_sim.py
python educational_demos/simulators/linux_ransomware.py

# Educational spreading simulation
python core_system/run.py spreading

# Payload dropper simulation
python core_system/run.py payload
```

#### Manual Execution Commands
```bash
# Execute with specific parameters
python educational_demos/manual_dropper.py --target-dir "test_files" --extension ".edu_lock"

# Run with educational safety features
python educational_demos/safe_education_demo/simple_format_encryption.py
```

## 🛡️ Detection System Activation

### 1. Start Real-time Monitoring
```bash
# Launch main detection system
python core_system/run.py monitor

# Alternative: Start with specific configuration
python core_system/run.py --mode=monitor --config=detection_config.json
```

### 2. Dashboard Access
```bash
# Open web-based monitoring dashboard
python core_system/run.py dashboard

# Access via browser at: http://localhost:8501
```

### 3. Manual Scanning Operations
```bash
# Scan specific directory
python core_system/run.py scan --path "C:\test_directory"

# System-wide scan
python core_system/run.py scan --system-wide

# Quick threat assessment
python core_system/run.py quick-scan
```

## 📊 Detection Process Workflow

### Real-time Monitoring Sequence
1. **Process Monitoring**: Continuous process tree analysis
2. **Behavioral Analysis**: API call sequence examination
3. **File System Watch**: Real-time file change detection
4. **Pattern Recognition**: ML model application
5. **Threat Classification**: Risk assessment and scoring
6. **Response Trigger**: Automated protective actions

### Detection Indicators
The system monitors for these ransomware behaviors:
- Rapid file encryption patterns
- Extension changes (.locked, .encrypted, etc.)
- Suspicious process creation chains
- Unusual file access sequences
- Registry modification spikes
- Network communication anomalies

## 🆘 File Recovery Instructions

### 1. Backup Folder Decryption (NEW - Easy Access)

#### Using Root Script (Recommended)
```bash
# Easy access from root directory
backup_decryptor.bat

# This will:
# - Check for Python availability
# - Navigate to core_system directory
# - Run backup_decryptor.py
# - Prompt for encryption key
# - Decrypt all .backup_locked files in D:\Backup
```

#### Using Core System Tool
```bash
# Navigate to core system
cd core_system

# Run decryption tool
python simulators/backup_decryptor.py

# Or use run.py interface
python run.py decrypt
```

### 2. General File Recovery

#### Using Batch Script
```bash
# Easy access recovery tool
recover_files.bat

# Recovers files with .core_encrypted and .backup_encrypted extensions
# Searches in core_system/data/test_files and D:\Backup
```

#### Using Python Tool
```bash
# Direct Python access
cd core_system
python file_recovery.py
```

### 3. Recovery Process Steps

#### Step 1: Obtain Encryption Key
- Key is displayed when files are encrypted
- Look for output like: `ENCRYPTION KEY: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=`
- Save this key immediately - it's required for recovery

#### Step 2: Run Recovery Tool
```bash
# For backup folder files
backup_decryptor.bat

# For general encrypted files
recover_files.bat
```

#### Step 3: Enter Key When Prompted
```
[STATUS] Starting backup folder decryption...
[KEY] Enter the encryption key (base64 format):
> xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=
```

#### Step 4: Confirm Recovery
```
[FOUND] 5 encrypted files to recover:
  - document1.txt.backup_locked -> document1.txt
  - photo.jpg.backup_locked -> photo.jpg
  - data.xlsx.backup_locked -> data.xlsx

Proceed with file recovery? (y/N): y
```

#### Step 5: Review Results
```
==================================================
FILE RECOVERY COMPLETE
==================================================
Successfully recovered: 5 files
Failed to recover: 0 files
==================================================
```

### 4. Recovery Tool Features

#### Key Validation
- Automatically validates encryption key format
- Tests key with sample encryption/decryption
- Provides clear error messages for invalid keys

#### Multi-format Support
- Handles `.backup_locked` extension (backup folder)
- Handles `.core_encrypted` extension (core system)
- Handles `.encrypted` extension (general)

#### Batch Processing
- Recovers multiple files simultaneously
- Shows progress for each file
- Maintains original file names and extensions

#### Error Handling
- Gracefully handles corrupted files
- Continues recovery even if some files fail
- Provides detailed failure information

### 5. Recovery Best Practices

#### Key Management
- **Save Immediately**: Copy encryption key as soon as it's displayed
- **Multiple Copies**: Store key in multiple safe locations
- **Label Keys**: Associate keys with specific encryption sessions
- **Never Lose**: Without the key, files cannot be recovered

#### Recovery Timing
- **Immediate Recovery**: Run recovery tool as soon as possible
- **Before System Changes**: Recover files before making system modifications
- **Test Environment**: Always test recovery in isolated environments

#### Verification
- **File Integrity**: Check that recovered files open correctly
- **Content Verification**: Compare with known good copies if available
- **Complete Recovery**: Ensure all expected files are restored

## 🔍 Verification and Testing

### 1. Successful Encryption Verification
```bash
# Check encrypted files
dir test_files\*.locked
dir test_files\*.encrypted

# Verify files are truly encrypted
python -c "open('test_files/sample.txt.locked', 'r').read()"
# Should show UnicodeDecodeError or random characters
```

### 2. Detection System Validation
```bash
# Verify monitoring is active
python core_system/run.py status

# Check recent detections
python core_system/run.py recent-alerts

# Review system logs
type logs\detection_log.txt
```

### 3. Recovery Process Testing
```bash
# Test file recovery functionality
python core_system/run.py recover --key recovery_key.key

# Verify restored files
dir test_files\*.restored
fc test_files\original.txt test_files\restored_original.txt
```

## 🛠️ Troubleshooting Common Issues

### Antivirus Issues

#### Issue 1: Dashboard Not Opening
```bash
# Solution: Check if port 8501 is available
netstat -an | findstr :8501

# Kill conflicting processes
taskkill /f /im python.exe

# Restart with verbose output
python core_system/run.py dashboard --verbose
```

#### Issue 2: Monitoring Not Detecting Threats
```bash
# Check if guardian daemon is running
tasklist | findstr python

# Restart monitoring services
python core_system/run.py restart-monitoring

# Verify model loading
python core_system/run.py test-model
```

#### Issue 3: Active Intervention Not Working
```bash
# Check administrative privileges
whoami /groups | findstr "High Mandatory Level"

# Run as administrator if needed
# Right-click command prompt -> Run as administrator

# Verify process termination permissions
python core_system/run.py diagnostics
```

### Dropper Creation Issues

#### Issue 4: GUI Not Launching
```bash
# Solution: Check dependencies
pip install tkinter
python -c "import tkinter; print('Tkinter available')"

# Alternative command-line approach
python educational_demos/ransomware_process_test.py --no-gui
```

#### Issue 5: Dropper Creation Fails
```bash
# Check output directory permissions
icacls . /grant %USERNAME%:F

# Verify Python path
echo %PATH%
where python

# Test with simple dropper
python core_system/run.py backup-exe-create
```

### Recovery Issues

#### Issue 6: Invalid Encryption Key
```bash
# Check key format requirements
# Keys should be 44 characters ending with =

# Test key validity
python -c "from cryptography.fernet import Fernet; Fernet(b'your_key_here')"

# Common fixes:
# - Ensure no extra spaces
# - Check for missing = padding
# - Verify base64 encoding
```

#### Issue 7: Files Not Found for Recovery
```bash
# Check target directories exist
dir "D:\Backup"
dir "core_system\data\test_files"

# Verify file extensions
dir *.backup_locked
dir *.core_encrypted

# Search system-wide
where /r C:\ *.backup_locked
```

### System Integration Issues

#### Issue 8: Python Path Issues
```bash
# Add Python to PATH permanently
setx PATH "%PATH%;C:\Python39;C:\Python39\Scripts"

# Verify installation
python --version
pip --version

# Reinstall if needed
python -m pip install --upgrade pip
pip install -r core_system/requirements.txt
```

#### Issue 9: Missing Dependencies
```bash
# Install all required packages
pip install -r core_system/requirements.txt

# Install specific missing packages
pip install cryptography psutil watchdog streamlit

# Verify installations
python -c "import cryptography, psutil, watchdog, streamlit; print('All packages OK')"
```

## 📈 Performance Optimization

### Antivirus Performance
```bash
# Adjust monitoring intensity
python core_system/run.py --monitoring-interval=0.5

# Limit CPU usage for monitoring
python core_system/run.py --cpu-limit=50

# Configure memory thresholds
python core_system/run.py --memory-threshold=80

# Disable dashboard for performance
python core_system/run.py monitor --no-dashboard
```

### Dropper Creation Optimization
```bash
# Batch create multiple dropper types
python core_system/run.py dropper-gui --batch-mode

# Use pre-compiled templates
python core_system/run.py backup-exe --template-optimized

# Parallel processing for large files
python core_system/run.py backup-exe --parallel
```

### Custom Configuration
Create `custom_config.json`:
```json
{
    "monitoring": {
        "scan_interval": 0.2,
        "process_depth": 3,
        "file_watch_patterns": ["*.txt", "*.doc", "*.pdf", "*.jpg", "*.png"],
        "directories": [
            "D:\\Backup",
            "C:\\Users\\Kanhaiya\\System And Security\\core_system\\data\\test_files"
        ]
    },
    "detection": {
        "sensitivity": "high",
        "false_positive_tolerance": 0.05,
        "response_delay": 1.0,
        "active_intervention": true,
        "auto_recovery": true
    },
    "dropper_creation": {
        "default_formats": ["ps1", "bat"],
        "target_directory": "D:\\Backup",
        "key_persistence": true,
        "educational_warnings": true
    },
    "recovery": {
        "auto_search_directories": [
            "D:\\Backup",
            "core_system\\data\\test_files"
        ],
        "supported_extensions": [".backup_locked", ".core_encrypted", ".encrypted"],
        "key_validation": true
    },
    "logging": {
        "detail_level": "verbose",
        "retention_days": 30,
        "log_threats": true,
        "log_interventions": true,
        "log_recovery_attempts": true
    }
}
```

## 🎓 Educational Scenarios

### Scenario 1: Basic Ransomware Detection
```bash
# Setup
python educational_demos/setup_basic_scenario.py

# Execute attack
python educational_demos/basic_ransomware_attack.py

# Observe detection
python core_system/run.py monitor-scenario
```

### Scenario 2: Advanced Evasion Techniques
```bash
# Setup advanced scenario
python educational_demos/setup_advanced_scenario.py

# Execute sophisticated attack
python educational_demos/advanced_ransomware_attack.py

# Test detection capabilities
python core_system/run.py test-evasion-detection
```

### Scenario 3: Recovery Demonstration
```bash
# Create encrypted environment
python educational_demos/create_encrypted_environment.py

# Demonstrate recovery process
python educational_demos/recovery_demonstration.py

# Show backup importance
python educational_demos/backup_importance_demo.py
```

## 🔐 Security Best Practices

### During Testing
- Always use isolated virtual machines
- Disable network connections when possible
- Take snapshots before testing
- Use dedicated test user accounts
- Monitor system logs continuously

### Post-Testing Cleanup
```bash
# Remove test artifacts
python core_system/reset_test_files.py

# Clear system logs
python core_system/run.py clear-logs

# Reset monitoring configuration
python core_system/run.py factory-reset
```

## 📚 Complete System Reference

### Quick Command Reference

#### Antivirus Commands
```bash
# Start monitoring
start_antivirus_core.bat          # Core system protection
start_antivirus_backup.bat        # Backup directory monitoring
python core_system/run.py monitor # Command-line monitoring
python core_system/run.py dashboard # Web dashboard

# System management
python core_system/run.py status     # Check system status
python core_system/run.py diagnostics # System diagnostics
python core_system/run.py restart-monitoring # Restart services
```

#### Virus Simulation Commands
```bash
# Encryption attacks
python core_system/run.py backup        # Backup folder encryption
python core_system/run.py attack        # Core system attack
start_virus_backup_real.bat            # Real encryption demo
start_virus_core_real.bat              # Real core attack demo

# Dropper creation
start_dropper_gui.bat                  # Advanced dropper GUI
start_injector_gui.bat                 # Interactive injector
python core_system/run.py dropper-gui  # Command-line dropper
python core_system/run.py interactive  # File injector
```

#### Recovery Commands
```bash
# File decryption
backup_decryptor.bat                   # NEW - Easy backup decryption
recover_files.bat                      # General file recovery
python core_system/run.py decrypt      # Command-line decryption
python core_system/file_recovery.py    # Direct recovery tool
```

### Directory Structure
```
System And Security/
├── core_system/                    # Main system components
│   ├── antivirus/                  # Antivirus modules
│   ├── data/                       # Test files and data
│   ├── model/                      # ML models
│   ├── monitor/                    # Monitoring components
│   ├── simulators/                 # Simulation tools
│   └── *.py                        # Core system files
├── educational_demos/              # Educational tools
│   ├── simulators/                 # Ransomware simulators
│   └── utils/                      # Utility scripts
├── security_tools/                 # Security utilities
│   ├── antivirus/                  # Antivirus components
│   ├── model/                      # Security models
│   └── monitor/                    # Monitoring tools
├── README.md                       # System overview
├── instructions.md                 # Complete usage guide
├── backup_decryptor.bat            # NEW - Easy decryption tool
├── recover_files.bat               # Recovery utility
├── start_*.bat                     # Quick launch scripts
└── *.py                            # Demo and utility scripts
```

## 📞 Support and Documentation

### Additional Resources
- **`README.md`** - Complete system documentation and overview
- **`instructions.md`** - Detailed usage instructions (this document)
- **`core_system/logs/`** - System logs and monitoring data
- **`educational_demos/documentation/`** - Educational materials
- **Online help**: `python core_system/run.py help`

### Reporting Issues
If you encounter problems:
1. Check system requirements are met
2. Verify all dependencies are installed
3. Review error logs in `core_system/logs/`
4. Try running with verbose output: `--verbose` flag
5. Use troubleshooting sections in this document
6. Contact support with detailed error information

### Educational Best Practices
- Always run in isolated environments
- Save encryption keys immediately
- Test recovery procedures before real scenarios
- Document all experimental results
- Follow security research ethics guidelines

---
**Remember: This system is for educational purposes only. Always practice responsible security research.**

---
**Remember: This system is for educational purposes only. Always practice responsible security research.**