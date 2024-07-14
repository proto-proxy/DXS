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

scriptDir = os.path.dirname(__file__)


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
        
def get_background(url):
    backgroundPath=os.path.join(scriptDir, "background.png") 

    if os.path.exists(backgroundPath):
        print("Found image in script dir...")
        return Image.open(backgroundPath)
  
    else:
        print("Image not found in script dir, downloading...")
        downloadedBackground = download_image(url)
    
        if downloadedBackground != None:
            
            downloadedBackground.save(backgroundPath, "png")
    
            return Image.open(backgroundPath)
            
        else:
            return None

background_url = "https://raw.githubusercontent.com/proto-proxy/gooners/main/image_2024-07-12_160138896.png"
background_image = get_background(background_url)

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
            print("Replaced hex successfully")
        else:
            print("Failed to replace hex")
        
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
                    print(f"Processed .fswap file: {file_path}")
                    swap_name = os.path.basename(file_path)
                    status_label.config(text=f"Done swapping ({swap_name})")
                else:
                    print("Invalid .fswap file format")
                    status_label.config(text="Invalid .fswap file format")
            else:
                print("Failed to find Fortnite installation path")
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

black_box = tk.Canvas(root, width=box_width, height=box_height, bg="black")
black_box.place(x=box_x, y=box_y)

status_label = tk.Label(black_box, text="", fg="white", bg="black", font=("Burbank Big Condensed Black", 10))
status_label.place(relx=0.5, rely=0.5, anchor="center")

pywinstyles.set_opacity(black_box, 0.53)

root.mainloop()
