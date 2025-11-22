import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import random
import platform
import sys
import subprocess
from datetime import datetime

# Try to import pyautogui
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

# Try to import Quartz for macOS fallback
try:
    import Quartz
    QUARTZ_AVAILABLE = True
except ImportError:
    QUARTZ_AVAILABLE = False

class MouseMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Jiggler")
        self.root.geometry("500x700")
        self.root.minsize(400, 600)
        
        # Dark theme colors
        self.colors = {
            'bg': '#1e293b',      # Slate 800
            'fg': '#f8fafc',      # Slate 50
            'accent': '#38bdf8',  # Sky 400
            'success': '#22c55e', # Green 500
            'danger': '#ef4444',  # Red 500
            'button': '#334155',  # Slate 700
            'button_text': '#ffffff'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        self.is_moving = False
        self.move_thread = None
        
        # Initialize mouse control
        self.init_mouse()
        
        # Log version
        self.log("Mouse Jiggler v1.0 Started")
        
        # Setup UI
        self.setup_ui()
        
        # Check permissions
        self.check_permissions()

    def init_mouse(self):
        self.mouse = None
        if PYAUTOGUI_AVAILABLE:
            self.mouse = pyautogui
            pyautogui.FAILSAFE = False
            self.log("Initialized PyAutoGUI")
        elif platform.system() == 'Darwin':
            self.log("PyAutoGUI not found, using macOS fallback")
        else:
            self.log("Error: No mouse control available")

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_msg = f"[{timestamp}] {message}"
        print(full_msg)
        if hasattr(self, 'log_area'):
            self.log_area.configure(state='normal')
            self.log_area.insert(tk.END, full_msg + "\n")
            self.log_area.see(tk.END)
            self.log_area.configure(state='disabled')

    def check_permissions(self):
        if platform.system() == 'Darwin':
            try:
                subprocess.run([
                    'osascript', '-e',
                    'tell application "System Events" to get mouse position'
                ], capture_output=True, timeout=1)
            except Exception as e:
                self.log(f"Permission check warning: {e}")

    def setup_ui(self):
        # Main Container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'], padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Mouse Jiggler", 
            font=("Helvetica", 24, "bold"),
            bg=self.colors['bg'], 
            fg=self.colors['fg']
        )
        title_label.pack(pady=(0, 10))
        
        # Status
        self.status_label = tk.Label(
            main_frame,
            text="Inactive",
            font=("Helvetica", 16),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.status_label.pack(pady=(0, 20))
        
        # Controls Frame
        controls_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        controls_frame.pack(fill=tk.X, pady=10)
        
        # Start Button - Canvas-based for color support on macOS
        start_frame = tk.Frame(controls_frame, bg=self.colors['bg'])
        start_frame.pack(side=tk.LEFT, padx=10, expand=True)
        
        self.start_canvas = tk.Canvas(start_frame, width=150, height=60, bg=self.colors['bg'], highlightthickness=0)
        self.start_canvas.pack()
        
        # Draw green button
        self.start_rect = self.start_canvas.create_rectangle(
            5, 5, 145, 55, 
            fill='#22c55e', 
            outline='#16a34a', 
            width=2
        )
        self.start_text = self.start_canvas.create_text(
            75, 30, 
            text="START", 
            fill='white', 
            font=("Helvetica", 16, "bold")
        )
        self.start_canvas.bind("<Button-1>", lambda e: self.start_moving())
        self.start_canvas.bind("<Enter>", lambda e: self.start_canvas.itemconfig(self.start_rect, fill='#16a34a'))
        self.start_canvas.bind("<Leave>", lambda e: self.start_canvas.itemconfig(self.start_rect, fill='#22c55e'))
        self.start_canvas.config(cursor="hand2")
        
        # Stop Button - Canvas-based for color support on macOS
        stop_frame = tk.Frame(controls_frame, bg=self.colors['bg'])
        stop_frame.pack(side=tk.LEFT, padx=10, expand=True)
        
        self.stop_canvas = tk.Canvas(stop_frame, width=150, height=60, bg=self.colors['bg'], highlightthickness=0)
        self.stop_canvas.pack()
        
        # Draw red button
        self.stop_rect = self.stop_canvas.create_rectangle(
            5, 5, 145, 55, 
            fill='#ef4444', 
            outline='#dc2626', 
            width=2
        )
        self.stop_text = self.stop_canvas.create_text(
            75, 30, 
            text="STOP", 
            fill='white', 
            font=("Helvetica", 16, "bold")
        )
        self.stop_canvas.bind("<Button-1>", lambda e: self.stop_moving())
        self.stop_canvas.bind("<Enter>", lambda e: self.stop_canvas.itemconfig(self.stop_rect, fill='#dc2626'))
        self.stop_canvas.bind("<Leave>", lambda e: self.stop_canvas.itemconfig(self.stop_rect, fill='#ef4444'))
        self.stop_canvas.config(cursor="hand2")
        
        # Initially disable stop button
        self.stop_canvas.itemconfig(self.stop_rect, fill='#4b5563', outline='#374151')
        self.stop_canvas.itemconfig(self.stop_text, fill='#9ca3af')
        self.stop_canvas.unbind("<Button-1>")
        self.stop_canvas.config(cursor="arrow")
        
        # Settings
        settings_frame = tk.LabelFrame(
            main_frame, 
            text="Settings", 
            bg=self.colors['bg'], 
            fg=self.colors['fg'],
            font=("Helvetica", 12)
        )
        settings_frame.pack(fill=tk.X, pady=20, padx=5)
        
        # Interval
        tk.Label(settings_frame, text="Interval (sec):", bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W, padx=10, pady=(10, 0))
        self.interval_var = tk.StringVar(value="2")
        tk.Spinbox(settings_frame, from_=1, to=60, textvariable=self.interval_var, width=10).pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        # Range
        tk.Label(settings_frame, text="Range (pixels):", bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W, padx=10)
        self.range_var = tk.StringVar(value="50")
        tk.Spinbox(settings_frame, from_=10, to=500, textvariable=self.range_var, width=10).pack(anchor=tk.W, padx=10, pady=(0, 10))

        # Test Button
        tk.Button(
            settings_frame,
            text="Test Single Move",
            command=self.test_move,
            bg=self.colors['accent'],
            fg='black'
        ).pack(pady=10)

        # Log Area
        log_frame = tk.LabelFrame(
            main_frame,
            text="Activity Log",
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_area = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            bg='#0f172a',
            fg='#94a3b8',
            font=("Menlo", 10),
            state='disabled'
        )
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def start_moving(self):
        if self.is_moving:
            return
            
        self.is_moving = True
        
        # Disable start button (gray it out)
        self.start_canvas.itemconfig(self.start_rect, fill='#4b5563', outline='#374151')
        self.start_canvas.itemconfig(self.start_text, fill='#9ca3af')
        self.start_canvas.unbind("<Button-1>")
        self.start_canvas.unbind("<Enter>")
        self.start_canvas.unbind("<Leave>")
        self.start_canvas.config(cursor="arrow")
        
        # Enable stop button (make it red)
        self.stop_canvas.itemconfig(self.stop_rect, fill='#ef4444', outline='#dc2626')
        self.stop_canvas.itemconfig(self.stop_text, fill='white')
        self.stop_canvas.bind("<Button-1>", lambda e: self.stop_moving())
        self.stop_canvas.bind("<Enter>", lambda e: self.stop_canvas.itemconfig(self.stop_rect, fill='#dc2626'))
        self.stop_canvas.bind("<Leave>", lambda e: self.stop_canvas.itemconfig(self.stop_rect, fill='#ef4444'))
        self.stop_canvas.config(cursor="hand2")
        
        self.status_label.config(text="Active - Moving", fg=self.colors['success'])
        self.log("Started movement loop")
        
        self.move_thread = threading.Thread(target=self.move_loop, daemon=True)
        self.move_thread.start()

    def stop_moving(self):
        self.is_moving = False
        
        # Enable start button (make it green)
        self.start_canvas.itemconfig(self.start_rect, fill='#22c55e', outline='#16a34a')
        self.start_canvas.itemconfig(self.start_text, fill='white')
        self.start_canvas.bind("<Button-1>", lambda e: self.start_moving())
        self.start_canvas.bind("<Enter>", lambda e: self.start_canvas.itemconfig(self.start_rect, fill='#16a34a'))
        self.start_canvas.bind("<Leave>", lambda e: self.start_canvas.itemconfig(self.start_rect, fill='#22c55e'))
        self.start_canvas.config(cursor="hand2")
        
        # Disable stop button (gray it out)
        self.stop_canvas.itemconfig(self.stop_rect, fill='#4b5563', outline='#374151')
        self.stop_canvas.itemconfig(self.stop_text, fill='#9ca3af')
        self.stop_canvas.unbind("<Button-1>")
        self.stop_canvas.unbind("<Enter>")
        self.stop_canvas.unbind("<Leave>")
        self.stop_canvas.config(cursor="arrow")
        
        self.status_label.config(text="Inactive", fg=self.colors['fg'])
        self.log("Stopped movement")

    def test_move(self):
        self.log("Testing single move...")
        try:
            if self.mouse:
                x, y = self.mouse.position()
                self.mouse.moveTo(x + 10, y + 10)
                self.log(f"Moved from ({x},{y}) to ({x+10},{y+10})")
            else:
                self.log("Error: Mouse control not initialized")
        except Exception as e:
            self.log(f"Test failed: {e}")

    def move_loop(self):
        while self.is_moving:
            try:
                interval = float(self.interval_var.get())
                dist = int(self.range_var.get())
                
                if self.mouse:
                    current_x, current_y = self.mouse.position()
                    dx = random.randint(-dist, dist)
                    dy = random.randint(-dist, dist)
                    
                    # Simple bounds check
                    try:
                        w, h = self.mouse.size()
                    except:
                        w, h = 1920, 1080
                        
                    new_x = max(0, min(current_x + dx, w))
                    new_y = max(0, min(current_y + dy, h))
                    
                    # Try to move
                    self.mouse.moveTo(new_x, new_y, duration=0.2)
                    
                    # VERIFICATION: Check if it actually moved
                    time.sleep(0.1)
                    check_x, check_y = self.mouse.position()
                    
                    # Allow for small pixel differences
                    if abs(check_x - new_x) > 5 or abs(check_y - new_y) > 5:
                        self.root.after(0, lambda: self.log("Warning: Cursor didn't move! Trying fallback..."))
                        self.fallback_move(new_x, new_y)
                    else:
                        self.root.after(0, lambda msg=f"Moved to ({new_x}, {new_y})": self.log(msg))
                else:
                    self.root.after(0, lambda: self.log("Error: No mouse control"))
                
                time.sleep(interval)
                
            except Exception as e:
                self.root.after(0, lambda msg=f"Error: {e}": self.log(msg))
                time.sleep(2)

    def fallback_move(self, x, y):
        """Fallback to Quartz (CoreGraphics) if pyautogui fails"""
        if QUARTZ_AVAILABLE:
            try:
                # Create an event source
                source = Quartz.CGEventSourceCreate(Quartz.kCGEventSourceStateHIDSystemState)
                
                move_event = Quartz.CGEventCreateMouseEvent(
                    source, 
                    Quartz.kCGEventMouseMoved, 
                    (x, y), 
                    Quartz.kCGMouseButtonLeft
                )
                Quartz.CGEventPost(Quartz.kCGHIDEventTap, move_event)
                
                # VERIFY FALLBACK
                time.sleep(0.1)
                check_x, check_y = self.mouse.position()
                
                if abs(check_x - x) > 5 or abs(check_y - y) > 5:
                    self.root.after(0, lambda: self.log(f"CRITICAL: Fallback also failed. OS is blocking control."))
                    self.root.after(0, lambda: messagebox.showerror(
                        "Permission Blocked", 
                        "macOS is blocking mouse control.\n\n"
                        "Even the backup method failed.\n"
                        "Please remove 'Mouse Mover Pro Max' from Accessibility settings and re-add it."
                    ))
                else:
                    self.root.after(0, lambda: self.log(f"Fallback (Quartz) moved to ({x}, {y})"))
                    
            except Exception as e:
                self.root.after(0, lambda msg=f"Quartz fallback failed: {e}": self.log(msg))
        else:
             self.root.after(0, lambda: self.log("Error: Quartz not available for fallback"))

def main():
    root = tk.Tk()
    app = MouseMoverApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
