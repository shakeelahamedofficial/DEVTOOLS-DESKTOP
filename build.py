"""
DevTools Desktop — Build Script
Automates tests, PyInstaller packaging, and ZIP creation.
"""

import os
import sys
import shutil
import subprocess
import zipfile
from pathlib import Path

# Extract version from branding (rudimentary parse to avoid importing if env is dirty)
VERSION = "1.0.0"

def run_tests():
    print("Running tests...")
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/"])
    if result.returncode != 0:
        print("Tests failed! Aborting build.")
        sys.exit(1)
    print("Tests passed.")

def clean_build():
    print("Cleaning previous builds...")
    dirs_to_clean = ["build", "dist", "release"]
    for d in dirs_to_clean:
        if os.path.exists(d):
            shutil.rmtree(d)
    os.makedirs("release", exist_ok=True)
    print("Cleaned.")

def package_exe():
    print("Packaging executable with PyInstaller...")
    
    # We create a simple PyInstaller spec implicitly via command line
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--windowed", # No console
        "--name", "DevTools",
        "--clean",
        "--noupx",
        "--icon", "app/public/icon.ico",
        "--add-data", "app/public;app/public",
        "app/main.py"
    ]
    
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("PyInstaller failed! Aborting.")
        sys.exit(1)
    print("Executable packaged.")

def create_release():
    print("Creating release package...")
    
    dist_dir = Path("dist/DevTools")
    if not dist_dir.exists():
        print("dist/DevTools not found.")
        sys.exit(1)
        
    # Copy documentation files
    docs = ["README.md", "USER_GUIDE.md", "LICENSE.txt", "CHANGELOG.md", "PRIVACY.md", "SUPPORT.md"]
    for doc in docs:
        if os.path.exists(doc):
            shutil.copy(doc, dist_dir / doc)
            
    # Create ZIP
    zip_filename = f"release/DevTools-Desktop-v{VERSION}-Windows.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, "dist")
                zipf.write(file_path, arcname)
                
    print(f"Release created: {zip_filename}")

if __name__ == "__main__":
    print(f"Starting DevTools Desktop Build (v{VERSION})")
    run_tests()
    clean_build()
    package_exe()
    create_release()
    print("Build Complete!")
