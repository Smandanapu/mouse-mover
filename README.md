# Mouse Mover

![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)

A simple Python GUI application that automatically moves your mouse cursor at configurable intervals to prevent your computer from going to sleep or appearing idle.

## Download

### Pre-built Executables

Download the latest version for your operating system:

- **macOS**: [Mouse-Mover-macOS.dmg](https://github.com/Smandanapu/mouse-mover/actions) - Drag and drop installer
- **Windows**: [Mouse-Mover-Windows.exe](https://github.com/Smandanapu/mouse-mover/actions) - Standalone executable

> **Note**: To download the executables:
> 1. Go to the [Actions tab](https://github.com/Smandanapu/mouse-mover/actions)
> 2. Click on the latest successful workflow run
> 3. Scroll down to "Artifacts" and download your platform's file

### Installation

**macOS:**
1. Download `Mouse-Mover-macOS.dmg`
2. Open the DMG file
3. Drag "Mouse Mover.app" to your Applications folder
4. Launch from Applications

**Windows:**
1. Download `Mouse Mover.exe`
2. Run the executable (no installation needed)
3. You may need to allow it in Windows Defender

### macOS Security Warning

When you first open the app on macOS, you may see a warning: **"Apple could not verify 'Mouse Mover.app' is free of malware"**

This is normal for apps that aren't code-signed with an Apple Developer certificate. The app is safe to use. Here's how to open it:

**Method 1: Right-Click to Open (Easiest)**
1. Locate "Mouse Mover.app" in your Applications folder
2. **Right-click** (or Control-click) on the app
3. Select **"Open"** from the menu
4. Click **"Open"** in the security dialog that appears
5. The app will now open and remember this choice for future launches

**Method 2: System Settings**
1. Try to open the app normally (you'll see the warning)
2. Go to **System Settings** → **Privacy & Security**
3. Scroll down to the **Security** section
4. You'll see a message about "Mouse Mover.app" being blocked
5. Click **"Open Anyway"**
6. Confirm by clicking **"Open"** in the dialog

**Method 3: Remove Quarantine Attribute (Advanced)**
```bash
xattr -d com.apple.quarantine "/Applications/Mouse Mover.app"
```

> **Note**: This warning appears because the app is not code-signed with an Apple Developer certificate ($99/year). The app is open source and safe to use.

## Features

- **Configurable Movement Interval**: Set how often the mouse moves (1-10 seconds)
- **Adjustable Movement Range**: Control how far the mouse moves (10-200 pixels)
- **Cross-Platform Support**: Works on macOS with native fallback when pyautogui is unavailable
- **Simple GUI**: Easy-to-use interface with start/stop controls
- **Thread-Safe**: Mouse movement runs in background thread for responsive UI

## Prerequisites

### macOS Setup

This application requires Python 3.13 with tkinter support. The easiest way to set this up is with Homebrew:

```bash
# Install Homebrew Python 3.13
brew install python@3.13

# Install tkinter support for Python 3.13
brew install python-tk@3.13
```

## Installation & Usage

### Option 1: Using the Launch Script (Recommended)

Simply run the provided launch script:

```bash
./run.sh
```

The script will automatically:
- Create a virtual environment if needed
- Install required dependencies
- Launch the application

### Option 2: Manual Setup

1. Create a virtual environment:
```bash
/opt/homebrew/bin/python3.13 -m venv venv
```

2. Activate the virtual environment:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install pyautogui
```

4. Run the application:
```bash
python main.py
```

## How to Use

1. **Launch the Application**: Use `./run.sh` or follow manual setup
2. **Configure Settings**:
   - **Interval**: How often to move the mouse (in seconds)
   - **Movement Range**: Maximum distance to move mouse (in pixels)
3. **Start Moving**: Click "Start Moving" to begin automatic mouse movement
4. **Stop Moving**: Click "Stop Moving" to stop the mouse movement
5. **Close Application**: Close the window to exit

## Technical Details

### Mouse Control Methods

The application uses two mouse control methods:

1. **PyAutoGUI** (Primary): Full-featured cross-platform mouse control
2. **macOS Native** (Fallback): Uses AppleScript when PyAutoGUI is unavailable

### Safety Features

- Mouse movement stays within screen boundaries
- Responsive stop functionality - stops quickly when requested
- Configurable movement patterns to appear more natural
- Thread-safe implementation prevents GUI freezing

## Troubleshooting

### "tkinter import error"

Make sure you're using Homebrew Python 3.13 with tkinter support:
```bash
brew install python@3.13 python-tk@3.13
```

### "pyautogui not installed"

The application will work with native macOS mouse control, but for full functionality:
```bash
source venv/bin/activate
pip install pyautogui
```

### Permission Issues on macOS

You may need to grant accessibility permissions to Terminal or your Python executable in:
**System Preferences → Security & Privacy → Privacy → Accessibility**

## Files

```text
.
├── LICENSE
├── README.md
├── main.py
├── requirements.txt
├── run.sh
└── venv/
```

## Dependencies

- `tkinter`: GUI framework (included with Python)
- `pyautogui`: Cross-platform mouse control
- `threading`: Background mouse movement
- `subprocess`: macOS native mouse control fallback

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).