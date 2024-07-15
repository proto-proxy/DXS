import os
import json
import mmap
import tkinter as tk
from tkinter import filedialog
import requests
from PIL import Image, ImageTk, ImageEnhance
import customtkinter
from io import BytesIO
import pywinstyles
import threading

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

scriptDir = os.path.dirname(__file__)

info_text = """How to use:
    Download the wanted fswap from the discord
    Click upload .fswap
    Wait for the swap to be completed
    You are done!

About DXS:
    DXS is a free, open source hex swapper for Fortnite.
    It was made by @appelmoesGG and @data.flux (proto)
    
    The goals for this project were simple: 
    -fast
    -easy to use
    -open source.
    
    Thanks for using!"""

HEIGHT = 400
WIDTH = 1000

root = customtkinter.CTk()
root.title("𝓓𝓧𝓢 - ( 𝓜𝓐𝓓𝓔 𝓑𝓨 𝓟𝓡𝓞𝓣𝓞𝓣𝓑𝓗 - 𝓪𝓹𝓹𝓮𝓵𝓶𝓸𝓮𝓼𝓰𝓰)")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

def about_window():

      about = customtkinter.CTkToplevel(root, fg_color="#000000")

      about.title("DXS - ABOUT")

      about.geometry("400x400")

      about.resizable(False, False)

      

      about_text = customtkinter.CTkLabel(about, text=info_text, text_color="#ffffff")

      about_text.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            return None
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")
        return None

background_url = "https://raw.githubusercontent.com/proto-proxy/gooners/main/image_2024-07-12_160138896.png"
background_image = download_image(background_url)

if background_image:
    enhancer = ImageEnhance.Brightness(background_image)
    darkened_image = enhancer.enhance(0.8)
    background_photo = ImageTk.PhotoImage(darkened_image)
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
else:
    print("Failed to load background image.")

def get_path(pakchunk_filename):
    launcher_installed = os.path.join(os.environ["PROGRAMDATA"], "Epic", "UnrealEngineLauncher", "LauncherInstalled.dat")
    try:
        with open(launcher_installed, 'r') as f:
            installations = json.load(f)["InstallationList"]
            for installation in installations:
                if installation["AppName"] == "Fortnite":
                    path = installation["InstallLocation"].replace("/", "\\")
                    paks_path = os.path.join(path, "FortniteGame", "Content", "Paks")
                    pakchunk_path = os.path.join(paks_path, pakchunk_filename)
                    return pakchunk_path
    except Exception as e:
        print(f"Failed to find Fortnite installation path: {e}")
        return None

def hex_replace(file_path, search_hex, replace_hex):
    with open(file_path, 'r+b') as f:
        mmapped_file = mmap.mmap(f.fileno(), 0)
        search_bytes = bytes.fromhex(search_hex)
        replace_bytes = bytes.fromhex(replace_hex)
        
        found_at = mmapped_file.find(search_bytes)
        if found_at != -1:
            status_label.config(text="Swapping hex...")
            mmapped_file[found_at:found_at+len(search_bytes)] = replace_bytes
            print_to_console("Replaced hex successfully")
        else:
            print_to_console("Failed to replace hex")
        
        mmapped_file.close()

def process_fswap(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        if len(lines) >= 1:
            pakchunk_filename = lines[0].strip()
            pakchunk_path = get_path(pakchunk_filename)

            if pakchunk_path:
                if len(lines) > 2:
                    search_hex = lines[2].strip()
                    replace_hex = lines[4].strip() if len(lines) > 4 else ""
                    hex_replace(pakchunk_path, search_hex, replace_hex)
                    print_to_console(f"Processed .fswap file: {file_path}")
                    swap_name = os.path.basename(file_path)
                    status_label.config(text=f"Done swapping ({swap_name})")
                else:
                    print_to_console("Invalid .fswap file format")
                    status_label.config(text="Invalid .fswap file format")
            else:
                print_to_console("Failed to find Fortnite installation path")
                status_label.config(text="Failed to find Fortnite installation path")

def upload_fswap():
    status_label.config(text="")  
    file_path = filedialog.askopenfilename(
        title="Select a .fswap file",
        filetypes=(("FSWAP files", "*.fswap"), ("All files", "*.*"))
    )
    if file_path:
        status_label.config(text="Loading swap...")
        threading.Thread(target=process_fswap, args=(file_path,)).start()

def open_custom_swap_window():
    custom_swap_window = customtkinter.CTkToplevel(root)
    custom_swap_window.title("Create Custom Swap")
    custom_swap_window.geometry("600x350")

    if background_image:
        darkened_image_custom = enhancer.enhance(0.8)
        background_photo_custom = ImageTk.PhotoImage(darkened_image_custom)
        background_label_custom = tk.Label(custom_swap_window, image=background_photo_custom)
        background_label_custom.image = background_photo_custom 
        background_label_custom.place(x=0, y=0, relwidth=1, relheight=1)

    font_settings = ("Burbank Big Condensed Black", 13, "bold")

    tk.Label(custom_swap_window, text="Pakchunk Filename:", font=font_settings).pack(pady=5)
    pakchunk_entry = customtkinter.CTkEntry(custom_swap_window)
    pakchunk_entry.pack(pady=5)

    tk.Label(custom_swap_window, text="Search Hex:", font=font_settings).pack(pady=5)
    search_hex_entry = customtkinter.CTkEntry(custom_swap_window)
    search_hex_entry.pack(pady=5)

    tk.Label(custom_swap_window, text="Replace Hex:", font=font_settings).pack(pady=5)
    replace_hex_entry = customtkinter.CTkEntry(custom_swap_window)
    replace_hex_entry.pack(pady=5)

    def create_swap():
        pakchunk_filename = pakchunk_entry.get()
        search_hex = search_hex_entry.get()
        replace_hex = replace_hex_entry.get()

        if pakchunk_filename and search_hex and replace_hex:
            fswap_content = f"{pakchunk_filename}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n{search_hex}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n{replace_hex}\n"

            fswap_filename = f"{pakchunk_filename.split('.')[0]}_custom.fswap"
            with open(fswap_filename, 'w') as fswap_file:
                fswap_file.write(fswap_content)

            status_label.config(text=f"Created custom swap file: {fswap_filename}")
            print_to_console(f"Created custom swap file: {fswap_filename}")
            custom_swap_window.destroy()
        else:
            error_label = tk.Label(custom_swap_window, text="All fields are required", font=font_settings)
            error_label.pack(pady=5)

    create_button = customtkinter.CTkButton(custom_swap_window, text="Create", command=create_swap, font=font_settings)
    create_button.pack(pady=20)

Button1 = customtkinter.CTkButton(
    master=root,
    font=customtkinter.CTkFont('Burbank big cd bk', size=13, weight='bold'),
    corner_radius=0,
    text="Upload .fswap",
    fg_color="#ffffff",
    bg_color="#ffffff",
    hover_color="#ffffff",
    border_color="#ffffff",
    text_color="#000000",
    command=upload_fswap 
)
Button1.place(x=436, y=100)

Button2 = customtkinter.CTkButton(
    master=root,
    font=customtkinter.CTkFont('Burbank big cd bk', size=13, weight='bold'),
    corner_radius=0,
    text="hex swap to fswap",
    fg_color="#ffffff",
    bg_color="#ffffff",
    hover_color="#ffffff",
    border_color="#ffffff",
    text_color="#000000",
    command=open_custom_swap_window 
)
Button2.place(x=436, y=HEIGHT - 100)

about_button = customtkinter.CTkButton(
    master=root,
    corner_radius=90,
    width=20,
    height=20,
    text="?",
    fg_color="#ffffff",
    bg_color="#000000",
    hover_color="#000000",
    border_color="#000000",
    text_color="#000000",
    command=about_window
    
)

about_button.place(x=0,y=0)

import sys
if len(sys.argv) > 1 and sys.argv[1].endswith(".fswap"):
    process_fswap(sys.argv[1])

box_width = 245
box_height = 125
box_x = WIDTH - box_width - 20  
box_y = HEIGHT - box_height - 20  

scrollable_frame = customtkinter.CTkScrollableFrame(root, width=box_width, height=box_height, bg_color="black", fg_color="black")
scrollable_frame.place(x=box_x, y=box_y)

def print_to_console(message):
    label = tk.Label(scrollable_frame, text=message, fg="white", bg="black", font=("Burbank Big Condensed Black", 10), anchor="w", justify="left", borderwidth=0, highlightthickness=0, wraplength=200)
    label.pack(fill="x")

status_label = tk.Label(scrollable_frame, text="", fg="white", bg="black", font=("Burbank Big Condensed Black", 10), borderwidth=0, highlightthickness=0)
status_label.pack()

pywinstyles.set_opacity(scrollable_frame, 0.53)

root.mainloop()
            
