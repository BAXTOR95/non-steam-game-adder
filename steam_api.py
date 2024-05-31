import requests
from config import API_KEY


def get_steam_id(username):
    url = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={API_KEY}&vanityurl={username}"
    response = requests.get(url).json()
    return response['response']['steamid']


def get_app_list():
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    response = requests.get(url).json()
    return response['applist']['apps']


def find_app_id(game_name):
    if game_name == "":
        return None

    apps = get_app_list()
    for app in apps:
        if app['name'].lower() == game_name.lower():
            return app['appid']
    return None
