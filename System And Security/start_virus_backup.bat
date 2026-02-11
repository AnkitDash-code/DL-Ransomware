@echo off
REM VIRUS SIMULATOR FOR BACKUP DIRECTORY MONITORING
REM Runs backup folder encryption against D:\Backup directory
REM Educational purposes only

title Virus Simulator - Backup Directory Target
echo ==================================================
echo   RANSOMWARE SIMULATOR - BACKUP DIRECTORY
echo   Target: D:\Backup
echo ==================================================
echo This runs the backup folder encryption simulator
echo against the D:\Backup directory
echo Features: Real backup folder encryption, key generation, recovery demo
echo ==================================================
echo.

REM Check if D:\Backup exists
if not exist "D:\Backup" (
    echo [ERROR] D:\Backup directory not found!
    echo Please run start_antivirus_backup.bat first to create the directory
    echo or create D:\Backup manually with test files
    pause
    exit /b 1
)

cd /d "C:\Users\Kanhaiya\System And Security\core_system"

echo Running backup folder encryption on D:\Backup...
echo Target directory: D:\Backup
echo.

REM Run backup encryptor targeting D:\Backup
python -c "
import os
import sys
sys.path.append('.')
from simulators.backup_encryptor import BackupFolderEncryptor

class BackupTargetEncryptor(BackupFolderEncryptor):
    def __init__(self):
        super().__init__()
        self.target_directory = r'D:\Backup'
        self.encryption_extension = '.backup_locked'
    
    def run_demo(self):
        print('=== BACKUP FOLDER ENCRYPTION DEMO ===')
        print(f'Target Directory: {self.target_directory}')
        print()
        
        # Check if directory exists and has files
        if not os.path.exists(self.target_directory):
            print('[ERROR] Target directory does not exist')
            return
            
        files = [f for f in os.listdir(self.target_directory) 
                if os.path.isfile(os.path.join(self.target_directory, f))]
        
        if not files:
            print('[WARNING] No files found in target directory')
            print('Creating sample files for demonstration...')
            
            # Create sample files
            sample_files = {
                'important_backup.txt': 'This contains important backup data that should be protected.',
                'financial_records.csv': 'Financial backup records, account numbers, transaction history.',
                'system_config.json': '{\"backup_settings\": true, \"encryption_enabled\": false}',
                'personal_photos.zip': 'Archive of family photos and personal images.',
                'work_documents.rar': 'Compressed work documents and project files.'
            }
            
            for filename, content in sample_files.items():
                filepath = os.path.join(self.target_directory, filename)
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f'[CREATED] {filename}')
            
            files = list(sample_files.keys())
        
        print(f'[FILES] Found {len(files)} files to encrypt:')
        for f in files:
            print(f'  - {f}')
        print()
        
        # Generate encryption key and encrypt
        key = self.generate_key()
        print(f'[KEY] Encryption Key Generated: {key.decode()}')
        print()
        
        # Perform encryption
        self.encrypt_backup_folder()
        
        print()
        print('[COMPLETE] Backup folder encryption demo finished')
        print(f'Recovery key: {key.decode()}')
        return key

# Run the backup encryption demo
encryptor = BackupTargetEncryptor()
recovery_key = encryptor.run_demo()
"

echo.
echo ==================================================
echo Backup directory attack simulation completed
echo Check antivirus dashboard for detection alerts
echo Recovery key displayed above for decryption demo
echo ==================================================
pause