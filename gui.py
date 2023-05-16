import customtkinter as ctk
import tkinter
from PIL import Image, ImageTk
import backend as bnd
from tkinter import messagebox
import os

INITIAL_DIRECTORY = "F:\Projects\Multi-Data-Steganography-Final"

root = ctk.CTk()
ctk.set_appearance_mode("dark")

root.title("Multidata Steganography")

received_secret_data = {"status": False}

is_image_open = False

def openImage():
    global is_image_open
    # filename = tkinter.filedialog.askopenfilename(initialdir="C:/Users/Arnold/Pictures", title="Select a File", filetypes=[('Image File', '*.png')])
    filepath = tkinter.filedialog.askopenfilename(initialdir=INITIAL_DIRECTORY, title="Select a File", filetypes=[('Image File', '*.png *.jpg *.jpeg')])

    if filepath:
        filename, file_ext = os.path.splitext(filepath)
        print(filename, file_ext, type(file_ext))
        # Replace forward slash of filepath with backward slash for proper image saving
        filepath = filepath.replace("/", "\\")
        image = Image.open(filepath)
        # # Convert non png image file to png
        # if file_ext != '.png':
        #     image.save(fr'{filename}.png')
        #     bnd.img_path = fr'{filename}.png'
        # else:
        #     bnd.img_path = filepath
        bnd.img_path = filepath
        print(bnd.img_path)

        image = image.resize((700, 600))

        # Load an image in the script
        one = ImageTk.PhotoImage(image=image)
        root.one = one

        # Add image to the Canvas Items
        canvas.create_image(0, 0, anchor="nw", image=one)

        bnd.load_vault_from_img()
        is_image_open = True


def on_click_save_image():
    bnd.save_image()
    messagebox.showinfo(title="Success", message="You have successfully saved the data to a file")


def on_click_show_data():
    global received_secret_data
    global is_image_open
    if not is_image_open:
        messagebox.showerror(title="Oh oh.. ☹ ", message="You need to first open the image file")
        return
    key = key_entry.get()
    result = bnd.show_data(k=key)

    hidden_data_textbox_showtab.configure(state="normal")
    hidden_data_textbox_showtab.delete("0.0", "end")
    if result["type"] == "plaintext":
        received_secret_data["status"] = True
        received_secret_data["type"] = "plaintext"
        received_secret_data["content"] = result["result"]
        hidden_data_textbox_showtab.insert("0.0", result["result"])
    elif result["type"] == "file":
        received_secret_data["status"] = True
        received_secret_data["type"] = "file"
        received_secret_data["filename"] = result["filename"]
        received_secret_data["content"] = result["filedata"]
        hidden_data_textbox_showtab.insert("0.0",
f'''
Stored File Detail :
--------------------------------
filename : {result["filename"]}
''')
        # hidden_data_textbox_showtab.insert("0.0",
        #                                    f'''
        # Stored File Detail :
        # -------------------
        # filename : {result["filename"]}
        # filesize : {result["filesize"]} MB''')


    else:
        hidden_data_textbox_showtab.insert("0.0", result["result"])
    hidden_data_textbox_showtab.configure(state="disabled")


def on_click_show_data_tab_clear():
    received_secret_data["status"] = False
    key_entry.delete(0, "end")
    hidden_data_textbox_showtab.configure(state="normal")
    hidden_data_textbox_showtab.delete("0.0", "end")
    hidden_data_textbox_showtab.insert("0.0", "Hidden data will be displayed here")
    hidden_data_textbox_showtab.configure(state="disabled")

    # msg = hidden_data_textbox_showtab.get("0.0", "end")
    # if msg[:len(msg)-1] == "Hidden data will be displayed here":
    #     pass
    # else:
    #     hidden_data_textbox_showtab.configure(state="normal")
    #     hidden_data_textbox_showtab.delete("0.0", "end")
    #     hidden_data_textbox_showtab.configure(state="disabled")


def on_click_save_as_file():
    global received_secret_data
    if received_secret_data["status"] == False:
        messagebox.showerror(title="Oh oh.. ☹️", message="You need to first get some data to able to store it")

    else:
        print("here")
        if received_secret_data["type"] == "file":
            print("received file type")
            file_name = received_secret_data["filename"]
            file_type = received_secret_data["filename"].split(".")[-1]
            print(file_type)
            filepath = tkinter.filedialog.asksaveasfilename(initialdir=INITIAL_DIRECTORY,
                                                            title="Select File Storage Path",
                                                            initialfile=file_name,
                                                            filetypes=[(file_type, file_type)],
                                                            defaultextension=file_type)
            # filepath = tkinter.filedialog.asksaveasfilename(initialdir=INITIAL_DIRECTORY, title="Select File Storage Path", initialfile=file_name, defaultextension=".txt")
            # print(filepath, type(filepath))
            if filepath:
                # Save the image data to a file
                with open(filepath, 'wb') as f:
                    f.write(received_secret_data["content"])
                messagebox.showinfo(title="Success", message="You have successfully saved the data to a file")
        else:
            filepath = tkinter.filedialog.asksaveasfilename(initialdir=INITIAL_DIRECTORY,
                                                            title="Select File Storage Path",
                                                            initialfile="secret",
                                                            filetypes=[(".txt", ".txt")],
                                                            defaultextension=".txt")
            if filepath:
                # Save the image data to a file
                with open(filepath, 'w') as f:
                    f.write(received_secret_data["content"])
                messagebox.showinfo(title="Success", message="You have successfully saved the data to a file")


# Left Section
left_frame = ctk.CTkFrame(root)
left_frame.pack(side="left", padx=10, pady=10, fill="both")

canvas = tkinter.Canvas(left_frame, width=700, height=600,)
canvas.grid(row=0, column=0, columnspan=2, pady=5)

open_image_btn = ctk.CTkButton(left_frame, text="Open Image", command=openImage)
open_image_btn.grid(row=1, column=0, padx=10, pady=10)

save_image_btn = ctk.CTkButton(left_frame, text="Save Image", command=on_click_save_image)
save_image_btn.grid(row=1, column=1, padx=10, pady=10)


# Right Side

# Creating tab section
tabsection = ctk.CTkTabview(root)
tabsection.pack(side="left", padx=10, pady=10, expand=True, fill="both")


show_data_tab = tabsection.add("🔓  Show Data")
hide_data_tab = tabsection.add("🔒  Hide Data")
tabsection.set("🔓  Show Data")

# Show data section
key_entry = ctk.CTkEntry(show_data_tab, placeholder_text="Enter Key", width=250, show="*")
key_entry.grid(row=0, column=0, padx=10, pady=20)
key_submit_button = ctk.CTkButton(show_data_tab, text="Show Data", width=30, command=on_click_show_data)
key_submit_button.grid(row=0, column=1, padx=10, pady=20)


hidden_data_textbox_showtab = ctk.CTkTextbox(show_data_tab, border_width=3, border_color="lightblue", border_spacing=10,
                                     fg_color="transparent", height=360, width=350)
hidden_data_textbox_showtab.grid(row=1, column=0, columnspan=2, sticky="we", padx=10, pady=10)
hidden_data_textbox_showtab.insert("0.0", "Hidden data will be displayed here")
hidden_data_textbox_showtab.configure(state="disabled")


show_data_bottom_frame = ctk.CTkFrame(show_data_tab, fg_color="transparent")
show_data_bottom_frame.grid(row=2, column=0, columnspan=2)

save_as_file_btn = ctk.CTkButton(show_data_bottom_frame, text="Save As File", width=100, command=on_click_save_as_file)
save_as_file_btn.grid(row=2, column=0, padx=20, pady=5)
clear_btn_showtab = ctk.CTkButton(show_data_bottom_frame, text="Clear", width=100, command=on_click_show_data_tab_clear)
clear_btn_showtab.grid(row=2, column=1, padx=20, pady=5)

FILE_TYPE = "Plaintext"

secret_filepath = ""


# ---------------------------------------------------------------------------------------------------------------------
# Hide Section Operations

def onclick_hide_data_btn():
    global is_image_open
    global secret_filepath
    key1 = enter_key_entry_hidetab.get()
    key2 = confirm_key_entry_hidetab.get()
    if not is_image_open:
        messagebox.showerror(title="Oh oh.. ☹ ", message="You need to first open the image file")
        return

    if len(key1) == 0 and len(key2) == 0:
        messagebox.showerror(title="Oh oh.. ☹ ", message="You need to enter the key to hide")
        return
    if key1 != key2:
        messagebox.showerror(title="Oh oh.. ☹️", message="The keys you have entered is not matching")
    else:
        if FILE_TYPE == "Plaintext":
            secret_txt = hide_data_textbox_hidetab.get("0.0", "end")
            if len(secret_txt) == 1:
                sure_to_proceed = messagebox.askokcancel(title="Are you sure ?", message="There is no data given to hide in the textbox. This could  erase any previous data stored for this key")
                if sure_to_proceed:
                    confirm_hide = bnd.hide_text(secret_txt, key1, "pop")
                    if confirm_hide:
                        messagebox.showinfo(title="Successful", message="Operation Successful")
                    else:
                        messagebox.showerror(title="Oh oh.. ☹️", message="There seems to be some issue when storing the data")
            else:
                existing_data = bnd.show_data(k=key1)
                if existing_data["type"] in ["plaintext", "file"]:
                    sure_to_proceed = messagebox.askokcancel(title="Are you sure ?",
                                                             message="There is already some data present for this key. This could replace any previous data stored for this key")
                    if sure_to_proceed:

                        confirm_hide = bnd.hide_text(secret_txt, key1, "hide")
                        if confirm_hide:
                            messagebox.showinfo(title="Successful", message="Operation Successful")
                        else:
                            messagebox.showerror(title="Oh oh.. ☹️",
                                                 message="There seems to be some issue when storing the data")
                else:
                    confirm_hide = bnd.hide_text(secret_txt, key1, "hide")
                    if confirm_hide:
                        messagebox.showinfo(title="Successful", message="Operation Successful")
                    else:
                        messagebox.showerror(title="Oh oh.. ☹️",
                                             message="There seems to be some issue when storing the data")
        else:
            # if file type is a File
            print(secret_filepath)
            if secret_filepath:
                existing_data = bnd.show_data(k=key1)
                if existing_data["type"] in ["plaintext", "file"]:
                    sure_to_proceed = messagebox.askokcancel(title="Are you sure ?",
                                                             message="There is already some data present for this key. This could replace any previous data stored for this key")
                    if sure_to_proceed:
                        confirm_hide = bnd.hide_file(secret_filepath, key1)
                        if confirm_hide:
                            messagebox.showinfo(title="Successful", message="Data is hidden successfully")
                        else:
                            messagebox.showerror(title="Oh oh.. ☹️", message="There seems to be some issue when storing the data")
                else:
                    confirm_hide = bnd.hide_file(secret_filepath, key1)
                    if confirm_hide:
                        messagebox.showinfo(title="Successful", message="Operation Successful")
                    else:
                        messagebox.showerror(title="Oh oh.. ☹️",
                                             message="There seems to be some issue when storing the data")
            else:
                messagebox.showerror(title="Oh oh.. ☹ ", message="You have not chosen any file to hide")


def on_select_input_type(choice):
    global FILE_TYPE
    if choice == "File":
        browse_file_btn.grid(row=0, column=2, padx=10, pady=20)
        hide_data_textbox_hidetab.delete("0.0", "end")
        hide_data_textbox_hidetab.configure(state="disabled")
        FILE_TYPE = "File"

    else:
        browse_file_btn.grid_forget()
        hide_data_textbox_hidetab.configure(state="normal")
        hide_data_textbox_hidetab.delete("0.0", "end")
        FILE_TYPE = "Plaintext"


def on_click_browse_file_btn():
    global secret_filepath
    hide_data_textbox_hidetab.configure(state="normal")
    hide_data_textbox_hidetab.delete("0.0", "end")
    hide_data_textbox_hidetab.configure(state="disabled")
    secret_filepath = tkinter.filedialog.askopenfilename(initialdir=INITIAL_DIRECTORY, title="Select a File", filetypes=[('Any File', '*.*')])
    if secret_filepath:
        file_stats = os.stat(secret_filepath)
        # File size in MB
        file_size = file_stats.st_size / (1024 * 1024)
        print(file_size)
        if file_size < 0:
            print("ok")
            file_size = file_stats.st_size / 1024
            print(file_size)
        # Rounding file size
        file_size = round(file_size, 2)
        # print(file_size)
        hide_data_textbox_hidetab.configure(state="normal")
        hide_data_textbox_hidetab.insert("0.0", f'''
Filepath of file to hide :
----------------------------------------------
{secret_filepath}

File size : {file_size} MB
        ''')
        hide_data_textbox_hidetab.configure(state="disabled")


def on_click_hide_data_tab_clear():
    global FILE_TYPE
    enter_key_entry_hidetab.delete(0, "end")
    confirm_key_entry_hidetab.delete(0, "end")
    enter_key_entry_hidetab.configure(placeholder_text="Enter Key")
    confirm_key_entry_hidetab.configure(placeholder_text="Confirm Key")

    if FILE_TYPE == "File":
        hide_data_textbox_hidetab.configure(state="normal")
        hide_data_textbox_hidetab.delete("0.0", "end")
        hide_data_textbox_hidetab.configure(state="disabled")
    else:
        hide_data_textbox_hidetab.delete("0.0", "end")


# --------------------------------------------------------------------------------------------------------------------
# Hide Data GUI Section


hide_data_top_frame = ctk.CTkFrame(hide_data_tab, fg_color="transparent")
hide_data_top_frame.grid(row=0, column=0)


input_type_label = ctk.CTkLabel(hide_data_top_frame, text="Input type  : ")
input_type_label.grid(row=0, column=0, padx=10, pady=20, sticky='w')

input_type_menu = ctk.CTkOptionMenu(hide_data_top_frame, width=150, values=["Plaintext", "File"], command=on_select_input_type)
input_type_menu.grid(row=0, column=1, padx=10, pady=20)


browse_file_btn = ctk.CTkButton(hide_data_top_frame,  width=30, text="Open File", command=on_click_browse_file_btn)





hide_data_textbox_hidetab = ctk.CTkTextbox(hide_data_tab, border_width=3, border_color="lightblue", border_spacing=10,
                                     fg_color="transparent", height=280, width=350)
hide_data_textbox_hidetab.grid(row=1, column=0, sticky="ew", padx=10, pady=10)


hide_data_bottom_frame = ctk.CTkFrame(hide_data_tab, fg_color="transparent")
hide_data_bottom_frame.grid(row=2, column=0, pady=5)


enter_key_entry_hidetab = ctk.CTkEntry(hide_data_bottom_frame, placeholder_text="Enter Key", width=255, show="*")
enter_key_entry_hidetab.grid(row=0, column=0, sticky='nswe', padx=10, pady=5)

confirm_key_entry_hidetab = ctk.CTkEntry(hide_data_bottom_frame, placeholder_text="Confirm Key", width=255, show="*")
confirm_key_entry_hidetab.grid(row=1, column=0, sticky='nswe', padx=10, pady=5,)

hide_data_btn = ctk.CTkButton(hide_data_bottom_frame, text="Hide Data", width=30, command=onclick_hide_data_btn)
hide_data_btn.grid(row=0, column=1, rowspan=2, sticky='nswe', padx=10, pady=5)

clear_btn_hidetab = ctk.CTkButton(hide_data_tab, text="Clear All", command=on_click_hide_data_tab_clear)
clear_btn_hidetab.grid(row=3, column=0, sticky='ews', padx=10, pady=5)



def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)


root.mainloop()