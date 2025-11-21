#!/bin/bash
# Mouse Mover Launch Script
# This script ensures the correct Python version and virtual environment are used

# Change to the script directory
cd "$(dirname "$0")"

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    /opt/homebrew/bin/python3.13 -m venv venv
    source venv/bin/activate
    echo "Installing pyautogui..."
    pip install pyautogui
else
    # Activate existing virtual environment
    source venv/bin/activate
fi

# Run the mouse mover application
python main.py