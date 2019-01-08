import tkinter as tk
from src.views import mainWindow

if __name__ == "__main__":
    __root = tk.Tk()

    mainWindow.MainWindow(__root)
    __root.mainloop()
