import customtkinter as ctk
from typing import Optional
from image_viewer import ImageViewer
from image_downloader import ImageDownloader
from utils import get_directory

class MainApp(ctk.CTk):
    PADDING = 20
    BUTTON_PADDING = 10
    TITLE_FONT_SIZE = 20

    def __init__(self):
        super().__init__()
        self.title("Image Reference Tool")
        self.geometry("1000x700")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.setup_sidebar()
        self.setup_content_frame()

        self.current_view: Optional[ctk.CTkFrame] = None
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

        ctk.CTkLabel(
            self.sidebar, 
            text="Image Reference Tool", 
            font=ctk.CTkFont(size=self.TITLE_FONT_SIZE, weight="bold")
        ).grid(row=0, column=0, padx=self.PADDING, pady=(self.PADDING, self.BUTTON_PADDING))

        ctk.CTkButton(
            self.sidebar, 
            text="Image Viewer", 
            command=self.show_viewer
        ).grid(row=1, column=0, padx=self.PADDING, pady=self.BUTTON_PADDING)

        ctk.CTkButton(
            self.sidebar, 
            text="Image Downloader", 
            command=self.show_downloader
        ).grid(row=2, column=0, padx=self.PADDING, pady=self.BUTTON_PADDING)

    def setup_content_frame(self):
        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

    def on_closing(self):
        print("Application is closing...")
        self.cleanup()
        self.destroy()

    def cleanup(self):
        if isinstance(self.current_view, ImageViewer):
            self.current_view.cancel_scheduled_tasks()
        # Cancel any other scheduled tasks in MainApp
        for task in self.tk.call('after', 'info'):
            self.after_cancel(task)

    def show_viewer(self):
        if isinstance(self.current_view, ImageDownloader):
            self.current_view.grid_forget()
        if isinstance(self.current_view, ImageViewer):
            self.current_view.cancel_scheduled_tasks()
        directory = get_directory()
        self.current_view = ImageViewer(self.content_frame, directory)
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def show_downloader(self):
        if isinstance(self.current_view, ImageViewer):
            self.current_view.cancel_scheduled_tasks()
            self.current_view.grid_forget()
        self.current_view = ImageDownloader(self.content_frame)
        self.current_view.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    try:
        app = MainApp()
        app.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")