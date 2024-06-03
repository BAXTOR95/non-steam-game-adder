import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog, PhotoImage
from steam_api import SteamAPI
from game_manager import find_ini_file, update_ini_file, create_steam_appid_file
from steam_integration import add_non_steam_game
from steam_manager import SteamManager
from config_management import load_config, save_config
from icon_handler import extract_icon_path
from config import API_KEY
import webbrowser


class NonSteamGameAdderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Non-Steam Game Adder")
        self.root.geometry("600x350")
        self.root.iconbitmap("assets/app_icon.ico")  # Set application icon

        self.steam_manager = SteamManager()
        self.steam_api = SteamAPI(API_KEY)

        self.create_styles()
        self.create_widgets()

    def create_styles(self):
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12), foreground="white")
        style.configure("TEntry", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12))

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=BOTH, expand=True)

        title_label = ttk.Label(
            frame,
            text="Non-Steam Game Adder",
            font=("Helvetica", 16, "bold"),
            foreground="white",
        )
        title_label.grid(row=0, columnspan=3, padx=10, pady=10)

        self.create_form(frame)
        self.create_buttons(frame)

    def create_form(self, frame):
        ttk.Label(frame, text="Game Name:").grid(
            row=1, column=0, padx=10, pady=5, sticky=W
        )
        self.game_name_entry = ttk.Entry(frame, width=30)
        self.game_name_entry.grid(
            row=1, column=1, padx=10, pady=5, sticky=W, columnspan=2
        )

        ttk.Label(frame, text="Steam Username:").grid(
            row=2, column=0, padx=10, pady=5, sticky=W
        )
        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.grid(
            row=2, column=1, padx=10, pady=5, sticky=W, columnspan=2
        )

        config = load_config()
        if 'username' in config:
            self.username_entry.insert(0, config['username'])

        self.create_directory_entry(frame)
        self.create_executable_entry(frame)
        self.create_icon_entry(frame)

    def create_directory_entry(self, frame):
        ttk.Label(frame, text="Game Directory:").grid(
            row=3, column=0, padx=10, pady=5, sticky=W
        )
        self.directory_entry = ttk.Entry(frame, width=30, state="readonly")
        self.directory_entry.grid(row=3, column=1, padx=10, pady=5, sticky=W)
        browse_directory_button = ttk.Button(
            frame, text="Browse", command=self.browse_directory
        )
        browse_directory_button.grid(row=3, column=2, padx=10, pady=5, sticky=W)

    def create_executable_entry(self, frame):
        ttk.Label(frame, text="Executable Path:").grid(
            row=4, column=0, padx=10, pady=5, sticky=W
        )
        self.exe_entry = ttk.Entry(frame, width=30, state="readonly")
        self.exe_entry.grid(row=4, column=1, padx=10, pady=5, sticky=W)
        browse_executable_button = ttk.Button(
            frame, text="Browse", command=self.browse_executable
        )
        browse_executable_button.grid(row=4, column=2, padx=10, pady=5, sticky=W)

    def create_icon_entry(self, frame):
        ttk.Label(frame, text="Icon Path (optional):").grid(
            row=5, column=0, padx=10, pady=5, sticky=W
        )
        self.icon_entry = ttk.Entry(frame, width=30, state="readonly")
        self.icon_entry.grid(row=5, column=1, padx=10, pady=5, sticky=W)

    def create_buttons(self, frame):
        self.add_game_icon = PhotoImage(file="assets/add_game_icon.png")
        add_button = ttk.Button(
            frame,
            text="Add Game",
            image=self.add_game_icon,
            compound=LEFT,
            command=self.add_game,
            bootstyle=SUCCESS,
        )
        add_button.grid(row=6, column=1, padx=10, pady=10, sticky=W)

        self.steam_icon = PhotoImage(file="assets/steam_icon.png")
        open_steam_button = ttk.Button(
            frame,
            text="Open Steam",
            image=self.steam_icon,
            compound=LEFT,
            command=self.steam_manager.open_steam,
            bootstyle=PRIMARY,
        )
        open_steam_button.grid(row=6, column=2, padx=10, pady=10, sticky=W)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_entry.config(state=tk.NORMAL)
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, directory)
            self.directory_entry.config(state="readonly")

    def browse_executable(self):
        exe_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
        if exe_path:
            self.exe_entry.config(state=tk.NORMAL)
            self.exe_entry.delete(0, tk.END)
            self.exe_entry.insert(0, exe_path)
            self.exe_entry.config(state="readonly")
            icon_path = extract_icon_path(exe_path)
            if icon_path:
                self.icon_entry.config(state=tk.NORMAL)
                self.icon_entry.delete(0, tk.END)
                self.icon_entry.insert(0, icon_path)
                self.icon_entry.config(state="readonly")

    def add_game(self):
        game_name = self.game_name_entry.get()
        username = self.username_entry.get()
        game_directory = self.directory_entry.get()
        exe_path = self.exe_entry.get()
        icon_path = self.icon_entry.get()

        config = load_config()
        config['username'] = username
        save_config(config)

        try:
            steam_id = self.steam_api.get_steam_id(username)
            if not steam_id:
                messagebox.showerror(
                    "Error", "Steam Username not found. Please enter a valid username."
                )
                return

            app_id = self.steam_api.find_app_id(game_name)
            if not app_id:
                messagebox.showerror(
                    "Error", "Game Name not found. Please enter a valid game name."
                )
                self.prompt_for_app_id(game_name)
                return

            self.continue_adding_game(
                app_id,
                game_name,
                steam_id,
                username,
                game_directory,
                exe_path,
                icon_path,
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def prompt_for_app_id(self, game_name):
        url = f"https://steamdb.info/search/?a=all&q={game_name}"
        webbrowser.open(url)

        def submit_app_id():
            app_id = app_id_entry.get()
            self.manual_app_id = app_id
            manual_app_id_window.destroy()
            self.continue_adding_game(
                app_id,
                self.game_name_entry.get(),
                self.steam_api.get_steam_id(self.username_entry.get()),
                self.username_entry.get(),
                self.directory_entry.get(),
                self.exe_entry.get(),
                self.icon_entry.get(),
            )

        manual_app_id_window = tk.Toplevel(self.root)
        manual_app_id_window.title("Enter Steam App ID")
        manual_app_id_window.geometry("300x150")

        tk.Label(manual_app_id_window, text="Enter Steam App ID:").pack(pady=10)
        app_id_entry = ttk.Entry(manual_app_id_window, width=30)
        app_id_entry.pack(pady=5)
        submit_button = ttk.Button(
            manual_app_id_window, text="Submit", command=submit_app_id
        )
        submit_button.pack(pady=10)

    def continue_adding_game(
        self, app_id, game_name, steam_id, username, game_directory, exe_path, icon_path
    ):
        try:
            if self.steam_manager.is_steam_running():
                messagebox.showinfo("Info", "Steam needs to be closed to proceed.")
                if not self.steam_manager.close_steam():
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
