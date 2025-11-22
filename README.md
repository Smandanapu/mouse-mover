# Mouse Jiggler

Keep your computer awake by automatically moving your mouse cursor at regular intervals.

## Features

- 🟢 **Easy to use** - Simple START/STOP controls with colorful buttons
- 🎯 **Customizable** - Adjust movement interval and range
- 📝 **Activity logging** - See exactly when and where the cursor moves
- 🔒 **Privacy-focused** - Runs locally, no data collection
- 🎨 **Modern UI** - Clean dark theme interface

## Installation

### macOS

1. **Download** the latest `Mouse-Jiggler.dmg` from the [Releases](https://github.com/Smandanapu/mouse-mover/releases) page
2. **Open** the downloaded DMG file
3. **Drag** Mouse Jiggler to your Applications folder
4. **Launch** Mouse Jiggler from Applications

### Windows

1. **Download** the latest `Mouse-Jiggler.exe` from the [Releases](https://github.com/Smandanapu/mouse-mover/releases) page
2. **Run** the executable (you may need to click "More info" → "Run anyway" if Windows Defender warns you)

## Required Permissions (macOS)

**Important:** Mouse Jiggler needs Accessibility permissions to control your mouse.

### First-time Setup

When you first launch Mouse Jiggler and click START:

1. macOS will show a dialog: **"Mouse Jiggler would like to control this computer using accessibility features"**
2. Click **"Open System Settings"**
3. In System Settings, toggle **ON** the switch next to "Mouse Jiggler"
4. Close System Settings and return to Mouse Jiggler
5. Click **START** again - it should now work!

### Manual Permission Setup

If the automatic prompt doesn't appear:

1. Open **System Settings** (or System Preferences on older macOS)
2. Go to **Privacy & Security** → **Accessibility**
3. Click the **lock icon** 🔒 and enter your password
4. Click the **+ button** to add an app
5. Navigate to **Applications** and select **Mouse Jiggler**
6. Make sure the checkbox next to Mouse Jiggler is **checked** ✅
7. Close System Settings

### Troubleshooting Permissions

If the cursor still doesn't move after granting permissions:

1. Open **System Settings** → **Privacy & Security** → **Accessibility**
2. **Remove** Mouse Jiggler from the list (click the **-** button)
3. **Restart your Mac** (this clears the permission cache)
4. Launch Mouse Jiggler again and grant permissions when prompted

## How to Use

1. **Launch** Mouse Jiggler
2. **Adjust settings** (optional):
   - **Interval**: How often to move the cursor (1-60 seconds)
   - **Range**: How far to move the cursor (10-500 pixels)
3. Click the **green START button** to begin
4. The cursor will move automatically at your specified interval
5. Click the **red STOP button** to stop movement
6. Check the **Activity Log** to see movement history

## Tips

- **Test first**: Use "Test Single Move" to verify permissions are working
- **Adjust range**: Lower range (10-50px) is subtle, higher range (100-500px) is more noticeable
- **Set interval**: Shorter intervals (1-5s) keep your computer very active, longer intervals (30-60s) are less intrusive
- **Check the log**: The Activity Log shows exactly when the cursor moved and if there were any errors

## Building from Source

```bash
# Clone the repository
git clone https://github.com/Smandanapu/mouse-mover.git
cd mouse-mover

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run from source
python3 main.py

# Or build executable
python3 build.py
```

## License

MIT License - See [LICENSE](LICENSE) file for details

## Support

If you encounter issues:
1. Check the Activity Log for error messages
2. Verify Accessibility permissions are enabled
3. Try the "Test Single Move" button
4. On macOS, restart your computer if permissions aren't working

---

**Note:** This app is designed to prevent your computer from going to sleep during presentations, long downloads, or other tasks where you need to stay active. Use responsibly!