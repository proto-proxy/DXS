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

HEIGHT = 400
WIDTH = 1000

root = customtkinter.CTk()
root.title("𝓓𝓧𝓢 - ( 𝓜𝓐𝓓𝓔 𝓑𝓨 𝓟𝓡𝓞𝓣𝓞𝓣𝓑𝓗 - 𝓪𝓹𝓹𝓮𝓵𝓶𝓸𝓮𝓼𝓰𝓰)")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

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
Button1.place(x=436, y=190)

import sys
if len(sys.argv) > 1 and sys.argv[1].endswith(".fswap"):
    process_fswap(sys.argv[1])

box_width = 225
box_height = 125
box_x = WIDTH - box_width - 20  
box_y = HEIGHT - box_height - 20  

scrollable_frame = customtkinter.CTkScrollableFrame(root, width=box_width, height=box_height, bg_color="black", fg_color="black")
scrollable_frame.place(x=box_x, y=box_y)

def print_to_console(message):
    label = tk.Label(scrollable_frame, text=message, fg="white", bg="black", font=("Burbank Big Condensed Black", 10), anchor="w", justify="left", borderwidth=0, highlightthickness=0)
    label.pack(fill="x")

status_label = tk.Label(scrollable_frame, text="", fg="white", bg="black", font=("Burbank Big Condensed Black", 10), borderwidth=0, highlightthickness=0)
status_label.pack()

pywinstyles.set_opacity(scrollable_frame, 0.53)

root.mainloop()
