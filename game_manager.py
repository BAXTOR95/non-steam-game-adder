import os
import logging


class GameManager:
    @staticmethod
    def find_ini_file(directory):
        """Find the first .ini file in the given directory."""
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".ini"):
                    logging.info(f"Found .ini file: {file} in {root}")
                    return os.path.join(root, file)
        logging.warning(f"No .ini file found in directory: {directory}")
        return None

    @staticmethod
    def update_ini_file(file_path, steam_id, username):
        """Update the .ini file with the given Steam ID and username."""
        try:
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
            logging.info(
                f"Updated .ini file at {file_path} with Steam ID and username."
            )
        except Exception as e:
            logging.error(f"Error updating .ini file at {file_path}: {e}")

    @staticmethod
    def create_steam_appid_file(directory, app_id):
        """Create a steam_appid.txt file with the given app ID in the specified directory."""
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
