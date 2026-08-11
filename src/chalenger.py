# Copyright (c) 2024 Renan Evaristo
"Arquivo de testes"

"""
import os
import sys
import time

import pandas as pd
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


def transfer_data_to_xlsx(data_ranking: dict) -> None:
    if data_ranking:
        df = pd.DataFrame(data_ranking["entries"])
        df.to_excel("ranking_tft.xlsx", index=False)
        print("Generate document: Sucess!")


def generate_puuid_list_from_xlsx(xlsx_path: str) -> list[str]:
    # le o arquivo xlsx e gera uma lista de PUUID
    df = pd.read_excel(xlsx_path)
    return df["puuid"].tolist()


def get_matches_by_player(my_api_key: str, my_puuid: str) -> list:

    # gera lista de partidas por PUUID
    url_matches = f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{my_puuid}/ids?count=10"
    headers = {"X-Riot-Token": my_api_key}
    response_matches = requests.get(url_matches, headers=headers, timeout=10)
    if response_matches.status_code == HTTP_OK:
        return response_matches.json()
    return []


def main() -> None:

    my_api_key = key_validation()
    data_ranking = validate_connection_get_response(my_api_key)
    # gera xlsx com os dados do chalenger
    transfer_data_to_xlsx(data_ranking)

    xlsx_path = "/home/renan/codigo/TFT/src/ranking_tft.xlsx"

    # pegar partidas por player
    puuids = generate_puuid_list_from_xlsx(xlsx_path)
    for p_id in puuids:
        match_id = get_matches_by_player(my_api_key, p_id)
        print(f"{match_id}")
        time.sleep(1.2)


if __name__ == "__main__":
    main()
"""
