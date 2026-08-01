# Copyright (c) 2024 Renan Evaristo

import os
import sys

import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException
import pandas as pd

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


def validate_connection_get_response(my_api_key: str) -> dict | None:

    url_chalenger = "https://br1.api.riotgames.com/tft/league/v1/challenger?queue=RANKED_TFT"
    headers = {"X-Riot-Token": my_api_key}
    try:
        response = requests.get(url_chalenger, headers=headers, timeout=10)
        if response.status_code == HTTP_OK:
            return response.json()
    except RequestException as e:
        print(f"Fail to connect!: {e}")
    return None


def transfer_data_to_csv(data_ranking: dict) -> None:
    if data_ranking:
        df = pd.DataFrame(data_ranking["entries"])
        df.to_excel("ranking_tft.xlsx", index=False)
        print("Generate document: Sucess!")


def main() -> None:

    my_api_key = key_validation()
    data_ranking = validate_connection_get_response(my_api_key)
    transfer_data_to_csv(data_ranking)
