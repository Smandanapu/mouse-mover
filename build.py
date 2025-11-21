import PyInstaller.__main__
import sys
import os
import shutil
import subprocess

def create_dmg():
    """Create a DMG installer for macOS."""
    print("\nCreating DMG installer for distribution...")
    
    app_name = "Mouse Mover.app"
    dmg_name = "Mouse-Mover-macOS.dmg"
    
    if not os.path.exists(f"dist/{app_name}"):
        print(f"Error: {app_name} not found in dist folder")
        return
    
    dmg_path = f"dist/{dmg_name}"
    
    # Remove old DMG if exists
    if os.path.exists(dmg_path):
        os.remove(dmg_path)
    
    # Create DMG using create-dmg
    try:
        subprocess.run([
            "create-dmg",
            "--volname", "Mouse Mover",
            "--volicon", f"dist/{app_name}/Contents/Resources/icon-windowed.icns",
            "--window-pos", "200", "120",
            "--window-size", "600", "400",
            "--icon-size", "100",
            "--icon", app_name, "175", "190",
            "--hide-extension", app_name,
            "--app-drop-link", "425", "190",
            dmg_path,
            f"dist/{app_name}"
        ], check=True)
        print(f"[OK] Created: {dmg_path}")
    except subprocess.CalledProcessError:
        # If create-dmg fails, fall back to hdiutil
        print("create-dmg failed, using hdiutil as fallback...")
        temp_dmg = "dist/temp.dmg"
        
        # Create temporary DMG
        subprocess.run([
            "hdiutil", "create",
            "-volname", "Mouse Mover",
            "-srcfolder", f"dist/{app_name}",
            "-ov", "-format", "UDZO",
            temp_dmg
        ], check=True)
        
        # Move to final location
        shutil.move(temp_dmg, dmg_path)
        print(f"[OK] Created: {dmg_path}")
    except FileNotFoundError:
        print("Warning: create-dmg not found. Install with: brew install create-dmg")
        print("Falling back to hdiutil...")
        subprocess.run([
            "hdiutil", "create",
            "-volname", "Mouse Mover",
            "-srcfolder", f"dist/{app_name}",
            "-ov", "-format", "UDZO",
            dmg_path
        ], check=True)
        print(f"[OK] Created: {dmg_path}")

def build():
    print("Starting build process...")
    
    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')

    # Common arguments
    args = [
        'main.py',
        '--name=Mouse Mover',
        '--noconfirm',
        '--clean',
        '--windowed',  # No console window
    ]

    # OS-specific arguments
    if sys.platform == 'darwin':
        # macOS specific - create .app bundle
        print("Configured for macOS build...")
    elif sys.platform == 'win32':
        # Windows specific - single .exe file
        args.extend([
            '--onefile',  # Single .exe file
        ])
        print("Configured for Windows build...")
    
    # Run PyInstaller
    print(f"Running PyInstaller with args: {args}")
    PyInstaller.__main__.run(args)
    print("Build complete! Check the 'dist' folder.")
    
    # Create distribution files
    if sys.platform == 'darwin':
        create_dmg()
    elif sys.platform == 'win32':
        exe_name = "Mouse Mover.exe"
        if os.path.exists(f"dist/{exe_name}"):
            print(f"[OK] Windows executable ready: dist/{exe_name}")
        else:
            print(f"Warning: {exe_name} not found in dist folder")

if __name__ == "__main__":
    build()
