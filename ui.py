import os
import json
import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog, PhotoImage
from steam_api import get_steam_id, find_app_id
from game_manager import find_ini_file, update_ini_file, create_steam_appid_file
from steam_integration import add_non_steam_game
from steam_manager import close_steam, open_steam, is_steam_running
from icoextract import IconExtractor, IconExtractorError

CONFIG_FILE = 'config.json'


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {}


def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)


def extract_icon_path(executable_path):
    try:
        extractor = IconExtractor(executable_path)
        icon_file = os.path.join(os.path.dirname(executable_path), "icon.ico")
        extractor.export_icon(icon_file, num=0)
        return icon_file
    except IconExtractorError:
        print("No icons available, or the resource is malformed")
        pass


def run_app():
    def browse_directory():
        directory = filedialog.askdirectory()
        if directory:
            directory_entry.config(state=tk.NORMAL)
            directory_entry.delete(0, tk.END)
            directory_entry.insert(0, directory)
            directory_entry.config(state="readonly")

    def browse_executable():
        exe_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
        if exe_path:
            exe_entry.config(state=tk.NORMAL)
            exe_entry.delete(0, tk.END)
            exe_entry.insert(0, exe_path)
            exe_entry.config(state="readonly")
            icon_path = extract_icon_path(exe_path)
            if icon_path:
                icon_entry.config(state=tk.NORMAL)
                icon_entry.delete(0, tk.END)
                icon_entry.insert(0, icon_path)
                icon_entry.config(state="readonly")

    def add_game():
        game_name = game_name_entry.get()
        username = username_entry.get()
        game_directory = directory_entry.get()
        exe_path = exe_entry.get()
        icon_path = icon_entry.get()

        config = load_config()
        config['username'] = username
        save_config(config)

        try:
            steam_id = get_steam_id(username)
            if not steam_id:
                messagebox.showerror(
                    "Error", "Steam Username not found. Please enter a valid username."
                )
                return

            app_id = find_app_id(game_name)
            if not app_id:
                messagebox.showerror(
                    "Error", "Game Name not found. Please enter a valid game name."
                )
                return

            if is_steam_running():
                messagebox.showinfo("Info", "Steam needs to be closed to proceed.")
                if not close_steam():
                    messagebox.showerror(
                        "Error", "Unable to close Steam. Please close it manually."
                    )
                    return

            ini_file = find_ini_file(game_directory)

            if ini_file:
                update_ini_file(ini_file, steam_id, username)
                create_steam_appid_file(game_directory, app_id)
                add_non_steam_game(game_name, exe_path, game_directory, icon_path)
                messagebox.showinfo("Success", "Game added successfully!")
            else:
                messagebox.showerror("Error", "INI file not found.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    root = ttk.Window(themename="darkly")
    root.title("Non-Steam Game Adder")
    root.geometry("600x350")
    root.iconbitmap("assets/app_icon.ico")  # Set application icon

    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 12), foreground="white")
    style.configure("TEntry", font=("Helvetica", 12))
    style.configure("TButton", font=("Helvetica", 12))

    frame = ttk.Frame(root, padding=20)
    frame.pack(fill=BOTH, expand=True)

    title_label = ttk.Label(
        frame,
        text="Non-Steam Game Adder",
        font=("Helvetica", 16, "bold"),
        foreground="white",
    )
    title_label.grid(row=0, columnspan=3, padx=10, pady=10)

    ttk.Label(frame, text="Game Name:").grid(row=1, column=0, padx=10, pady=5, sticky=W)
    game_name_entry = ttk.Entry(frame, width=30)
    game_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky=W, columnspan=2)

    ttk.Label(frame, text="Steam Username:").grid(
        row=2, column=0, padx=10, pady=5, sticky=W
    )
    username_entry = ttk.Entry(frame, width=30)
    username_entry.grid(row=2, column=1, padx=10, pady=5, sticky=W, columnspan=2)

    config = load_config()
    if 'username' in config:
        username_entry.insert(0, config['username'])

    ttk.Label(frame, text="Game Directory:").grid(
        row=3, column=0, padx=10, pady=5, sticky=W
    )
    directory_entry = ttk.Entry(frame, width=30, state="readonly")
    directory_entry.grid(row=3, column=1, padx=10, pady=5, sticky=W)
    browse_directory_button = ttk.Button(frame, text="Browse", command=browse_directory)
    browse_directory_button.grid(row=3, column=2, padx=10, pady=5, sticky=W)

    ttk.Label(frame, text="Executable Path:").grid(
        row=4, column=0, padx=10, pady=5, sticky=W
    )
    exe_entry = ttk.Entry(frame, width=30, state="readonly")
    exe_entry.grid(row=4, column=1, padx=10, pady=5, sticky=W)
    browse_executable_button = ttk.Button(
        frame, text="Browse", command=browse_executable
    )
    browse_executable_button.grid(row=4, column=2, padx=10, pady=5, sticky=W)

    ttk.Label(frame, text="Icon Path (optional):").grid(
        row=5, column=0, padx=10, pady=5, sticky=W
    )
    icon_entry = ttk.Entry(frame, width=30, state="readonly")
    icon_entry.grid(row=5, column=1, padx=10, pady=5, sticky=W)

    add_game_icon = PhotoImage(file="assets/add_game_icon.png")
    add_button = ttk.Button(
        frame,
        text="Add Game",
        image=add_game_icon,
        compound=LEFT,
        command=add_game,
        bootstyle=SUCCESS,
    )
    add_button.grid(row=6, column=1, padx=10, pady=10, sticky=W)

    steam_icon = PhotoImage(file="assets/steam_icon.png")
    open_steam_button = ttk.Button(
        frame,
        text="Open Steam",
        image=steam_icon,
        compound=LEFT,
        command=open_steam,
        bootstyle=PRIMARY,
    )
    open_steam_button.grid(row=6, column=2, padx=10, pady=10, sticky=W)

    root.mainloop()
