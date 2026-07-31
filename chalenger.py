import os

import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException

# Copyright (c) 2024 Renan Evaristo

HTTP_OK = 200


def main() -> None:

    load_dotenv()
    api_key = os.getenv("RGAPI_KEY")

    if api_key is None:
        print("Error: Key")
        return
    else:
        print("Sucess!")

    url_chalenger = "https://br1.api.riotgames.com/tft/league/v1/challenger?queue=RANKED_TFT"

    headers = {"X-Riot-Token": api_key}

    try:
        response = requests.get(url_chalenger, headers=headers, timeout=10)
        if response.status_code == HTTP_OK:
            response.json()
    except RequestException as e:
        print(f"Fail to conect!: {e}")
