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
        self.master.geometry("1200x800")
        self.master.resizable(False, False)

        # Colors
        self.button_color = "#6e8237"
        self.background_color = "#404040"
        self.listbox_color = "#636363"
        self.master.configure(fg_color=self.background_color)

        # Bind
        self.master.bind("<Escape>", self.confirm_exit)

        # Fonts
        self.main_font = ("Cascadia Code SemiBold", 24, "bold")
        self.list_font = ("Cascadia Code SemiBold", 16, "bold")

        # Place Frame
        self.main_menu_view()

    def confirm_exit(self, event):
        result = messagebox.askquestion("Potwierdzenie", "Czy na pewno chcesz wyjść?")
        if result == "yes":
            self.master.destroy()

    def main_menu_view(self):
        # Create Frame
        self.main_menu_frame = ctk.CTkFrame(master=self.master,
                                            fg_color="transparent")

        # Create Widgets
        self.merge_button = ctk.CTkButton(master=self.main_menu_frame,
                                          text="Połącz pliki PDF",
                                          command=lambda: self.change_frame(old_frame=self.main_menu_frame,
                                                                            new_frame=self.pdf_merge_view))

        # Configure Widgets
        self.merge_button.configure(font=self.main_font,
                                    fg_color=self.button_color)

        # Place Widgets
        self.merge_button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER, relwidth=0.4, relheight=0.1)

        # Place Frame
        self.main_menu_frame.pack(fill="both", expand=True)

    def change_frame(self, old_frame, new_frame):
        for widget in old_frame.winfo_children():
            widget.destroy()

        new_frame()

    def pdf_merge_view(self):
        # Variables
        self.pdf_files = []
        self.drag_data = {"x": 0,
                          "y": 0,
                          "selected_index": None}

        # Create Frame
        self.pdf_merge_frame = ctk.CTkFrame(master=self.main_menu_frame)

        # Create Widgets
        self.pdf_add_button = ctk.CTkButton(master=self.pdf_merge_frame,
                                            text="Dodaj plik PDF",
                                            command=self.pdf_add_func)
        self.pdf_remove_button = ctk.CTkButton(master=self.pdf_merge_frame,
                                               text="Usuń plik PDF",
                                               command=self.pdf_remove_func)
        self.pdf_listbox = tk.Listbox(master=self.pdf_merge_frame,
                                      selectmode=tk.SINGLE,
                                      exportselection=False,
                                      height=10,
                                      relief="sunken",
                                      selectbackground="#6694de",
                                      takefocus=True)
        self.pdf_merge_button = ctk.CTkButton(master=self.pdf_merge_frame,
                                              text="Połącz pliki PDF",
                                              command=self.pdf_merge_func)
        self.pdf_up_button = ctk.CTkButton(master=self.pdf_merge_frame,
                                           text="▲",
                                           command=self.move_selected_pdf_up)
        self.pdf_down_button = ctk.CTkButton(master=self.pdf_merge_frame,
                                             text="▼",
                                             command=self.move_selected_pdf_down)

        # Configure Widgets
        for widget in self.pdf_merge_frame.winfo_children():
            widget.configure(font=self.main_font)
        self.pdf_listbox.configure(font=self.list_font)

        button_list = [self.pdf_add_button, self.pdf_remove_button, self.pdf_merge_button,
                       self.pdf_up_button, self.pdf_down_button]

        for button in button_list:
            button.configure(fg_color=self.button_color)

        # Place Widgets
        self.pdf_add_button.place(relx=0.1, rely=0.05, anchor=ctk.NW, relwidth=0.375, relheight=0.1)
        self.pdf_remove_button.place(relx=0.9, rely=0.05, anchor=ctk.NE, relwidth=0.375, relheight=0.1)
        self.pdf_listbox.place(relx=0.5, rely=0.2, anchor=ctk.N, relwidth=0.8, relheight=0.6)
        self.pdf_merge_button.place(relx=0.1, rely=0.85, anchor=ctk.NW, relwidth=0.56, relheight=0.1)

        self.pdf_up_button.place(relx=0.9, rely=0.85, anchor=ctk.NE, relwidth=0.1, relheight=0.1)
        self.pdf_down_button.place(relx=0.78, rely=0.85, anchor=ctk.NE, relwidth=0.1, relheight=0.1)

        # Place Frame
        self.pdf_merge_frame.pack(fill="both", expand=True)

        # Update PDF files
        self.update_pdf_listbox()

    def move_selected_pdf_up(self):
        selected_index = self.pdf_listbox.curselection()
        if selected_index and selected_index[0] > 0:
            self.pdf_files[selected_index[0]], self.pdf_files[selected_index[0] - 1] = (
                self.pdf_files[selected_index[0] - 1],
                self.pdf_files[selected_index[0]]
            )
            self.update_pdf_listbox()
            self.pdf_listbox.selection_set(selected_index[0] - 1)

    def move_selected_pdf_down(self):
        selected_index = self.pdf_listbox.curselection()
        if selected_index and selected_index[0] < len(self.pdf_files) - 1:
            self.pdf_files[selected_index[0]], self.pdf_files[selected_index[0] + 1] = (
                self.pdf_files[selected_index[0] + 1],
                self.pdf_files[selected_index[0]]
            )
            self.update_pdf_listbox()
            self.pdf_listbox.selection_set(selected_index[0] + 1)

    def update_pdf_listbox(self):
        self.pdf_listbox.delete(0, tk.END)
        i = 0
        for pdf_file in self.pdf_files:
            file_name = os.path.basename(pdf_file)
            file_name = f"{i}. {file_name}"
            self.pdf_listbox.insert(tk.END, file_name)
            background_color = "#f2f2f2" if i % 2 else "#d4d4d4"
            self.pdf_listbox.itemconfig(i, {"bg": background_color})
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

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Pliki PDF", "*.pdf")],
            title="Zapisz plik PDF"
        )

        if not file_path.endswith(".pdf"):
            file_path += ".pdf"

        merger.write(file_path)
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
