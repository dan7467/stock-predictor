import requests

def check_if_symbol_exists(coin):
    response = requests.get(f'https://api.coincap.io/v2/assets/{coin}').json()
    return "data" in response