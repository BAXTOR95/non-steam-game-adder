import os
import shutil
from datetime import datetime

NUL = b'\x00'
SOH = b'\x01'
STX = b'\x02'
BS = b'\x08'


def locate_steam_installation():
    steam_path_options = [
        os.path.expanduser('~/.local/share/Steam'),
        'C:\\Program Files (x86)\\Steam',
        'C:\\Program Files\\Steam',
    ]
    return next((path for path in steam_path_options if os.path.exists(path)), None)


def find_steam_user_ids(steam_path):
    userdata_path = os.path.join(steam_path, 'userdata')
    user_ids = [
        d
        for d in os.listdir(userdata_path)
        if os.path.isdir(os.path.join(userdata_path, d))
    ]
    if not user_ids:
        raise FileNotFoundError("No Steam user IDs found")
    return user_ids


def read_shortcuts_file(path):
    with open(path, 'rb') as f:
        return f.read()


def write_shortcuts_file(path, data):
    with open(path, 'wb') as f:
        f.write(data)


def game_exists(shortcuts_data, app_name):
    return app_name.encode('utf-8') in shortcuts_data


def find_last_entry_index(shortcuts_data):
    last_index = 0
    while True:
        index = shortcuts_data.find(NUL + str(last_index).encode('utf-8') + NUL)
        if index == -1:
            break
        last_index += 1
    return last_index - 1


def add_non_steam_game_entry(
    shortcuts_data, app_name, exe, start_dir, icon='', shortcut_path=''
):
    if b'shortcuts' not in shortcuts_data:
        shortcuts_data = NUL + b'shortcuts' + NUL

    last_entry_index = find_last_entry_index(shortcuts_data)
    new_entry_index = last_entry_index + 1

    shortcuts_data = shortcuts_data.rstrip(BS)

    if new_entry_index == 0:
        entry_start = NUL + b'0' + NUL
    else:
        entry_start = NUL + str(new_entry_index).encode('utf-8') + NUL
        # Ensure there are two trailing BS characters
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

    return shortcuts_data + app_struct


def process_user_id(
    steam_path, user_id, app_name, exe, start_dir, icon='', shortcut_path=''
):
    shortcuts_file = os.path.join(
        steam_path, 'userdata', user_id, 'config', 'shortcuts.vdf'
    )

    if not os.path.exists(shortcuts_file):
        print(f"Shortcuts file for user {user_id} not found, creating a new one.")
        open(shortcuts_file, 'wb').write(NUL + b'shortcuts' + NUL)

    shortcuts_data = read_shortcuts_file(shortcuts_file)

    if game_exists(shortcuts_data, app_name):
        print(f"The game '{app_name}' already exists in the shortcuts file.")
        return

    updated_shortcuts_data = add_non_steam_game_entry(
        shortcuts_data,
        app_name=app_name,
        exe=exe,
        start_dir=start_dir,
        icon=icon,
        shortcut_path=shortcut_path,
    )

    write_shortcuts_file(shortcuts_file, updated_shortcuts_data)
    print(f"Non-Steam game '{app_name}' added for user {user_id} successfully.")


def add_non_steam_game(app_name, exe, start_dir, icon=''):
    steam_path = locate_steam_installation()
    if not steam_path:
        raise FileNotFoundError("Steam installation not found")

    user_ids = find_steam_user_ids(steam_path)

    for user_id in user_ids:
        process_user_id(steam_path, user_id, app_name, exe, start_dir, icon)
