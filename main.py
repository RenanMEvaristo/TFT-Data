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

    load_dotenv()
    api_key = os.getenv("RGAPI_KEY")

    if api_key is None:
        print("ERROR: Key")
    else:
        print("Sucess!")

    game_name = "Juvenal"
    tag_line = "81919"

    url_account = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"

    headers = {"X-Riot-Token": api_key}

    try:
        response = requests.get(url_account, headers=headers, timeout=10)

        if response.status_code == HTTP_OK:
            data = response.json()
            my_puuid = data["puuid"]
            print(f"Sucess! Your PUUID is: {my_puuid}")

            url_matches = f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{my_puuid}/ids?count=10"
            response_matches = requests.get(url_matches, headers=headers, timeout=10)

            if response_matches.status_code == HTTP_OK:
                list_ids = response_matches.json()
                print(f"Games ID's: {list_ids}")
                if list_ids:
                    match_id = list_ids[0]
                    url_matches_info = f"https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}"

                    response_info = requests.get(url_matches_info, headers=headers, timeout=10)

                    if response_info.status_code == HTTP_OK:
                        matches_info = response_info.json()

                        for i, p in enumerate(matches_info["info"]["participants"], start=1):
                            puuid_player = p["puuid"]
                            position = p["placement"]
                            units_info = p["units"]

                            print(f"Player {i} | Position: {position} | PUUID: {puuid_player}...")
                            print("Final Team:")

                            for uni in units_info:
                                name = uni["character_id"].replace("TFT17_", "")
                                stars = uni["tier"]
                                text_itens = ", ".join(uni["itemNames"])
                                item_name = text_itens.replace("TFT_Item_", "").replace("TFT17_Item_", "")

                                print(f" - {name:<12} | Stars: {stars} | Items: {item_name}")

        else:
            print(f"Error:! {response.status_code}: {response.text}")
    except RequestException as e:
        print(f"Fail to conect!: {e}")


if __name__ == "__main__":
    main()
