# Copyright (c) 2024 Renan Evaristo
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class ChallengerPlayer(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    puuid: str
    league_points: int
    wins: int
    losses: int


class Unit(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    character_id: str
    item_names: list[str]
    tier: int
    rarity: int


class Traits(BaseModel):
    name: str
    num_units: int
    tier_current: int
    tier_total: int


class Participant(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    puuid: str
    placement: int
    level: int
    gold_left: int
    last_round: int
    units: list[Unit]
    traits: list[Traits]


class ChallengerRanking(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    tier: str
    entries: list[ChallengerPlayer]


class MatchInfo(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    game_length: float
    tft_set_number: int
    participants: list[Participant]


class Match(BaseModel):
    metadata: dict
    info: MatchInfo
