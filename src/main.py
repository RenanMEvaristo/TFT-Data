import os
import time
from collections import Counter

import httpx
from dotenv import load_dotenv
from pydantic import ValidationError

from constants import CHAMPION_TRAITS, HTTP_OK, HTTP_TOO_MANY_REQUESTS, TOP_FOUR
from models import ChallengerRanking, Match, Participant, Unit


def load_api_key() -> str:
    "Function that loads the API key from the .env file and returns the key if it is valid."

    load_dotenv()
    api_key = os.getenv("RGAPI_KEY")
    if not api_key:
        raise ValueError("Key dont found!")
    return api_key


def get_challenger_ranking(api_key: str) -> ChallengerRanking | None:
    """A function that takes the API key as an argument and loads the TFT Ranked"
    Challenger league, returning either the JSON file or None."""
    url = "https://br1.api.riotgames.com/tft/league/v1/challenger?queue=RANKED_TFT"
    headers = {"X-Riot-Token": api_key}

    try:
        response = httpx.get(url, headers=headers, timeout=10)
        if response.status_code == HTTP_OK:
            return ChallengerRanking.model_validate(response.json())
    except (httpx.RequestError, ValidationError) as e:
        print(f"Error: Get Rank {e}")

    return None


def get_match_ids_by_puuid(api_key: str, puuid: str, max_matches_to_fetch: int = 5) -> list[str]:
    """
    - puuid: unique identifer of the player
    - count: max number of matches to fetch
    - Time.sleep to avoid exceeding requests per minute.
    """

    url = f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids"
    headers = {"X-Riot-Token": api_key}
    params = {"count": max_matches_to_fetch}

    try:
        response = httpx.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == HTTP_TOO_MANY_REQUESTS:
            time.sleep(10)
            return get_match_ids_by_puuid(api_key, puuid, max_matches_to_fetch)

        if response.status_code == HTTP_OK:
            return response.json()
    except httpx.RequestError as e:
        print(f"Error: Match ID: {e}")
    return []


def get_match_details(api_key: str, match_id: str, retries: int = 3) -> Match | None:
    """
    If necessary, automatically retries 2 times. Timeouts after 10 seconds.
    Returns None if ANY error occurs.
    """

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


def get_hero_traits(unit: Unit) -> tuple[str, list[str]]:
    """
    Returns a tuple containing the heroes' names and their traits.
    """

    hero_name = unit.character_id.replace("TFT17_", "").replace("TFT_", "")
    traits = CHAMPION_TRAITS.get(hero_name, ["No trait"])
    return hero_name, traits


def extract_team_comp(participant: Participant) -> dict[str, list[str]]:
    """
    For each player,
    Returns a Dict with the hero's name and traits.
    """
    team_comp = {}
    for unit in participant.units:
        hero_name, traits = get_hero_traits(unit)
        team_comp[hero_name] = traits
    return team_comp


def analyze_unit_meta(matches: list[Match]) -> dict:
    """
    Selects the top 4 from each match and returns the hero names followed by their traits.
    E.g. Leona: Vanguard
    """

    matches_report = {}

    for i, match in enumerate(matches, start=1):
        match_key = f"Match #{i}"
        matches_report[match_key] = {}

        print(f"\n{match_key} (Duration: {match.info.game_length / 60:.1f} min)")

        for participant in match.info.participants:
            placement = participant.placement

            if placement <= TOP_FOUR:
                placement_key = f"Placement {participant.placement}"

                team_comp = extract_team_comp(participant)
                matches_report[match_key][placement_key] = team_comp

    return matches_report


def print_matches_player_traits(matches_report: dict) -> None:
    """Function that prints the heroes' traits"""

    for match_key, placements in matches_report.items():
        print(f"\n{match_key}")
        for placement_key, team in placements.items():
            print(f"{placement_key}")
            for hero, traits in team.items():
                traits_str = ", ".join(traits)
                print(f"{hero:<15} -> Traits: {traits_str}")


def count_heroes_meta(matches: list[Match]) -> Counter:
    """Function that counts the number of times a hero appears in the top 4."""
    heroes_list = []
    for match in matches:
        for participant in match.info.participants:
            if participant.placement <= TOP_FOUR:
                for unit in participant.units:
                    hero_name = unit.character_id.replace("TFT17_", "").replace("TFT_", "")
                    heroes_list.append(hero_name)
    return Counter(heroes_list)


def count_traits_meta(matches: list[Match]) -> Counter:
    """Function that counts the number of times a hero appears in the top 4."""
    traits_list = []
    for match in matches:
        for participant in match.info.participants:
            if participant.placement <= TOP_FOUR:
                for unit in participant.units:
                    hero_name = unit.character_id.replace("TFT17_", "").replace("TFT_", "")
                    traits = CHAMPION_TRAITS.get(hero_name, [])
                    traits_list.extend(traits)  # lista de traits
    return Counter(traits_list)


def fill_matches_db(puuids: list, api: str) -> list:
    """Populates a list with match data. Uses `time.sleep` to avoid exceeding the request limit."""
    matches_db = []
    for i, puuid in enumerate(puuids, start=1):
        print(f"\n [{i} / {len(puuids)}] Mining match PUUID: {puuid[:10]}...")
        match_ids = get_match_ids_by_puuid(api, puuid, max_matches_to_fetch=2)

        for m_id in match_ids:
            match_obj = get_match_details(api, m_id)

            if match_obj:
                matches_db.append(match_obj)
            time.sleep(1.2)
    return matches_db


def match_info(matches: Match, idx: int) -> None:
    """Function that prints the duration and number of players for each match."""

    duration_min = matches.info.game_length / 60
    total_players = len(matches.info.participants)
    print(f"Match #{idx}: Duration: {duration_min:.1f} min | Players: {total_players}")


def main() -> None:

    api_key = load_api_key()
    ranking = get_challenger_ranking(api_key)

    if not ranking:
        print("Error: Fail to get ranking")
        return

    top_puuids = [player.puuid for player in ranking.entries]

    print(f"{len(ranking.entries)} Players loaded on RAM")
    print(f"Selected {len(top_puuids)} Players to mine matches")

    matches_db = fill_matches_db(top_puuids, api_key)

    matches_report = analyze_unit_meta(matches_db)
    print_matches_player_traits(matches_report)

    print("TOP 4 HEROES IN META (TOP 4 POSITION)")
    hero_counter = count_heroes_meta(matches_db)
    for hero, count in hero_counter.most_common():
        print(f"{hero:<15} -> Picked: {count} times")

    trait_counter = count_traits_meta(matches_db)
    for trait, count in trait_counter.most_common():
        print(f"{trait:<15} -> Frequency: {count} times")


if __name__ == "__main__":
    main()
