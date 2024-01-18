import customtkinter as ctk


def main_menu_view(master):
    # Create Frame
    main_menu_frame = ctk.CTkFrame(master=master)

    # Create Widgets
    merge_button = ctk.CTkButton(master=main_menu_frame,
                                 text="Połącz pliki PDF",
                                 command=lambda: print("Merge"))

    # Place Widgets
    merge_button.pack()

    # Place Frame
    main_menu_frame.pack(fill="both", expand=True)
