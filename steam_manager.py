"""
steam_manager.py
================

This module provides a class to manage the Steam application, including checking if it is running,
terminating it, and opening it.

Classes
-------
SteamManager
    A class containing static methods to manage the Steam application.

Functions
---------
None

Attributes
----------
STEAM_PROCESS_NAME : str
    The name of the Steam process.
STEAM_PATH_OPTIONS : list
    A list of possible paths to the Steam executable.

Methods
-------
is_steam_running()
    Check if Steam is currently running.

close_steam()
    Terminate the Steam process if it's running.

open_steam()
    Open the Steam application.

Notes
-----
- The `psutil` library is used to iterate over running processes.
- The `subprocess` library is used to open the Steam application.
- Ensure that the `psutil` and `icoextract` libraries are installed in your environment.

Example
-------
To check if Steam is running, close it if it is, and then open it:

from steam_manager import SteamManager

if SteamManager.is_steam_running():
    if SteamManager.close_steam():
        print("Steam closed successfully.")
    else:
        print("Failed to close Steam.")
else:
    print("Steam is not running.")

if SteamManager.open_steam():
    print("Steam opened successfully.")
else:
    print("Failed to open Steam.")
"""

import os
import psutil
import subprocess
import logging


class SteamManager:
    """
    A class containing static methods to manage the Steam application, including checking if it is running,
    terminating it, and opening it.
    """

    STEAM_PROCESS_NAME = 'steam.exe'
    STEAM_PATH_OPTIONS = [
        os.path.expanduser('~/.local/share/Steam/steam.sh'),
        'C:\\Program Files (x86)\\Steam\\Steam.exe',
        'C:\\Program Files\\Steam\\Steam.exe',
    ]

    @staticmethod
    def is_steam_running():
        """
        Check if Steam is currently running.

        Returns:
            bool: True if Steam is running, False otherwise.
        """
        for process in psutil.process_iter(['pid', 'name']):
            if SteamManager.STEAM_PROCESS_NAME in process.info['name']:
                logging.info(f"Steam is running with PID: {process.info['pid']}")
                return True
        logging.info("Steam is not running.")
        return False

    @staticmethod
    def close_steam():
        """
        Terminate the Steam process if it's running.

        Returns:
            bool: True if the Steam process was found and terminated, False otherwise.
        """
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
        """
        Open the Steam application.

        Returns:
            bool: True if the Steam application was found and opened, False otherwise.
        """
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
