# Copyright (c) 2024 Renan Evaristo

import os
import time
from collections import Counter

import httpx
from dotenv import load_dotenv
from pydantic import ValidationError

from models import ChallengerRanking, Match

HTTP_OK = 200
HTTP_TOO_MANY_REQUESTS = 429
TOP_FOUR = 4
DEBUG = True


CLASS_MAPPER = {
    # Nomes da API da Riot : Nome Bonito no Jogo
    "ASTrait": "Challenger",
    "HPTank": "Brawler",
    "ResistTank": "Bastion",
    "ShieldTank": "Vanguard",
    "ManaTrait": "Conduit",
    "MeleeTrait": "Marauder",
    "RangedTrait": "Sniper",
    "AssassinTrait": "Rogue",
    "APTrait": "Replicator",
    "SummonTrait": "Shepherd",
    "FlexTrait": "Voyager",
    "Fateweaver": "Fateweaver",
}

# src/constants.py

CHAMPION_TRAITS = {
    "Aatrox": ["Challenger", "Brawler"],
    "Briar": ["Rogue", "Brawler"],
    "Caitlyn": ["Sniper", "AnimaSquad"],
    "Chogath": ["Brawler", "Primordian"],
    "Ezreal": ["Sniper", "PsyOps"],
    "Leona": ["Bastion", "Vanguard"],
    "Lissandra": ["Replicator", "DarkStar"],
    "Nasus": ["Brawler", "Bastion"],
    "Poppy": ["Vanguard", "SpaceGroove"],
    "RekSai": ["Marauder", "Rogue"],
    "Talon": ["Rogue", "PsyOps"],
    "Teemo": ["Replicator", "SpaceGroove"],
    "TwistedFate": ["Conduit", "Fateweaver"],
    "Veigar": ["Replicator", "Astronaut"],
    "Akali": ["Rogue", "DRX"],
    "Belveth": ["Marauder", "DarkStar"],
    "Gnar": ["Brawler", "Marauder"],
    "Gragas": ["Bastion", "SpaceGroove"],
    "Gwen": ["Replicator", "AnimaSquad"],
    "Jax": ["Vanguard", "Mecha"],
    "Jinx": ["Sniper", "AnimaSquad"],
    "Meepsie": ["Shepherd", "SpaceGroove"],
    "Milio": ["Replicator", "SpaceGroove"],
    "Mordekaiser": ["Vanguard", "DarkStar"],
    "Pantheon": ["Bastion", "DRX"],
    "Pyke": ["Rogue", "PsyOps"],
    "Zoe": ["Replicator", "Fateweaver"],
    "Aurora": ["Conduit", "Astronaut"],
    "Diana": ["Replicator", "DarkStar"],
    "Fizz": ["Rogue", "SpaceGroove"],
    "Illaoi": ["Brawler", "DRX"],
    "Kaisa": ["Sniper", "AnimaSquad"],
    "Lulu": ["Conduit", "SpaceGroove"],
    "Maokai": ["Brawler", "Astronaut"],
    "MissFortune": ["Sniper", "AnimaSquad"],
    "Ornn": ["Bastion", "Astronaut"],
    "Rhaast": ["Marauder", "Primordian"],
    "Samira": ["Sniper", "PsyOps"],
    "Urgot": ["Sniper", "Primordian"],
    "Viktor": ["Replicator", "PsyOps"],
    "AurelionSol": ["Conduit", "DarkStar"],
    "Corki": ["Sniper", "Astronaut"],
    "Karma": ["Replicator", "DarkStar"],
    "Kindred": ["Sniper", "Fateweaver"],
    "Leblanc": ["Replicator", "DarkStar"],
    "MasterYi": ["Marauder", "PsyOps"],
    "Nami": ["Conduit", "SpaceGroove"],
    "Nunu": ["Brawler", "SpaceGroove"],
    "Rammus": ["Bastion", "SpaceGroove"],
    "Riven": ["Vanguard", "AnimaSquad"],
    "TahmKench": ["Brawler", "SpaceGroove"],
    "TheMightyMech": ["Mecha", "Brawler"],
    "Xayah": ["Sniper", "DRX"],
    "Bard": ["Conduit", "Astronaut"],
    "Blitzcrank": ["Vanguard", "SpaceGroove"],
    "Fiora": ["Marauder", "AnimaSquad"],
    "Graves": ["Sniper", "DRX"],
    "Jhin": ["Sniper", "DarkStar"],
    "Morgana": ["Replicator", "DarkStar"],
    "Shen": ["Bastion", "DRX"],
    "Sona": ["Conduit", "SpaceGroove"],
    "Vex": ["Replicator", "DarkStar"],
    "Zed": ["Rogue", "PsyOps"],
}


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


def count_elements(count: list) -> None:
    return Counter(count)


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


# def get_unit_tratis(unit_id: str) -> list[str]:

#     clean_name = unit_id.replace("TFT17_", "").replace("TFT_", "").replace(" ", " ")

#     return CHAMPION_TRAITS.get(clean_name, ["Unknow"])


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


def analyze_hero_traits_meta(matches: list[Match]) -> dict[str, list[str]]:
    hero_traits_map: dict[str, list[str]] = {}

    for match in matches:
        for participant in match.info.participants:
            for unit in participant.units:
                hero_name = unit.character_id.replace("TFT17_", "").replace("TFT_", "")
                traits = CHAMPION_TRAITS.get(hero_name, ["Don't have traits"])
                hero_traits_map[hero_name] = traits

    return hero_traits_map


# def real_trait_name(trait: list[str]) -> list[str]:

#     real_name_trait = []
#     for traits in trait:
#         real_name = CLASS_MAPPER.get(traits, traits)
#         real_name_trait.append(real_name)
#     return real_name_trait


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

    count_units = count_elements(picked_unit_list)

    print(count_units)


if __name__ == "__main__":
    main()
