import customtkinter as ctk
import tkinter
from PIL import Image

root = ctk.CTk()
ctk.set_appearance_mode("dark")

root.title("Multidata Steganography")



# Left Section
left_frame = ctk.CTkFrame(root)
left_frame.pack(side="left", padx=10, pady=10, fill="both")

canvas = tkinter.Canvas(left_frame, width=700, height=600,)
canvas.grid(row=0, column=0, columnspan=2, pady=5)

open_image_btn = ctk.CTkButton(left_frame, text="Open Image")
open_image_btn.grid(row=1, column=0, padx=10, pady=10)

save_image_btn = ctk.CTkButton(left_frame, text="Save Image")
save_image_btn.grid(row=1, column=1, padx=10, pady=10)


# Right Side

# Creating tab section
tabsection = ctk.CTkTabview(root)
tabsection.pack(side="left", padx=10, pady=10, expand=True, fill="both")


show_data_tab = tabsection.add("🔓  Show Data")
hide_data_tab = tabsection.add("🔒  Hide Data")
tabsection.set("🔓  Show Data")

# Show data section
key_entry = ctk.CTkEntry(show_data_tab, placeholder_text="Enter Key", width=250)
key_entry.grid(row=0, column=0, padx=10, pady=20)
key_submit_button = ctk.CTkButton(show_data_tab, text="Show Data", width=30)
key_submit_button.grid(row=0, column=1, padx=10, pady=20)


hidden_data_textbox_showtab = ctk.CTkTextbox(show_data_tab, border_width=2, border_color="lightblue", border_spacing=10,
                                     fg_color="transparent", height=360, width=350)
hidden_data_textbox_showtab.grid(row=1, column=0, columnspan=2, sticky="we", padx=10, pady=10)
hidden_data_textbox_showtab.insert("0.0", "Hidden data will be displayed here")
hidden_data_textbox_showtab.configure(state="disabled")


show_data_bottom_frame = ctk.CTkFrame(show_data_tab, fg_color="transparent")
show_data_bottom_frame.grid(row=2, column=0, columnspan=2)

save_as_file_btn = ctk.CTkButton(show_data_bottom_frame, text="Save As File", width=100)
save_as_file_btn.grid(row=2, column=0, padx=20, pady=5)
clear_btn_showtab = ctk.CTkButton(show_data_bottom_frame, text="Clear", width=100)
clear_btn_showtab.grid(row=2, column=1, padx=20, pady=5)


# Hide Data Section
def on_select_input_type(choice):
    if choice == "File":
        browse_file_btn.grid(row=0, column=2, padx=10, pady=20)
        hidden_data_textbox_hidetab.delete("0.0", "end")
        hidden_data_textbox_hidetab.configure(state="disabled")

    else:
        browse_file_btn.grid_forget()
        hidden_data_textbox_hidetab.configure(state="normal")



hide_data_top_frame = ctk.CTkFrame(hide_data_tab, fg_color="transparent")
hide_data_top_frame.grid(row=0, column=0)


input_type_label = ctk.CTkLabel(hide_data_top_frame, text="Input type  : ")
input_type_label.grid(row=0, column=0, padx=10, pady=20, sticky='w')

input_type_menu = ctk.CTkOptionMenu(hide_data_top_frame, width=150, values=["Plaintext", "File"], command=on_select_input_type)
input_type_menu.grid(row=0, column=1, padx=10, pady=20)


browse_file_btn = ctk.CTkButton(hide_data_top_frame,  width=30, text="Open File")





hidden_data_textbox_hidetab = ctk.CTkTextbox(hide_data_tab, border_width=3, border_color="lightblue", border_spacing=10,
                                     fg_color="transparent", height=280, width=350)
hidden_data_textbox_hidetab.grid(row=1, column=0, sticky="ew", padx=10, pady=10)


hide_data_bottom_frame = ctk.CTkFrame(hide_data_tab, fg_color="transparent")
hide_data_bottom_frame.grid(row=2, column=0, pady=5)


enter_key_entry_hidetab = ctk.CTkEntry(hide_data_bottom_frame, placeholder_text="Enter Key", width=270)
enter_key_entry_hidetab.grid(row=0, column=0, sticky='nswe', padx=10, pady=5)

confirm_key_entry_hidetab = ctk.CTkEntry(hide_data_bottom_frame, placeholder_text="Confirm Key", width=270)
confirm_key_entry_hidetab.grid(row=1, column=0, sticky='nswe', padx=10, pady=5,)

hide_data_btn = ctk.CTkButton(hide_data_bottom_frame, text="Hide Data", width=30)
hide_data_btn.grid(row=0, column=1, rowspan=2, sticky='nswe', padx=10, pady=5)

clear_btn_hidetab = ctk.CTkButton(hide_data_tab, text="Clear All")
clear_btn_hidetab.grid(row=3, column=0, sticky='ews', padx=10, pady=5)







root.mainloop()