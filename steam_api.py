import requests
import logging


class SteamAPI:
    BASE_URL = "http://api.steampowered.com"
    APP_LIST_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"

    def __init__(self, api_key):
        self.api_key = api_key
        self.app_list_cache = None

    def get_steam_id(self, username):
        """Retrieve the Steam ID for a given username."""
        try:
            url = f"{self.BASE_URL}/ISteamUser/ResolveVanityURL/v0001/?key={self.api_key}&vanityurl={username}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            steam_id = data['response'].get('steamid')
            if steam_id:
                logging.info(
                    f"Retrieved Steam ID for username '{username}': {steam_id}"
                )
                return steam_id
            logging.warning(
                f"Steam ID not found for username '{username}'. Response: {data}"
            )
            return None
        except requests.RequestException as e:
            logging.error(f"Error retrieving Steam ID for username '{username}': {e}")
            return None

    def get_app_list(self):
        """Retrieve the list of all Steam applications."""
        try:
            if not self.app_list_cache:
                response = requests.get(self.APP_LIST_URL)
                response.raise_for_status()
                data = response.json()
                self.app_list_cache = data['applist']['apps']
                response_data = response.content
                with open('response_data.txt', 'wb') as file:
                    file.write(response_data)
                logging.info("Retrieved Steam app list.")
            return self.app_list_cache
        except requests.RequestException as e:
            logging.error(f"Error retrieving Steam app list: {e}")
            return []

    def find_app_id(self, game_name):
        """Find the Steam app ID for a given game name."""
        if not game_name or game_name == "":
            return None

        apps = self.get_app_list()
        app_dict = {app['name'].lower(): app['appid'] for app in apps}

        app_id = app_dict.get(game_name.lower())
        if app_id:
            logging.info(f"Found app ID for game '{game_name}': {app_id}")
        else:
            logging.warning(f"App ID not found for game '{game_name}'.")

        return app_id


# Configure logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)
