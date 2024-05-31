import os
import shutil

def find_ini_file(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".ini"):
                return os.path.join(root, file)
    return None


def update_ini_file(file_path, steam_id, username):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if 'PlayerID=' in line or 'AccountId=' in line:
                file.write(f"AccountId={steam_id}\n")
            elif 'UserName=' in line:
                file.write(f"UserName={username}\n")
            else:
                file.write(line)


def create_steam_appid_file(directory, app_id):
    file_path = os.path.join(directory, "steam_appid.txt")
    with open(file_path, 'w') as file:
        file.write(str(app_id))


def copy_ini_file_to_root(game_directory, ini_file):
    root_ini_path = os.path.join(game_directory, os.path.basename(ini_file))
    shutil.copy(ini_file, root_ini_path)
