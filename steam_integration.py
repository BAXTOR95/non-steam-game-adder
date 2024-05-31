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


def create_backup(path):
    backup_path = f"{path}.backup_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    shutil.copy(path, backup_path)
    return backup_path

def format_app_id(app_id):
    return str(app_id).encode('utf-8')

def game_exists(shortcuts_data, app_name):
    return app_name.encode('utf-8') in shortcuts_data

def remove_trailing_bs(data):
    return data.rstrip(BS)

def add_non_steam_game_entry(
    shortcuts_data, app_name, exe, start_dir, app_id, icon='', shortcut_path=''
):
    if b'shortcuts' not in shortcuts_data:
        shortcuts_data = NUL + b'shortcuts' + NUL

    # Remove trailing BS characters if present
    shortcuts_data = remove_trailing_bs(shortcuts_data)

    last_entry_index = shortcuts_data.rfind(NUL + b'0' + NUL)
    if last_entry_index == -1:
        last_entry_index = len(shortcuts_data)

    app_struct = (
        NUL + b'0' + NUL +
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

    return (
        shortcuts_data[:last_entry_index]
        + app_struct
        + shortcuts_data[last_entry_index:]
    )


def process_user_id(
    steam_path, user_id, app_name, exe, start_dir, app_id, icon='', shortcut_path=''
):
    shortcuts_file = os.path.join(
        steam_path, 'userdata', user_id, 'config', 'shortcuts.vdf'
    )

    if not os.path.exists(shortcuts_file):
        print(f"Shortcuts file for user {user_id} not found, creating a new one.")
        open(shortcuts_file, 'wb').write(NUL + b'shortcuts' + NUL)

    backup_file = create_backup(shortcuts_file)
    print(f"Backup created at: {backup_file}")

    shortcuts_data = read_shortcuts_file(shortcuts_file)

    if game_exists(shortcuts_data, app_name):
        print(f"The game '{app_name}' already exists in the shortcuts file.")
        return

    updated_shortcuts_data = add_non_steam_game_entry(
        shortcuts_data,
        app_name=app_name,
        exe=exe,
        start_dir=start_dir,
        app_id=app_id,
        icon=icon,
        shortcut_path=shortcut_path,
    )

    write_shortcuts_file(shortcuts_file, updated_shortcuts_data)
    print(f"Non-Steam game '{app_name}' added for user {user_id} successfully.")


def add_non_steam_game(app_name, exe, start_dir, app_id, icon=''):
    steam_path = locate_steam_installation()
    if not steam_path:
        raise FileNotFoundError("Steam installation not found")

    user_ids = find_steam_user_ids(steam_path)

    for user_id in user_ids:
        process_user_id(steam_path, user_id, app_name, exe, start_dir, app_id, icon)
