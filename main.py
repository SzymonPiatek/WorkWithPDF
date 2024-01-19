import os
from tkinter import messagebox
from tkinter import filedialog
import tkinter as tk
import customtkinter as ctk
from pypdf import PdfMerger


class MyApp:
    def __init__(self, master):
        # App settings
        self.master = master
        self.master.title("Work with PDF")
        self.master.geometry("800x600")

        # Bind
        self.master.bind("<Escape>", self.confirm_exit)

        # Place Frame
        self.main_menu_view()

    def confirm_exit(self, event):
        result = messagebox.askquestion("Potwierdzenie", "Czy na pewno chcesz wyjść?")
        if result == "yes":
            self.master.destroy()

    def main_menu_view(self):
        # Create Frame
        self.main_menu_frame = ctk.CTkFrame(master=self.master)

        # Create Widgets
        merge_button = ctk.CTkButton(master=self.main_menu_frame,
                                     text="Połącz pliki PDF",
                                     command=lambda: self.change_frame(old_frame=self.main_menu_frame,
                                                                       new_frame=self.pdf_merge_view))

        # Place Widgets
        merge_button.pack()

        # Place Frame
        self.main_menu_frame.pack(fill="both", expand=True)

    def change_frame(self, old_frame, new_frame):
        for widget in old_frame.winfo_children():
            widget.destroy()

        new_frame()

    def pdf_merge_view(self):
        # Variables
        self.pdf_files = []

        # Create Frame
        self.pdf_merge_frame = ctk.CTkFrame(master=self.main_menu_frame)

        # Create Widgets
        self.pdf_add_button = ctk.CTkButton(master=self.pdf_merge_frame,
                                            text="Dodaj plik PDF",
                                            command=self.pdf_add_func)
        self.pdf_remove_button = ctk.CTkButton(master=self.pdf_merge_frame,
                                               text="Usuń plik PDF",
                                               command=self.pdf_remove_func)
        self.pdf_listbox = tk.Listbox(master=self.pdf_merge_frame)
        self.pdf_merge_button = ctk.CTkButton(master=self.pdf_merge_frame,
                                              text="Połącz pliki PDF",
                                              command=self.pdf_merge_func)

        # Place Widgets
        self.pdf_add_button.place(relx=0.25, rely=0.1, anchor=ctk.CENTER, relwidth=0.2, relheight=0.1)
        self.pdf_remove_button.place(relx=0.75, rely=0.1, anchor=ctk.CENTER, relwidth=0.2, relheight=0.1)
        self.pdf_listbox.place(relx=0.5, rely=0.2, anchor=ctk.N, relwidth=0.7, relheight=0.6)
        self.pdf_merge_button.place(relx=0.5, rely=0.9, anchor=ctk.CENTER, relwidth=0.2, relheight=0.1)

        # Place Frame
        self.pdf_merge_frame.pack(fill="both", expand=True)

        # Update PDF files
        self.update_pdf_listbox()

    def update_pdf_listbox(self):
        self.pdf_listbox.delete(0, tk.END)
        i = 1
        for pdf_file in self.pdf_files:
            file_name = os.path.basename(pdf_file)
            file_name = f"{i}. {file_name}"
            self.pdf_listbox.insert(tk.END, file_name)
            i += 1

    def pdf_add_func(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pliki PDF", "*.pdf")])

        if file_path:
            self.pdf_files.append(file_path)

        self.update_pdf_listbox()

    def pdf_merge_func(self):
        merger = PdfMerger()

        for pdf in self.pdf_files:
            print(pdf)
            merger.append(pdf)

        merger.write("output.pdf")
        merger.close()

    def pdf_remove_func(self):
        selected_index = self.pdf_listbox.curselection()
        if selected_index:
            del self.pdf_files[selected_index[0]]
            self.update_pdf_listbox()


if __name__ == "__main__":
    root = ctk.CTk()
    app = MyApp(root)
    root.mainloop()
