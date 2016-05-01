import requests

# Make requests over https
STEAM_OWNED_GAMES_URL = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'


def read_games_for_steamid(steamid, api_key):
    request_params = {'key': str(api_key), 'steamid': str(steamid), 'include_played_free_games': ''}
    r = requests.get(STEAM_OWNED_GAMES_URL, params=request_params)
    print(r)
