"""
steam_integration.py
====================

This module provides a class containing static methods to integrate non-Steam games into the Steam platform.

Classes
-------
SteamIntegration
    A class containing static methods to manage non-Steam game entries in Steam.

Functions
---------
None

Attributes
----------
STEAM_PATH_OPTIONS : list
    A list of possible paths to the Steam installation directory.

Methods
-------
locate_steam_installation()
    Locate the Steam installation directory.

find_steam_user_ids(steam_path)
    Find all Steam user IDs in the given Steam installation path.

read_shortcuts_file(path)
    Read the shortcuts.vdf file.

write_shortcuts_file(path, data)
    Write to the shortcuts.vdf file.

game_exists(shortcuts_data, app_name)
    Check if a game already exists in the shortcuts data.

find_last_entry_index(shortcuts_data)
    Find the index of the last entry in the shortcuts data.

add_non_steam_game_entry(shortcuts_data, app_name, exe, start_dir, icon='', shortcut_path='')
    Add a new non-Steam game entry to the shortcuts data.

process_user_id(steam_path, user_id, app_name, exe, start_dir, icon='', shortcut_path='')
    Process the addition of a non-Steam game entry for a specific user ID.

add_non_steam_game(app_name, exe, start_dir, icon='')
    Add a non-Steam game to all user profiles in the Steam installation.

Notes
-----
- The `psutil` library is used to iterate over running processes.
- The `subprocess` library is used to open the Steam application.
- Ensure that the `psutil` and `icoextract` libraries are installed in your environment.

Example
-------
To add a non-Steam game to the Steam library for all users:

from steam_integration import SteamIntegration

app_name = "Your Game Name"
exe = "path/to/game.exe"
start_dir = "path/to/game/directory"
icon = "path/to/game/icon"

try:
    SteamIntegration.add_non_steam_game(app_name, exe, start_dir, icon)
    print(f"Non-Steam game '{app_name}' added successfully.")
except FileNotFoundError as e:
    print(e)
"""

import os
import logging

NUL = b'\x00'
SOH = b'\x01'
STX = b'\x02'
BS = b'\x08'


class SteamIntegration:
    """
    A class containing static methods to integrate non-Steam games into the Steam platform.
    """

    STEAM_PATH_OPTIONS = [
        os.path.expanduser('~/.local/share/Steam'),
        'C:\\Program Files (x86)\\Steam',
        'C:\\Program Files\\Steam',
    ]

    @staticmethod
    def locate_steam_installation():
        """
        Locate the Steam installation directory.

        Returns:
            str: The path to the Steam installation directory if found, else None.
        """
        for path in SteamIntegration.STEAM_PATH_OPTIONS:
            if os.path.exists(path):
                logging.info(f"Steam installation found at: {path}")
                return path
        logging.error("Steam installation not found.")
        return None

    @staticmethod
    def find_steam_user_ids(steam_path):
        """
        Find all Steam user IDs in the given Steam installation path.

        Args:
            steam_path (str): The path to the Steam installation directory.

        Returns:
            list: A list of user IDs found in the Steam userdata directory.

        Raises:
            FileNotFoundError: If no Steam user IDs are found.
        """
        userdata_path = os.path.join(steam_path, 'userdata')
        user_ids = [
            d
            for d in os.listdir(userdata_path)
            if os.path.isdir(os.path.join(userdata_path, d))
        ]
        if not user_ids:
            raise FileNotFoundError("No Steam user IDs found")
        logging.info(f"Steam user IDs found: {user_ids}")
        return user_ids

    @staticmethod
    def read_shortcuts_file(path):
        """
        Read the shortcuts.vdf file.

        Args:
            path (str): The path to the shortcuts.vdf file.

        Returns:
            bytes: The contents of the shortcuts.vdf file.
        """
        with open(path, 'rb') as f:
            return f.read()

    @staticmethod
    def write_shortcuts_file(path, data):
        """
        Write to the shortcuts.vdf file.

        Args:
            path (str): The path to the shortcuts.vdf file.
            data (bytes): The data to be written to the file.
        """
        with open(path, 'wb') as f:
            f.write(data)

    @staticmethod
    def game_exists(shortcuts_data, app_name):
        """
        Check if a game already exists in the shortcuts data.

        Args:
            shortcuts_data (bytes): The data from the shortcuts.vdf file.
            app_name (str): The name of the game to check.

        Returns:
            bool: True if the game exists, else False.
        """
        exists = app_name.encode('utf-8') in shortcuts_data
        if exists:
            logging.info(f"The game '{app_name}' already exists in the shortcuts file.")
        return exists

    @staticmethod
    def find_last_entry_index(shortcuts_data):
        """
        Find the index of the last entry in the shortcuts data.

        Args:
            shortcuts_data (bytes): The data from the shortcuts.vdf file.

        Returns:
            int: The index of the last entry in the shortcuts data.
        """
        last_index = 0
        while True:
            index = shortcuts_data.find(NUL + str(last_index).encode('utf-8') + NUL)
            if index == -1:
                break
            last_index += 1
        logging.info(f"Last entry index in shortcuts data: {last_index - 1}")
        return last_index - 1

    @staticmethod
    def add_non_steam_game_entry(
        shortcuts_data, app_name, exe, start_dir, icon='', shortcut_path=''
    ):
        """
        Add a new non-Steam game entry to the shortcuts data.

        Args:
            shortcuts_data (bytes): The data from the shortcuts.vdf file.
            app_name (str): The name of the non-Steam game.
            exe (str): The executable path of the non-Steam game.
            start_dir (str): The start directory of the non-Steam game.
            icon (str, optional): The icon path of the non-Steam game. Defaults to ''.
            shortcut_path (str, optional): The shortcut path. Defaults to ''.

        Returns:
            bytes: The updated shortcuts data with the new non-Steam game entry.
        """
        if b'shortcuts' not in shortcuts_data:
            shortcuts_data = NUL + b'shortcuts' + NUL

        last_entry_index = SteamIntegration.find_last_entry_index(shortcuts_data)
        new_entry_index = last_entry_index + 1

        shortcuts_data = shortcuts_data.rstrip(BS)

        if new_entry_index == 0:
            entry_start = NUL + b'0' + NUL
        else:
            entry_start = NUL + str(new_entry_index).encode('utf-8') + NUL
            shortcuts_data = shortcuts_data + BS + BS

        app_struct = (
            entry_start
            + STX
            + b'appid'
            + NUL
            + (NUL * 4)
            + SOH
            + b'AppName'
            + NUL
            + app_name.encode('utf-8')
            + NUL
            + SOH
            + b'Exe'
            + NUL
            + f'"{exe}"'.encode('utf-8')
            + NUL
            + SOH
            + b'StartDir'
            + NUL
            + os.path.join(start_dir, '').encode('utf-8')
            + NUL
            + SOH
            + b'icon'
            + NUL
            + f'"{icon}"'.encode('utf-8')
            + NUL
            + SOH
            + b'ShortcutPath'
            + NUL
            + shortcut_path.encode('utf-8')
            + NUL
            + SOH
            + b'LaunchOptions'
            + NUL
            + NUL
            + STX
            + b'IsHidden'
            + NUL
            + (NUL * 4)
            + STX
            + b'AllowDesktopConfig'
            + NUL
            + SOH
            + (NUL * 3)
            + STX
            + b'AllowOverlay'
            + NUL
            + SOH
            + (NUL * 3)
            + STX
            + b'OpenVR'
            + NUL
            + (NUL * 4)
            + STX
            + b'Devkit'
            + NUL
            + (NUL * 4)
            + SOH
            + b'DevkitGameID'
            + NUL
            + NUL
            + STX
            + b'DevkitOverrideAppID'
            + NUL
            + (NUL * 4)
            + STX
            + b'LastPlayTime'
            + NUL
            + (NUL * 4)
            + SOH
            + b'FlatpakAppID'
            + NUL
            + NUL
            + NUL
            + b'tags'
            + NUL
            + BS
            + BS
            + BS
            + BS
        )

        logging.info(
            f"Added new non-Steam game entry for '{app_name}' with index {new_entry_index}."
        )
        return shortcuts_data + app_struct

    @staticmethod
    def process_user_id(
        steam_path, user_id, app_name, exe, start_dir, icon='', shortcut_path=''
    ):
        """
        Process the addition of a non-Steam game entry for a specific user ID.

        Args:
            steam_path (str): The path to the Steam installation directory.
            user_id (str): The Steam user ID.
            app_name (str): The name of the non-Steam game.
            exe (str): The executable path of the non-Steam game.
            start_dir (str): The start directory of the non-Steam game.
            icon (str, optional): The icon path of the non-Steam game. Defaults to ''.
            shortcut_path (str, optional): The shortcut path. Defaults to ''.
        """
        shortcuts_file = os.path.join(
            steam_path, 'userdata', user_id, 'config', 'shortcuts.vdf'
        )

        if not os.path.exists(shortcuts_file):
            logging.info(
                f"Shortcuts file for user {user_id} not found, creating a new one."
            )
            with open(shortcuts_file, 'wb') as f:
                f.write(NUL + b'shortcuts' + NUL)

        shortcuts_data = SteamIntegration.read_shortcuts_file(shortcuts_file)

        if SteamIntegration.game_exists(shortcuts_data, app_name):
            logging.info(f"The game '{app_name}' already exists for user {user_id}.")
            return

        updated_shortcuts_data = SteamIntegration.add_non_steam_game_entry(
            shortcuts_data,
            app_name=app_name,
            exe=exe,
            start_dir=start_dir,
            icon=icon,
            shortcut_path=shortcut_path,
        )

        SteamIntegration.write_shortcuts_file(shortcuts_file, updated_shortcuts_data)
        logging.info(
            f"Non-Steam game '{app_name}' added for user {user_id} successfully."
        )

    @staticmethod
    def add_non_steam_game(app_name, exe, start_dir, icon=''):
        """
        Add a non-Steam game to all user profiles in the Steam installation.

        Args:
            app_name (str): The name of the non-Steam game.
            exe (str): The executable path of the non-Steam game.
            start_dir (str): The start directory of the non-Steam game.
            icon (str, optional): The icon path of the non-Steam game. Defaults to ''.

        Raises:
            FileNotFoundError: If the Steam installation is not found.
        """
        steam_path = SteamIntegration.locate_steam_installation()
        if not steam_path:
            raise FileNotFoundError("Steam installation not found")

        user_ids = SteamIntegration.find_steam_user_ids(steam_path)

        for user_id in user_ids:
            SteamIntegration.process_user_id(
                steam_path, user_id, app_name, exe, start_dir, icon
            )


# Configure logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)
