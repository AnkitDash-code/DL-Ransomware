# Ransomware Execution and Detection Instructions

## 🎯 Overview

This document provides step-by-step instructions for executing educational ransomware simulations and detecting them using the Zero-Day Ransomware Detection System.

## ⚠️ IMPORTANT SAFETY NOTICE

**This is for EDUCATIONAL PURPOSES ONLY**
- All activities must be conducted in isolated environments
- Never run on production systems or real data
- Ensure proper backups before any testing
- Understand that these tools demonstrate real attack vectors

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

### 2. Test Environment Setup
```bash
# Create isolated test directory
mkdir test_environment
cd test_environment

# Generate sample files for testing
python ../educational_demos/ransomware_process_test.py
```

## 🔧 Ransomware Execution Instructions

### Method 1: GUI-Based Dropper Creation (Recommended)

#### Step 1: Launch Interactive Injector
```bash
# From core system directory
cd core_system
python run.py interactive
```

#### Step 2: Create Educational Dropper
1. **Select Target Files**: Choose files to convert to droppers
2. **Set Target Directory**: Specify which directory to encrypt when executed
3. **Configure Settings**:
   - Choose dropper type (Python/Batch/PowerShell)
   - Set file extension for encrypted files
   - Configure delay and stealth options
4. **Create Dropper**: Click "Create Dropper" button
5. **Verify Creation**: Check "View Created Droppers" for confirmation

#### Step 3: Execute Dropper
```bash
# Run the created dropper file
python dropper_filename_dropper.py
# or double-click the batch/powerShell dropper
```

### Method 2: Direct Simulation Execution

#### Using Pre-built Simulators
```bash
# Launch comprehensive ransomware simulator
python educational_demos/comprehensive_ransomware_simulator.py

# Run specific variant simulations
python educational_demos/simulators/ransomware_sim.py
python educational_demos/simulators/linux_ransomware.py
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

### Issue 1: GUI Not Launching
```bash
# Solution: Check dependencies
pip install tkinter
python -c "import tkinter; print('Tkinter available')"

# Alternative command-line approach
python educational_demos/ransomware_process_test.py --no-gui
```

### Issue 2: Detection System Not Responding
```bash
# Restart monitoring services
python core_system/run.py restart-monitoring

# Check system resources
python core_system/run.py diagnostics

# Verify model loading
python core_system/run.py test-model
```

### Issue 3: Files Not Encrypting Properly
```bash
# Check encryption library
python -c "from cryptography.fernet import Fernet; print('Crypto OK')"

# Test with simple encryption
python educational_demos/simple_format_encryption/simple_format_encryption.py
```

## 📈 Performance Optimization

### Resource Management
```bash
# Adjust monitoring intensity
python core_system/run.py --monitoring-interval=0.5

# Limit CPU usage
python core_system/run.py --cpu-limit=50

# Configure memory thresholds
python core_system/run.py --memory-threshold=80
```

### Custom Configuration
Create `custom_config.json`:
```json
{
    "monitoring": {
        "scan_interval": 0.2,
        "process_depth": 3,
        "file_watch_patterns": ["*.txt", "*.doc", "*.pdf"]
    },
    "detection": {
        "sensitivity": "high",
        "false_positive_tolerance": 0.05,
        "response_delay": 1.0
    },
    "logging": {
        "detail_level": "verbose",
        "retention_days": 30
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

## 📞 Support and Documentation

### Additional Resources
- `README.md` - Complete system documentation
- `core_system/logs/` - System logs and monitoring data
- `educational_demos/documentation/` - Educational materials
- Online help: `python core_system/run.py help`

### Reporting Issues
If you encounter problems:
1. Check system requirements are met
2. Verify all dependencies are installed
3. Review error logs in `core_system/logs/`
4. Try running with verbose output: `--verbose` flag
5. Contact support with detailed error information

---
**Remember: This system is for educational purposes only. Always practice responsible security research.**