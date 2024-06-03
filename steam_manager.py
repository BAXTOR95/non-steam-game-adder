import os
import psutil
import subprocess
import logging


class SteamManager:
    STEAM_PROCESS_NAME = 'steam.exe'
    STEAM_PATH_OPTIONS = [
        os.path.expanduser('~/.local/share/Steam/steam.sh'),
        'C:\\Program Files (x86)\\Steam\\Steam.exe',
        'C:\\Program Files\\Steam\\Steam.exe',
    ]

    @staticmethod
    def is_steam_running():
        """Check if Steam is currently running."""
        for process in psutil.process_iter(['pid', 'name']):
            if SteamManager.STEAM_PROCESS_NAME in process.info['name']:
                logging.info(f"Steam is running with PID: {process.info['pid']}")
                return True
        logging.info("Steam is not running.")
        return False

    @staticmethod
    def close_steam():
        """Terminate the Steam process if it's running."""
        for process in psutil.process_iter(['pid', 'name']):
            if SteamManager.STEAM_PROCESS_NAME in process.info['name']:
                logging.info(
                    f"Terminating Steam process with PID: {process.info['pid']}"
                )
                process.terminate()
                process.wait()
                logging.info("Steam has been terminated.")
                return True
        logging.warning("Steam process not found.")
        return False

    @staticmethod
    def open_steam():
        """Open the Steam application."""
        for path in SteamManager.STEAM_PATH_OPTIONS:
            if os.path.exists(path):
                logging.info(f"Opening Steam from path: {path}")
                subprocess.Popen([path])
                return True
        logging.error("Steam executable not found in any of the specified paths.")
        return False


# Configure logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)
