from ui import ttk, NonSteamGameAdderApp

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = NonSteamGameAdderApp(root)
    root.mainloop()
