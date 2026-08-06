# Copyright (c) 2024 Renan Evaristo

import os
import sys
import time
from pathlib import Path

import httpx
import pandas as pd
from dotenv import load_dotenv
from pydantic import ValidationError
from models import ChallengerRanking, Match
from collections import Counter


HTTP_OK = 200
HTTP_TOO_MANY_REQUESTS = 429
TOP_FOUR = 4
DEBUG = True


def load_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("RGAPI_KEY")
    if not api_key:
        raise ValueError("Key dont found!")
    return api_key


def get_challenger_ranking(api_key: str) -> ChallengerRanking | None:
    url = "https://br1.api.riotgames.com/tft/league/v1/challenger?queue=RANKED_TFT"
    headers = {"X-Riot-Token": api_key}

    try:
        response = httpx.get(url, headers=headers, timeout=10)
        if response.status_code == HTTP_OK:
            return ChallengerRanking.model_validate(response.json())
    except (httpx.RequestError, ValidationError) as e:
        print(f"Error: Get Rank {e}")

    return None


def get_match_ids_by_puuid(api_key: str, puuid: str, count: int = 5) -> list[str]:
    url = f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids"
    headers = {"X-Riot-Token": api_key}
    params = {"count": count}

    try:
        response = httpx.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == HTTP_TOO_MANY_REQUESTS:
            time.sleep(10)
            return get_match_ids_by_puuid(api_key, puuid, count)

        if response.status_code == HTTP_OK:
            return response.json()
    except httpx.RequestError as e:
        print(f"Error: Match ID: {e}")
    return []


def get_match_details(api_key: str, match_id: str, retries: int = 3) -> Match | None:

    if retries <= 0:
        print(f"Limit exced for match {match_id}...")
        return None

    url = f"https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}"
    headers = {"X-Riot-Token": api_key}

    try:
        response = httpx.get(url, headers=headers, timeout=10)
        if response.status_code == HTTP_TOO_MANY_REQUESTS:
            time.sleep(10)
            return get_match_details(api_key, match_id, retries=retries - 1)

        if response.status_code == HTTP_OK:
            return Match.model_validate(response.json())

    except (httpx.RequestError, ValidationError) as e:
        print(f"Error: Match {match_id}: {e}")

    return None


def analyze_unit_meta(matches: list[Match]) -> list:

    unit_list = []
    atual_team_list = []

    for i, match in enumerate(matches, start=1):
        match_info(match, i)
        for participant in match.info.participants:
            placement = participant.placement

            if placement <= TOP_FOUR:
                print(f"Participant Placement {participant.placement}")
                for unit in participant.units:
                    picked_unit = unit.character_id
                    picked_unit = picked_unit.replace("TFT17_", "")
                    unit_list.append(picked_unit)
                    if DEBUG:
                        atual_team_list.append(picked_unit)  # debug only
                if DEBUG:
                    print(atual_team_list)  # debug only
                    atual_team_list = []  # debug only
        print("End of match")
        print("------------\n\n")

    return unit_list


def count_units(count: list) -> None:
    counting = Counter(count)
    print(counting)


def units_name() -> list:
    return [
        "Aatrox",
        "Briar",
        "Caitlyn",
        "Chogath",
        "Ezreal",
        "Leona",
        "Lissandra",
        "Nasus",
        "Poppy",
        "RekSai",
        "Talon",
        "Teemo",
        "Twisted Fate",
        "Veigar",
        "Akali",
        "Belveth",
        "Gnar",
        "Gragas",
        "Gwen",
        "Jax",
        "Jinx",
        "Meepsie",
        "Milio",
        "Mordekaiser",
        "Pantheon",
        "Pyke",
        "Zoe",
        "Aurora",
        "Diana",
        "Fizz",
        "Illaoi",
        "Kaisa",
        "Lulu",
        "Maokai",
        "Miss Fortune",
        "Ornn",
        "Rhaast",
        "Samira",
        "Urgot",
        "Viktor",
        "Aurelion Sol",
        "Corki",
        "Karma",
        "Kindred",
        "Leblanc",
        "Master Yi",
        "Nami",
        "Nunu",
        "Rammus",
        "Riven",
        "Tahm Kench",
        "The Mighty Mech",
        "Xayah",
        "Bard",
        "Blitzcrank",
        "Fiora",
        "Graves",
        "Jhin",
        "Morgana",
        "Shen",
        "Sona",
        "Vex",
        "Zed",
    ]


def fill_matches_db(puuids: list, api: str) -> list:
    matches_db = []
    for i, puuid in enumerate(puuids, start=1):
        print(f"\n [{i} / {len(puuids)}] Mining match PUUID: {puuid[:10]}...")
        match_ids = get_match_ids_by_puuid(api, puuid, count=2)

        for m_id in match_ids:
            match_obj = get_match_details(api, m_id)

            if match_obj:
                matches_db.append(match_obj)
            time.sleep(1.2)
    return matches_db


def analyze_trait_meta(matches: list[Match]) -> None:
    trait_list = []
    for match in matches:
        for participant in match.info.participants:
            for traits in participant.traits:
                trait_name = traits.name
                trait_name = trait_name.replace("TFT17_", "")
                trait_list.append(trait_name)
    print(f"{trait_list}")


def match_info(matches: list[Match], idx: int) -> None:

    duration_min = matches.info.game_length / 60
    total_players = len(matches.info.participants)
    print(f"Match #{idx}: Duration: {duration_min:.1f} min | Players: {total_players}")


def main() -> None:

    api_key = load_api_key()
    ranking = get_challenger_ranking(api_key)

    if not ranking:
        print("Error: Fail to get ranking")
        return

    top_puuids = [player.puuid for player in ranking.entries[:3]]

    print(f"{len(ranking.entries)} Players loaded on RAM")
    print(f"Selected {len(top_puuids)} Players to mine matches")

    matches_db = fill_matches_db(top_puuids, api_key)

    picked_unit_list = analyze_unit_meta(matches_db)
    count_units(picked_unit_list)


if __name__ == "__main__":
    main()
