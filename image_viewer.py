import os
import random
from PIL import Image
import customtkinter as ctk

class ImageViewer(ctk.CTkFrame):
    def __init__(self, parent, directory):
        super().__init__(parent)
        self.directory = directory
        self.image_files = self.get_image_files(directory)
        self.index = 0
        self.timer_id = None
        self.delay = 3000 
        self.is_paused = False
        self.current_image = None

        if not self.image_files:
            print("No images found in the directory.")
            return

        random.shuffle(self.image_files)
        self.setup_ui()

    def setup_ui(self):
        self.grid_rowconfigure(0, weight=1)  # Image label row
        self.grid_rowconfigure(1, weight=0)  # Controls row
        self.grid_columnconfigure(0, weight=1)  # Main column

        # Image Label
        self.img_label = ctk.CTkLabel(self, text="")
        self.img_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 0))

        # Controls Frame
        controls_frame = ctk.CTkFrame(self)
        controls_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        controls_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Buttons in Controls Frame
        ctk.CTkButton(controls_frame, text="Previous", command=self.prev_image).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.play_pause_button = ctk.CTkButton(controls_frame, text="Pause", command=self.toggle_pause)
        self.play_pause_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(controls_frame, text="Next", command=self.next_image).grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # Delay Frame
        delay_frame = ctk.CTkFrame(controls_frame)
        delay_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(delay_frame, text="Delay (ms):").pack(side="left", padx=5)
        self.delay_entry = ctk.CTkEntry(delay_frame)
        self.delay_entry.pack(side="left", padx=10, expand=True, fill="x")
        self.delay_entry.insert(0, str(self.delay))
        ctk.CTkButton(delay_frame, text="Set Delay", command=self.set_delay).pack(side="left", padx=10)

        # Bind resize event
        self.bind("<Configure>", self.on_resize)
        self.show_image()

    def get_image_files(self, directory):
        supported_formats = ('.png', '.jpg', '.jpeg', '.gif')
        return [f for f in os.listdir(directory) if f.lower().endswith(supported_formats)]

    def show_image(self):
        if 0 <= self.index < len(self.image_files):
            image_path = os.path.join(self.directory, self.image_files[self.index])
            self.current_image = Image.open(image_path)
            self.update_image()

            if not self.is_paused:
                self.timer_id = self.after(self.delay, self.next_image)

    def update_image(self):
        if self.current_image:
            width = self.img_label.winfo_width()
            height = self.img_label.winfo_height()
            
            img_copy = self.current_image.copy()
            img_copy.thumbnail((width, height))
            
            ctk_image = ctk.CTkImage(light_image=img_copy, dark_image=img_copy, size=img_copy.size)
            self.img_label.configure(image=ctk_image)
            self.img_label.image = ctk_image

    def on_resize(self, event):
        if event.widget == self:
            self.after_cancel(self.timer_id)
            self.update_image()
            if not self.is_paused:
                self.timer_id = self.after(self.delay, self.next_image)

    def next_image(self):
        self.index = (self.index + 1) % len(self.image_files)
        self.show_image()

    def prev_image(self):
        self.index = (self.index - 1) % len(self.image_files)
        self.show_image()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.play_pause_button.configure(text="Play")
            if self.timer_id:
                self.after_cancel(self.timer_id)
        else:
            self.play_pause_button.configure(text="Pause")
            self.show_image()

    def set_delay(self):
        try:
            new_delay = int(self.delay_entry.get())
            if new_delay > 0:
                self.delay = new_delay
                if not self.is_paused:
                    if self.timer_id:
                        self.after_cancel(self.timer_id)
                    self.show_image()
            else:
                raise ValueError("Delay must be positive")
        except ValueError:
            print("Invalid delay value. Please enter a positive integer.")
