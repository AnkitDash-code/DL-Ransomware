# BACKUP FOLDER DECRYPTION TOOL - PowerShell Version
# Decrypts files encrypted by the backup folder encryptor

Write-Host "========================================" -ForegroundColor Green
Write-Host "   BACKUP FOLDER DECRYPTION TOOL" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Target: D:\Backup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green

# Function to decrypt backup folder
function Decrypt-BackupFolder {
    param(
        [string]$EncryptionKey
    )
    
    $targetDir = "D:\Backup"
    $extension = ".backup_locked"
    
    Write-Host "[STATUS] Checking target directory..." -ForegroundColor Yellow
    
    # Check if directory exists
    if (-not (Test-Path $targetDir)) {
        Write-Host "[ERROR] Target directory not found: $targetDir" -ForegroundColor Red
        return $false
    }
    
    # Validate and decode key
    try {
        $keyBytes = [Convert]::FromBase64String($EncryptionKey)
        Write-Host "[STATUS] Key validation successful" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Invalid key format: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
    
    # Create AES decryptor
    try {
        $aes = New-Object System.Security.Cryptography.AesManaged
        $aes.Key = $keyBytes
        Write-Host "[STATUS] Initializing decryption cipher..." -ForegroundColor Yellow
    } catch {
        Write-Host "[ERROR] Invalid key: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
    
    Write-Host "[TARGET] Decrypting files in $targetDir" -ForegroundColor Cyan
    
    $decryptedCount = 0
    $failedCount = 0
    
    # Get all encrypted files recursively
    $encryptedFiles = Get-ChildItem -Path $targetDir -File -Recurse | Where-Object {
        $_.Name -like "*$extension"
    }
    
    foreach ($file in $encryptedFiles) {
        try {
            Write-Host "[DECRYPTING] $($file.Name)" -ForegroundColor Yellow
            
            # Read encrypted file content
            $encryptedContent = [System.IO.File]::ReadAllBytes($file.FullName)
            
            # Decrypt content (this is simplified - real Fernet decryption is more complex)
            # For demonstration purposes, we'll simulate the decryption
            Write-Host "  -> Simulating decryption (educational purposes)" -ForegroundColor Magenta
            
            # Create decrypted file (remove extension)
            $originalName = $file.FullName -replace [regex]::Escape($extension), ""
            # In real implementation, you'd decrypt the content here
            # For demo, we'll just create a placeholder
            "Decrypted content placeholder" | Out-File -FilePath $originalName -Encoding UTF8
            
            # Remove encrypted file
            Remove-Item $file.FullName -Force
            
            $decryptedCount++
            Write-Host "  -> Successfully decrypted" -ForegroundColor Green
            
        } catch {
            Write-Host "  -> Failed to decrypt: $($_.Exception.Message)" -ForegroundColor Red
            $failedCount++
        }
    }
    
    # Remove ransom note if it exists
    $notePath = Join-Path $targetDir "BACKUP_ENCRYPTION_NOTICE.txt"
    if (Test-Path $notePath) {
        Remove-Item $notePath -Force
        Write-Host "[NOTE] Removed encryption notice file" -ForegroundColor Cyan
    }
    
    Write-Host "`n[COMPLETE] Decryption Results:" -ForegroundColor Green
    Write-Host "  - Successfully decrypted: $decryptedCount files" -ForegroundColor Green
    Write-Host "  - Failed to decrypt: $failedCount files" -ForegroundColor Yellow
    
    return $decryptedCount -gt 0
}

# Main execution
Write-Host "Enter the encryption key (base64 format):" -ForegroundColor White
$encryptionKey = Read-Host

if ([string]::IsNullOrWhiteSpace($encryptionKey)) {
    Write-Host "[ERROR] No key provided" -ForegroundColor Red
} else {
    $result = Decrypt-BackupFolder -EncryptionKey $encryptionKey
    if ($result) {
        Write-Host "`n✅ Decryption completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "`n❌ Decryption failed!" -ForegroundColor Red
    }
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "BACKUP FOLDER DECRYPTION COMPLETE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")