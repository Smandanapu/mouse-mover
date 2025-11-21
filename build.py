import PyInstaller.__main__
import sys
import os
import shutil
import zipfile

def compress_build():
    """Compress the built application for distribution."""
    print("\nCreating compressed archive for distribution...")
    
    if sys.platform == 'darwin':
        # macOS: zip the .app bundle
        app_name = "Mouse Mover.app"
        zip_name = "Mouse-Mover-macOS.zip"
        
        if os.path.exists(f"dist/{app_name}"):
            zip_path = f"dist/{zip_name}"
            
            # Remove old zip if exists
            if os.path.exists(zip_path):
                os.remove(zip_path)
            
            # Create zip file
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                app_path = f"dist/{app_name}"
                for root, dirs, files in os.walk(app_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, 'dist')
                        zipf.write(file_path, arcname)
            
            print(f"✓ Created: {zip_path}")
        else:
            print(f"Warning: {app_name} not found in dist folder")
            
    elif sys.platform == 'win32':
        # Windows: zip the .exe file
        exe_name = "Mouse Mover.exe"
        zip_name = "Mouse-Mover-Windows.zip"
        
        if os.path.exists(f"dist/{exe_name}"):
            zip_path = f"dist/{zip_name}"
            
            # Remove old zip if exists
            if os.path.exists(zip_path):
                os.remove(zip_path)
            
            # Create zip file
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(f"dist/{exe_name}", exe_name)
            
            print(f"✓ Created: {zip_path}")
        else:
            print(f"Warning: {exe_name} not found in dist folder")

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
        # macOS specific
        # args.extend([
        #     '--target-architecture=universal2', # Support both Intel and Apple Silicon
        # ])
        print("Configured for macOS build...")
    elif sys.platform == 'win32':
        # Windows specific
        args.extend([
            '--onefile',  # Single .exe file
        ])
        print("Configured for Windows build...")
    
    # Run PyInstaller
    print(f"Running PyInstaller with args: {args}")
    PyInstaller.__main__.run(args)
    print("Build complete! Check the 'dist' folder.")
    
    # Compress the build
    compress_build()

if __name__ == "__main__":
    build()
