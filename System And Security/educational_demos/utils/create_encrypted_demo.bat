@echo off
echo Creating properly encrypted educational files...

REM Create directory
mkdir encryption_demo 2>nul

REM Create original file with sensitive content
echo CONFIDENTIAL PROJECT DATA > encryption_demo\project_notes.txt
echo ========================== >> encryption_demo\project_notes.txt
echo RANSOMWARE DETECTION SYSTEM >> encryption_demo\project_notes.txt
echo -------------------------- >> encryption_demo\project_notes.txt
echo Project Goals: >> encryption_demo\project_notes.txt
echo 1. Implement machine learning model >> encryption_demo\project_notes.txt
echo 2. Create real-time monitoring system >> encryption_demo\project_notes.txt
echo 3. Build dashboard interface >> encryption_demo\project_notes.txt
echo 4. Conduct security testing >> encryption_demo\project_notes.txt
echo 5. Prepare presentation materials >> encryption_demo\project_notes.txt
echo. >> encryption_demo\project_notes.txt
echo SENSITIVE RESEARCH DATA - MUST BE PROTECTED >> encryption_demo\project_notes.txt

echo [ORIGINAL] Created readable project notes file

REM Generate encryption key using Python
python -c "from cryptography.fernet import Fernet; key=Fernet.generate_key(); open('encryption_demo/key.key', 'wb').write(key); print('[KEY] Generated encryption key')"

REM Encrypt the file using Python
python -c "from cryptography.fernet import Fernet; key=open('encryption_demo/key.key', 'rb').read(); data=open('encryption_demo/project_notes.txt', 'rb').read(); encrypted=Fernet(key).encrypt(data); open('encryption_demo/project_notes.txt', 'wb').write(encrypted); print('[ENCRYPTED] File properly encrypted')"

REM Rename encrypted file
ren "encryption_demo\project_notes.txt" "project_notes.txt.encrypted"

echo [RENAMED] File renamed with .encrypted extension

echo.
echo ==============================================
echo EDUCATIONAL ENCRYPTION COMPLETE!
echo ==============================================
echo ✅ Original file was human-readable
echo ✅ File is now properly encrypted
echo ✅ Try opening the .encrypted file - it should be unreadable!
echo ✅ This demonstrates real ransomware behavior
echo ==============================================

REM Create explanation file
echo ==============================================> encryption_demo\EXPLANATION.txt
echo EDUCATIONAL RANSOMWARE ENCRYPTION>> encryption_demo\EXPLANATION.txt
echo ==============================================>> encryption_demo\EXPLANATION.txt
echo.>> encryption_demo\EXPLANATION.txt
echo This file demonstrates proper file encryption>> encryption_demo\EXPLANATION.txt
echo that makes files truly inaccessible without>> encryption_demo\EXPLANATION.txt
echo the decryption key.>> encryption_demo\EXPLANATION.txt
echo.>> encryption_demo\EXPLANATION.txt
echo Files in this directory:>> encryption_demo\EXPLANATION.txt
echo - project_notes.txt.encrypted (truly encrypted)>> encryption_demo\EXPLANATION.txt
echo - key.key (decryption key)>> encryption_demo\EXPLANATION.txt
echo.>> encryption_demo\EXPLANATION.txt
echo This simulates how real ransomware works!>> encryption_demo\EXPLANATION.txt
echo ==============================================>> encryption_demo\EXPLANATION.txt

echo [INFO] Created explanation file