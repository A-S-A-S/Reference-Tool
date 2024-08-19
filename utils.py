import tkinter as tk
from tkinter import filedialog

def get_directory():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory()
    return directory