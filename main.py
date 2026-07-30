import os
from dotenv import load_dotenv
import requests


def main():

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
        response = requests.get(url_account, headers=headers)

        if response.status_code == 200:
            data = response.json()
            my_puuid = data["puuid"]
            print(f"Sucess! Your PUUID is: {my_puuid}")

            url_matches = f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{my_puuid}/ids?count=10"
            response_matches = requests.get(url_matches, headers=headers)

            if response_matches.status_code == 200:
                list_ids = response_matches.json()
                print(f"Games ID's: {list_ids}")
            else:
                print(f"Error: Game dont found: {response_matches.status_code}")

        else:
            print(f"Error:! {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Fail to connect!: {e}")


if __name__ == "__main__":
    main()
