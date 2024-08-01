import tkinter as tk
from gui import NERApp
from utils import ensure_directories

if __name__ == "__main__":
    ensure_directories()
    root = tk.Tk()
    app = NERApp(root)
    root.mainloop()