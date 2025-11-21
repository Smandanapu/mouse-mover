
import tkinter as tk
from tkinter import ttk
import threading
import time
import random

try:
    import pyautogui
except ImportError:
    print("pyautogui not installed. Using macOS-native mouse control.")
    pyautogui = None

import subprocess
import platform

class MacOSMouseControl:
    """Fallback mouse control using macOS native methods when pyautogui is unavailable"""
    
    @staticmethod
    def position():
        """Get current mouse position using AppleScript"""
        try:
            script = '''
            tell application "System Events"
                set mousePos to (do shell script "echo $((`system_profiler SPDisplaysDataType | grep Resolution | head -1 | awk '{print $2}'` / 2)), $((`system_profiler SPDisplaysDataType | grep Resolution | head -1 | awk '{print $4}'` / 2))")
                return mousePos
            end tell
            '''
            # Simplified approach - get mouse position via CGEvent
            result = subprocess.run([
                'osascript', '-e',
                'tell application "System Events" to set mousePosition to (mouse position as list)'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                pos_str = result.stdout.strip()
                # Parse "x, y" format
                x, y = pos_str.split(', ')
                return (int(float(x)), int(float(y)))
            else:
                return (500, 500)  # Default fallback position
        except:
            return (500, 500)  # Default fallback position
    
    @staticmethod
    def moveTo(x, y, duration=0.1):
        """Move mouse to position using AppleScript"""
        try:
            # Use AppleScript to move mouse
            script = f'''
            tell application "System Events"
                set mouseLoc to {{{x}, {y}}}
                click at mouseLoc
            end tell
            '''
            # Use a simpler approach with cliclick if available, otherwise AppleScript
            try:
                subprocess.run(['cliclick', f'm:{x},{y}'], check=True, timeout=1)
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Fallback to AppleScript
                subprocess.run(['osascript', '-e', f'tell application "System Events" to set mouse position to {{{x}, {y}}}'], timeout=1)
        except Exception as e:
            print(f"Error moving mouse: {e}")
    
    @staticmethod
    def size():
        """Get screen size"""
        try:
            result = subprocess.run([
                'osascript', '-e',
                'tell application "Finder" to get bounds of window of desktop'
            ], capture_output=True, text=True, timeout=2)
            
            if result.returncode == 0:
                bounds = result.stdout.strip().split(', ')
                width = int(bounds[2]) - int(bounds[0])
                height = int(bounds[3]) - int(bounds[1])
                return (width, height)
            else:
                return (1920, 1080)  # Default fallback
        except:
            return (1920, 1080)  # Default fallback

class RoundedButton(tk.Canvas):
    def __init__(self, parent, width, height, corner_radius, padding=0, color="#000000", text_color="#ffffff", border_color=None, border_width=0, text="", command=None):
        tk.Canvas.__init__(self, parent, borderwidth=0, relief="flat", highlightthickness=0, bg=parent["bg"])
        self.command = command
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.padding = padding
        self.color = color
        self.original_color = color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.text = text
        self.state = "normal"

        # Resize canvas
        self.configure(width=width, height=height)

        # Bind events
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)

        self._draw()

    def _draw(self):
        self.delete("all")
        
        # Determine colors based on state
        if self.state == "disabled":
            fill_color = "#334155" # Slate 700
            text_color = "#64748b" # Slate 500
            border_c = "#475569"   # Slate 600
        else:
            fill_color = self.color
            text_color = self.text_color
            border_c = self.border_color if self.border_color else fill_color

        # Draw border if needed (by drawing a larger rect behind)
        if self.border_width > 0:
             self._draw_rounded_rect(2, 2, self.width-2, self.height-2, self.corner_radius, border_c)
             # Inner rect
             offset = 2 + self.border_width
             self._draw_rounded_rect(offset, offset, self.width-offset, self.height-offset, self.corner_radius - self.border_width, fill_color)
        else:
             self._draw_rounded_rect(2, 2, self.width-2, self.height-2, self.corner_radius, fill_color)
        
        # Draw text
        self.create_text(self.width/2, self.height/2, text=self.text, fill=text_color, font=("Helvetica", 16, "bold"))

    def _draw_rounded_rect(self, x1, y1, x2, y2, radius, color):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, fill=color)

    def _on_press(self, event):
        if self.state != "disabled":
            self.configure(relief="sunken")
            if self.command:
                self.command()

    def _on_release(self, event):
        if self.state != "disabled":
            self.configure(relief="flat")

    def _on_hover(self, event):
        if self.state != "disabled":
            # Brighten color
            self.color = self._adjust_color(self.original_color, 20)
            self._draw()

    def _on_leave(self, event):
        if self.state != "disabled":
            self.color = self.original_color
            self._draw()

    def _adjust_color(self, hex_color, factor):
        # Simple color adjustment
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        
        r = min(255, r + factor)
        g = min(255, g + factor)
        b = min(255, b + factor)
        
        return f"#{r:02x}{g:02x}{b:02x}"

    def set_state(self, state):
        self.state = state
        self._draw()
        
    def set_color(self, color):
        self.color = color
        self.original_color = color
        self._draw()


class MouseMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Mover Pro")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        
        # Set modern professional color scheme (Deep Slate Theme)
        self.colors = {
            'bg_gradient_start': '#0f172a', # Slate 900
            'bg_gradient_end': '#1e293b',   # Slate 800
            'accent_primary': '#38bdf8',    # Sky 400
            'accent_secondary': '#7dd3fc',  # Sky 300
            'text_primary': '#f8fafc',      # Slate 50
            'text_secondary': '#94a3b8',    # Slate 400
            'success': '#10b981',           # Emerald 500
            'danger': '#ef4444',            # Red 500
            'card_bg': '#1e293b',           # Slate 800
            'card_border': '#334155'        # Slate 700
        }
        
        # Configure root background
        self.root.configure(bg=self.colors['bg_gradient_start'])
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        self.is_moving = False
        self.move_thread = None
        
        # Initialize mouse control
        if pyautogui:
            self.mouse = pyautogui
            # Disable pyautogui failsafe for smoother operation
            pyautogui.FAILSAFE = False
        elif platform.system() == 'Darwin':  # macOS
            self.mouse = MacOSMouseControl()
        else:
            self.mouse = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container with gradient background
        main_frame = tk.Frame(self.root, bg=self.colors['bg_gradient_start'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Header section with icon and title
        header_frame = tk.Frame(main_frame, bg=self.colors['bg_gradient_start'], height=140)
        header_frame.pack(fill=tk.X, padx=30, pady=(30, 20))
        
        # Load and display icon
        try:
            icon_path = "/Users/satmac/.gemini/antigravity/brain/2e0f67ce-93b1-4b7c-88ac-47ec2a5a440a/mouse_mover_icon_1763747272841.png"
            from PIL import Image, ImageTk
            icon_image = Image.open(icon_path)
            icon_image = icon_image.resize((80, 80), Image.Resampling.LANCZOS)
            self.icon_photo = ImageTk.PhotoImage(icon_image)
            icon_label = tk.Label(header_frame, image=self.icon_photo, bg=self.colors['bg_gradient_start'])
            icon_label.pack(pady=(0, 15))
        except Exception as e:
            print(f"Could not load icon: {e}")
            # Fallback: Create a styled text icon
            icon_label = tk.Label(
                header_frame, 
                text="🖱️", 
                font=("SF Pro Display", 48),
                bg=self.colors['bg_gradient_start'],
                fg=self.colors['text_secondary']
            )
            icon_label.pack(pady=(0, 15))
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="Mouse Mover Pro",
            font=("SF Pro Display", 28, "bold"),
            bg=self.colors['bg_gradient_start'],
            fg=self.colors['text_primary']
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Automated Cursor Movement",
            font=("SF Pro Text", 12),
            bg=self.colors['bg_gradient_start'],
            fg=self.colors['text_secondary']
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Status card
        status_card = tk.Frame(
            main_frame,
            bg=self.colors['card_bg'],
            highlightbackground=self.colors['card_border'],
            highlightthickness=2
        )
        status_card.pack(fill=tk.X, padx=30, pady=(0, 20))
        
        status_inner = tk.Frame(status_card, bg=self.colors['card_bg'])
        status_inner.pack(fill=tk.X, padx=20, pady=15)
        
        status_title = tk.Label(
            status_inner,
            text="STATUS",
            font=("SF Pro Text", 10, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['text_secondary']
        )
        status_title.pack(anchor=tk.W)
        
        self.status_label = tk.Label(
            status_inner,
            text="● Inactive",
            font=("SF Pro Display", 16, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['text_secondary']
        )
        self.status_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Control buttons frame - centered layout
        buttons_frame = tk.Frame(main_frame, bg=self.colors['bg_gradient_start'])
        buttons_frame.pack(fill=tk.X, padx=30, pady=(0, 25))
        
        # Create a container for centered buttons
        button_container = tk.Frame(buttons_frame, bg=self.colors['bg_gradient_start'])
        button_container.pack()
        
        # Start button (Custom Rounded)
        start_frame = tk.Frame(button_container, bg=self.colors['bg_gradient_start'])
        start_frame.pack(side=tk.LEFT, padx=15)
        
        self.start_button = RoundedButton(
            start_frame,
            width=160,
            height=60,
            corner_radius=30,
            color=self.colors['success'],
            text="START",
            command=self.start_moving,
            border_color="#059669", # Emerald 600
            border_width=2
        )
        self.start_button.pack()
        
        # Stop button (Custom Rounded)
        stop_frame = tk.Frame(button_container, bg=self.colors['bg_gradient_start'])
        stop_frame.pack(side=tk.LEFT, padx=15)
        
        self.stop_button = RoundedButton(
            stop_frame,
            width=160,
            height=60,
            corner_radius=30,
            color=self.colors['danger'],
            text="STOP",
            command=self.stop_moving,
            border_color="#dc2626", # Red 600
            border_width=2
        )
        self.stop_button.set_state("disabled")
        self.stop_button.pack()
        
        # Settings card
        settings_card = tk.Frame(
            main_frame,
            bg=self.colors['card_bg'],
            highlightbackground=self.colors['card_border'],
            highlightthickness=2
        )
        settings_card.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))
        
        settings_inner = tk.Frame(settings_card, bg=self.colors['card_bg'])
        settings_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        settings_title = tk.Label(
            settings_inner,
            text="SETTINGS",
            font=("SF Pro Text", 10, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['text_secondary']
        )
        settings_title.pack(anchor=tk.W, pady=(0, 15))
        
        # Interval setting
        interval_frame = tk.Frame(settings_inner, bg=self.colors['card_bg'])
        interval_frame.pack(fill=tk.X, pady=(0, 20))
        
        interval_label = tk.Label(
            interval_frame,
            text="Movement Interval",
            font=("SF Pro Text", 13),
            bg=self.colors['card_bg'],
            fg=self.colors['text_primary']
        )
        interval_label.pack(anchor=tk.W)
        
        interval_desc = tk.Label(
            interval_frame,
            text="Time between movements (seconds)",
            font=("SF Pro Text", 10),
            bg=self.colors['card_bg'],
            fg=self.colors['text_secondary']
        )
        interval_desc.pack(anchor=tk.W, pady=(2, 8))
        
        self.interval_var = tk.StringVar(value="2")
        interval_spinbox = tk.Spinbox(
            interval_frame,
            from_=1,
            to=10,
            textvariable=self.interval_var,
            font=("SF Pro Text", 14),
            bg=self.colors['bg_gradient_start'],
            fg=self.colors['text_primary'],
            buttonbackground=self.colors['accent_secondary'],
            relief=tk.FLAT,
            width=15,
            insertbackground=self.colors['text_primary']
        )
        interval_spinbox.pack(anchor=tk.W, ipady=8)
        
        # Range setting
        range_frame = tk.Frame(settings_inner, bg=self.colors['card_bg'])
        range_frame.pack(fill=tk.X)
        
        range_label = tk.Label(
            range_frame,
            text="Movement Range",
            font=("SF Pro Text", 13),
            bg=self.colors['card_bg'],
            fg=self.colors['text_primary']
        )
        range_label.pack(anchor=tk.W)
        
        range_desc = tk.Label(
            range_frame,
            text="Maximum distance to move cursor (pixels)",
            font=("SF Pro Text", 10),
            bg=self.colors['card_bg'],
            fg=self.colors['text_secondary']
        )
        range_desc.pack(anchor=tk.W, pady=(2, 8))
        
        self.range_var = tk.StringVar(value="50")
        range_spinbox = tk.Spinbox(
            range_frame,
            from_=10,
            to=200,
            textvariable=self.range_var,
            font=("SF Pro Text", 14),
            bg=self.colors['bg_gradient_start'],
            fg=self.colors['text_primary'],
            buttonbackground=self.colors['accent_secondary'],
            relief=tk.FLAT,
            width=15,
            insertbackground=self.colors['text_primary']
        )
        range_spinbox.pack(anchor=tk.W, ipady=8)
    
    def start_moving(self):
        if not self.mouse:
            self.status_label.config(
                text="● Error: Not Available",
                fg=self.colors['danger']
            )
            return
        
        # Immediate UI feedback
        self.start_button.set_state("disabled")
        self.stop_button.set_state("normal")
        self.status_label.config(
            text="● Starting...",
            fg='#fbbf24' # Amber 400
        )
        self.root.update()  # Force immediate UI update
        
        self.is_moving = True
        
        # Start movement in a separate thread
        self.move_thread = threading.Thread(target=self.move_mouse_loop, daemon=True)
        self.move_thread.start()
        
        # Update status after thread starts
        self.root.after(100, lambda: self.status_label.config(
            text="● Active - Moving Cursor",
            fg=self.colors['success']
        ))
    
    def stop_moving(self):
        # Immediate UI feedback
        self.stop_button.set_state("disabled")
        self.status_label.config(
            text="● Stopping...",
            fg='#fbbf24' # Amber 400
        )
        self.root.update()  # Force immediate UI update
        
        self.is_moving = False
        
        # Restore UI after stopping
        self.root.after(200, lambda: (
            self.start_button.set_state("normal"),
            self.status_label.config(
                text="● Inactive",
                fg=self.colors['text_secondary']
            )
        ))
    
    def move_mouse_loop(self):
        try:
            interval = float(self.interval_var.get())
            movement_range = int(self.range_var.get())
        except ValueError:
            interval = 2.0
            movement_range = 50
        
        while self.is_moving:
            try:
                # Get current mouse position
                current_x, current_y = self.mouse.position()
                
                # Generate random movement within range
                dx = random.randint(-movement_range, movement_range)
                dy = random.randint(-movement_range, movement_range)
                
                new_x = current_x + dx
                new_y = current_y + dy
                
                # Ensure new position is within screen bounds
                screen_width, screen_height = self.mouse.size()
                new_x = max(0, min(new_x, screen_width - 1))
                new_y = max(0, min(new_y, screen_height - 1))
                
                # Move mouse smoothly with shorter duration
                self.mouse.moveTo(new_x, new_y, duration=0.1)
                
                # Wait for the specified interval with responsive checking
                start_time = time.time()
                while time.time() - start_time < interval and self.is_moving:
                    time.sleep(0.1)  # Check every 100ms for stop signal
                
            except Exception as e:
                print(f"Error moving mouse: {e}")
                break
    
    def on_closing(self):
        self.stop_moving()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = MouseMoverApp(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
