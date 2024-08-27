"""
game_manager.py
===============

This module provides a class containing static methods to manage game configuration files.

Classes
-------
GameManager
    A class containing static methods to manage game configuration files.

Functions
---------
None

Attributes
----------
None

Methods
-------
find_ini_file(directory)
    Find the first .ini file in the given directory.

update_ini_file(file_path, steam_id)
    Update the .ini file with the given Steam ID.

create_steam_appid_file(directory, app_id)
    Create a steam_appid.txt file with the given app ID in the specified directory.

Notes
-----
- The `os` library is used to handle file and directory operations.
- The `logging` library is used to log information and errors.

Example
-------
To find, update, and create configuration files:

from game_manager import GameManager

# Find .ini file in directory
ini_file = GameManager.find_ini_file("path/to/directory")
if ini_file:
    print(f"Found .ini file: {ini_file}")
else:
    print("No .ini file found.")

# Update .ini file with Steam ID
GameManager.update_ini_file(ini_file, "123456789")

# Create steam_appid.txt file
GameManager.create_steam_appid_file("path/to/directory", 123456)
"""

import os
import logging


class GameManager:
    """
    A class containing static methods to manage game configuration files.
    """

    @staticmethod
    def find_ini_file(directory):
        """
        Find the first .ini file in the given directory.

        Args:
            directory (str): The directory to search for .ini files.

        Returns:
            str: The path to the first .ini file found, else None.
        """
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".ini"):
                    logging.info(f"Found .ini file: {file} in {root}")
                    return os.path.join(root, file)
        logging.warning(f"No .ini file found in directory: {directory}")
        return None

    @staticmethod
    def update_ini_file(file_path, steam_id):
        """
        Update the .ini file with the given Steam ID.

        Args:
            file_path (str): The path to the .ini file to update.
            steam_id (str): The Steam ID to insert into the .ini file.
        """
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()

            with open(file_path, 'w') as file:
                for line in lines:
                    if 'PlayerID=' in line or 'AccountId=' in line:
                        file.write(f"AccountId={steam_id}\n")
                    else:
                        file.write(line)
            logging.info(f"Updated .ini file at {file_path} with Steam ID.")
        except Exception as e:
            logging.error(f"Error updating .ini file at {file_path}: {e}")

    @staticmethod
    def create_steam_appid_file(directory, app_id):
        """
        Create a steam_appid.txt file with the given app ID in the specified directory.

        Args:
            directory (str): The directory to create the steam_appid.txt file in.
            app_id (int): The app ID to write to the steam_appid.txt file.
        """
        try:
            file_path = os.path.join(directory, "steam_appid.txt")
            with open(file_path, 'w') as file:
                file.write(str(app_id))
            logging.info(
                f"Created steam_appid.txt file at {file_path} with app ID: {app_id}"
            )
        except Exception as e:
            logging.error(f"Error creating steam_appid.txt file in {directory}: {e}")


# Configure logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)
