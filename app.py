import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("400x380")
        self.title("ICON1K")

if __name__ == "__main__":
    app = App()
    app.mainloop()