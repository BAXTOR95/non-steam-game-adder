import os
import json
import tkinter as tk
from tkinter import messagebox, filedialog
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
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)

    def browse_executable():
        exe_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
        exe_entry.delete(0, tk.END)
        exe_entry.insert(0, exe_path)
        icon_path = extract_icon_path(exe_path)
        icon_entry.delete(0, tk.END)
        icon_entry.insert(0, icon_path)

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
            if is_steam_running():
                messagebox.showinfo("Info", "Steam needs to be closed to proceed.")
                if not close_steam():
                    messagebox.showerror(
                        "Error", "Unable to close Steam. Please close it manually."
                    )
                    return

            steam_id = get_steam_id(username)
            app_id = find_app_id(game_name)
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

    root = tk.Tk()
    root.title("Steam Non-Steam Game Adder")

    tk.Label(root, text="Game Name:").grid(row=0, column=0)
    game_name_entry = tk.Entry(root)
    game_name_entry.grid(row=0, column=1)

    tk.Label(root, text="Steam Username:").grid(row=1, column=0)
    username_entry = tk.Entry(root)
    username_entry.grid(row=1, column=1)

    config = load_config()
    if 'username' in config:
        username_entry.insert(0, config['username'])

    tk.Label(root, text="Game Directory:").grid(row=2, column=0)
    directory_entry = tk.Entry(root)
    directory_entry.grid(row=2, column=1)
    browse_directory_button = tk.Button(root, text="Browse", command=browse_directory)
    browse_directory_button.grid(row=2, column=2)

    tk.Label(root, text="Executable Path:").grid(row=3, column=0)
    exe_entry = tk.Entry(root)
    exe_entry.grid(row=3, column=1)
    browse_executable_button = tk.Button(root, text="Browse", command=browse_executable)
    browse_executable_button.grid(row=3, column=2)

    tk.Label(root, text="Icon Path (optional):").grid(row=4, column=0)
    icon_entry = tk.Entry(root)
    icon_entry.grid(row=4, column=1)

    add_button = tk.Button(root, text="Add Game", command=add_game)
    add_button.grid(row=5, columnspan=3)

    open_steam_button = tk.Button(root, text="Open Steam", command=open_steam)
    open_steam_button.grid(row=6, columnspan=3)

    root.mainloop()
