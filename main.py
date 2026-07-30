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
                if list_ids:
                    match_id = list_ids[0]
                    url_matches_info = f"https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}"

                    response_info = requests.get(url_matches_info, headers=headers)

                    if response_info.status_code == 200:
                        matches_info = response_info.json()

                        for i, p in enumerate(
                            matches_info["info"]["participants"], start=1
                        ):
                            puuid_player = p["puuid"]
                            position = p["placement"]
                            units_info = p["units"]
                            print(
                                f"Player {i}: {puuid_player} | Position: {position} | PUUID: {puuid_player}..."
                            )
                            print("Final Team:")

                            for uni in units_info:
                                name = uni["character_id"].replace("TFT17_", "")
                                stars = uni["tier"]

                                print(f" - {name:<12} | Stars: {stars}")

        else:
            print(f"Error:! {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Fail to connect!: {e}")


if __name__ == "__main__":
    main()
