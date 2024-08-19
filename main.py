import customtkinter as ctk
from image_viewer import ImageViewer
from image_downloader import ImageDownloader
from utils import get_directory

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Image Reference Tool")
        self.geometry("1000x700")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar for navigation
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="Image Reference Tool", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.viewer_button = ctk.CTkButton(self.sidebar, text="Image Viewer", command=self.show_viewer)
        self.viewer_button.grid(row=1, column=0, padx=20, pady=10)

        self.downloader_button = ctk.CTkButton(self.sidebar, text="Image Downloader", command=self.show_downloader)
        self.downloader_button.grid(row=2, column=0, padx=20, pady=10)

        # Main content area
        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.current_view = None

        # Bind the close button event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # Perform any cleanup tasks here
        print("Application is closing...")
        self.destroy()

    def show_viewer(self):
        if isinstance(self.current_view, ImageDownloader):
            self.current_view.grid_forget()
        directory = get_directory()
        self.current_view = ImageViewer(self.content_frame, directory)
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def show_downloader(self):
        if isinstance(self.current_view, ImageViewer):
            self.current_view.grid_forget()
        self.current_view = ImageDownloader(self.content_frame)
        self.current_view.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
