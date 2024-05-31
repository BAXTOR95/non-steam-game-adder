import os
import psutil
import subprocess


def is_steam_running():
    for process in psutil.process_iter(['pid', 'name']):
        if 'steam.exe' in process.info['name']:
            return True
    return False


def close_steam():
    for process in psutil.process_iter(['pid', 'name']):
        if 'steam.exe' in process.info['name']:
            process.terminate()
            process.wait()
            return True
    return False


def open_steam():
    steam_path_options = [
        os.path.expanduser('~/.local/share/Steam/steam.sh'),
        'C:\\Program Files (x86)\\Steam\\Steam.exe',
        'C:\\Program Files\\Steam\\Steam.exe',
    ]
    for path in steam_path_options:
        if os.path.exists(path):
            subprocess.Popen([path])
            return True
    return False
