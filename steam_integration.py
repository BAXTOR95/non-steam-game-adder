import os
import logging

NUL = b'\x00'
SOH = b'\x01'
STX = b'\x02'
BS = b'\x08'


class SteamIntegration:
    STEAM_PATH_OPTIONS = [
        os.path.expanduser('~/.local/share/Steam'),
        'C:\\Program Files (x86)\\Steam',
        'C:\\Program Files\\Steam',
    ]

    @staticmethod
    def locate_steam_installation():
        """Locate the Steam installation directory."""
        for path in SteamIntegration.STEAM_PATH_OPTIONS:
            if os.path.exists(path):
                logging.info(f"Steam installation found at: {path}")
                return path
        logging.error("Steam installation not found.")
        return None

    @staticmethod
    def find_steam_user_ids(steam_path):
        """Find all Steam user IDs in the given Steam installation path."""
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
        """Read the shortcuts.vdf file."""
        with open(path, 'rb') as f:
            return f.read()

    @staticmethod
    def write_shortcuts_file(path, data):
        """Write to the shortcuts.vdf file."""
        with open(path, 'wb') as f:
            f.write(data)

    @staticmethod
    def game_exists(shortcuts_data, app_name):
        """Check if a game already exists in the shortcuts data."""
        exists = app_name.encode('utf-8') in shortcuts_data
        if exists:
            logging.info(f"The game '{app_name}' already exists in the shortcuts file.")
        return exists

    @staticmethod
    def find_last_entry_index(shortcuts_data):
        """Find the index of the last entry in the shortcuts data."""
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
        """Add a new non-Steam game entry to the shortcuts data."""
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
            entry_start +
            STX + b'appid' + NUL + (NUL * 4) +
            SOH + b'AppName' + NUL + app_name.encode('utf-8') + NUL +
            SOH + b'Exe' + NUL + f'"{exe}"'.encode('utf-8') + NUL +
            SOH + b'StartDir' + NUL + os.path.join(start_dir, '').encode('utf-8') + NUL +
            SOH + b'icon' + NUL + f'"{icon}"'.encode('utf-8') + NUL +
            SOH + b'ShortcutPath' + NUL + shortcut_path.encode('utf-8') + NUL +
            SOH + b'LaunchOptions' + NUL + NUL +
            STX + b'IsHidden' + NUL + (NUL * 4) +
            STX + b'AllowDesktopConfig' + NUL + SOH + (NUL * 3) +
            STX + b'AllowOverlay' + NUL + SOH + (NUL * 3) +
            STX + b'OpenVR' + NUL + (NUL * 4) +
            STX + b'Devkit' + NUL + (NUL * 4) +
            SOH + b'DevkitGameID' + NUL + NUL +
            STX + b'DevkitOverrideAppID' + NUL + (NUL * 4) +
            STX + b'LastPlayTime' + NUL + (NUL * 4) +
            SOH + b'FlatpakAppID' + NUL + NUL +
            NUL + b'tags' + NUL +
            BS + BS + BS + BS
        )

        logging.info(
            f"Added new non-Steam game entry for '{app_name}' with index {new_entry_index}."
        )
        return shortcuts_data + app_struct

    @staticmethod
    def process_user_id(
        steam_path, user_id, app_name, exe, start_dir, icon='', shortcut_path=''
    ):
        """Process the addition of a non-Steam game entry for a specific user ID."""
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
        """Add a non-Steam game to all user profiles in the Steam installation."""
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
