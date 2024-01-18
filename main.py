from tkinter import messagebox
import customtkinter as ctk

from main_menu import *


class MyApp:
    def __init__(self, master):
        # App settings
        self.master = master
        self.master.title("Work with PDF")
        self.master.geometry("800x600")

        # Bind
        self.master.bind("<Escape>", self.confirm_exit)

        # Frames
        self.main_menu_view = main_menu_view
        self.main_menu_view(master=self.master)

    def confirm_exit(self, event):
        result = messagebox.askquestion("Potwierdzenie", "Czy na pewno chcesz wyjść?")
        if result == "yes":
            self.master.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    app = MyApp(root)
    root.mainloop()
