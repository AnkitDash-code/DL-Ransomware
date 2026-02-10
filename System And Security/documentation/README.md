# Zero-Day Ransomware Detection System - Organized Structure

## Directory Organization

### 📁 **core_system/**
Contains the fundamental system components and configuration files:
- `config.py` - Main configuration settings
- `run.py` - Primary command interface and runner
- `requirements.txt` - Python dependencies
- `reset_test_files.py` - Test environment reset utility
- `myenv/` - Python virtual environment

### 📁 **dropper_creation/**
Legitimate-appearing dropper files and creation tools:
- `legitimate_document_processor.py` - Python dropper (appears as document processor)
- `system_maintenance.bat` - Windows batch dropper (appears as maintenance script)
- `system_admin_utility.sh` - Linux shell dropper (appears as admin utility)
- `normal_business_document.pdf` - PDF dropper with embedded JavaScript
- `create_legitimate_pdf.py` - PDF generation tool
- `universal_dropper_generator.py` - Multi-format dropper creator

### 🛡️ **security_tools/**
Core security and antivirus components:
- `antivirus/` - Real-time protection and threat detection
- `model/` - Machine learning models and training components
- `monitor/` - System monitoring and behavioral analysis

### 🎓 **educational_demos/**
Learning materials and demonstration tools:
- Various dropper concept demonstrations
- Simulator tools for security education
- Test files and experimental droppers
- `simulators/` - Educational simulation frameworks

### 📊 **data_files/**
Training data and datasets:
- `data/` - Test files and sample data
- `ransomware_dataset_realistic.csv` - RISS ransomware dataset (1524 samples)

### 📚 **documentation/**
Project documentation and specifications:
- `prompt.txt` - Original project requirements and specifications

## Usage Commands

From the main directory, use the organized run.py:
```bash
# Navigate to core_system directory
cd core_system

# Run system commands
python run.py setup          # Initial setup
python run.py train          # Train ML model
python run.py dashboard      # Start monitoring dashboard
python run.py attack         # Run ransomware simulation
python run.py interactive    # GUI dropper creator
```

## Key Features by Directory

### Core System
- Central command interface
- Configuration management
- Environment setup and maintenance

### Dropper Creation
- Legitimate-appearing malicious files
- Multi-format dropper generation
- Educational security research tools

### Security Tools
- Real-time threat detection
- Machine learning-based analysis
- Active protection mechanisms

### Educational Demos
- Security concept demonstrations
- Safe experimentation environment
- Learning and training materials

This organization maintains clean separation of concerns while keeping all related functionality grouped logically for easy navigation and maintenance.