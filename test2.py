import os
import random
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

class ImageViewer:
    def __init__(self, root, directory):
        self.root = root
        self.directory = directory
        self.image_files = self.get_image_files(directory)
        self.index = 0
        self.timer_id = None
        self.delay = 3000
        self.is_paused = False

        # Dark theme colors
        self.bg_color = "#2b2b2b"
        self.fg_color = "#ffffff"
        self.button_bg = "#3c3f41"
        self.button_fg = "#ffffff"
        self.entry_bg = "#3c3f41"
        self.entry_fg = "#ffffff"

        if not self.image_files:
            print("No images found in the directory.")
            self.root.quit()
            return

        random.shuffle(self.image_files)
        
        self.setup_ui()

    def setup_ui(self):
        # Configure root window
        self.root.title("Get Reference")
        self.root.configure(bg=self.bg_color)

        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=self.bg_color)
        style.configure('TButton', background=self.button_bg, foreground=self.button_fg)
        style.configure('TLabel', background=self.bg_color, foreground=self.fg_color)
        style.configure('TEntry', fieldbackground=self.entry_bg, foreground=self.entry_fg)

        # Main widget
        self.img_label = tk.Label(self.root, bg=self.bg_color)
        self.img_label.pack(pady=10)
        
        # Controls
        controls_frame = ttk.Frame(self.root)
        controls_frame.pack(pady=10)

        ttk.Button(controls_frame, text="Previous", command=self.prev_image).grid(row=0, column=0, padx=5)
        ttk.Button(controls_frame, text="Next", command=self.next_image).grid(row=0, column=2, padx=5)

        self.play_pause_button = ttk.Button(controls_frame, text="Pause", command=self.toggle_pause)
        self.play_pause_button.grid(row=0, column=1, padx=5)
        
        ttk.Label(controls_frame, text="Delay (ms):").grid(row=1, column=0, pady=10)
        self.delay_entry = ttk.Entry(controls_frame, width=10)
        self.delay_entry.insert(0, str(self.delay))
        self.delay_entry.grid(row=1, column=1)
        ttk.Button(controls_frame, text="Set Delay", command=self.set_delay).grid(row=1, column=2)

        self.show_image()

    def get_image_files(self, directory):
        supported_formats = ('.png', '.jpg', '.jpeg', '.gif')
        return [f for f in os.listdir(directory) if f.lower().endswith(supported_formats)]

    def show_image(self):
        if 0 <= self.index < len(self.image_files):
            image_path = os.path.join(self.directory, self.image_files[self.index])
            img = Image.open(image_path)
            img.thumbnail((800, 600))
            photo = ImageTk.PhotoImage(img)
            self.img_label.config(image=photo)
            self.img_label.image = photo

            if not self.is_paused:
                self.timer_id = self.root.after(self.delay, self.next_image)

    def next_image(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.index = (self.index + 1) % len(self.image_files)
        self.show_image()

    def prev_image(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.index = (self.index - 1) % len(self.image_files)
        self.show_image()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.play_pause_button.config(text="Play")
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
        else:
            self.play_pause_button.config(text="Pause")
            self.show_image()

    def set_delay(self):
        try:
            new_delay = int(self.delay_entry.get())
            if new_delay > 0:
                self.delay = new_delay
                if not self.is_paused:
                    if self.timer_id:
                        self.root.after_cancel(self.timer_id)
                    self.show_image()
            else:
                raise ValueError("Delay must be positive")
        except ValueError:
            print("Invalid delay value. Please enter a positive integer.")

if __name__ == "__main__":
    directory = input("Enter the directory path with images: ") or r"C:\Users\Se\Stuff\Projects\GetReference\pntrst"
    root = tk.Tk()
    app = ImageViewer(root, directory)
    root.mainloop()