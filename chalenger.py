# Copyright (c) 2024 Renan Evaristo

import os
import sys

import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException

HTTP_OK = 200


def key_validation() -> str:
    load_dotenv()
    api_key = os.getenv("RGAPI_KEY")
    if api_key is None:
        print("Error: Key")

        sys.exit(1)
    else:
        print("Success!")
        return api_key


def main() -> None:

    url_chalenger = "https://br1.api.riotgames.com/tft/league/v1/challenger?queue=RANKED_TFT"

    my_api_key = key_validation()

    headers = {"X-Riot-Token": my_api_key}

    try:
        response = requests.get(url_chalenger, headers=headers, timeout=10)
        if response.status_code == HTTP_OK:
            response.json()
    except RequestException as e:
        print(f"Fail to conect!: {e}")
