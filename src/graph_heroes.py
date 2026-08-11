# Copyright (c) 2024 Renan Evaristo

import matplotlib

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from collections import Counter

from main import count_heroes_meta, fill_matches_db, get_challenger_ranking, load_api_key


def show_heroes_chart_in_ram(hero_counter: Counter, top_n: int = 10) -> None:
    """Opens the chart of the most played Heroes directly in a pop-up window in RAM."""
    if not hero_counter:
        print("⚠️ Hero counter is empty.")
        return

    top_heroes = hero_counter.most_common(top_n)

    names = [hero for hero, _ in top_heroes]
    counts = [count for _, count in top_heroes]

    names.reverse()
    counts.reverse()

    plt.figure(figsize=(10, 6))
    bars = plt.barh(names, counts, color="#2ecc71")

    for bar in bars:
        width = bar.get_width()
        plt.text(
            width + 0.2,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width)}",
            ha="left",
            va="center",
            fontweight="bold",
        )

    # Títulos e Estilo Idênticos
    plt.title(f"Top {top_n} Heroes on META (Top 4)", fontsize=14, fontweight="bold")
    plt.xlabel("How many times each hero is choosen", fontsize=12)
    plt.ylabel("Heroes", fontsize=12)
    plt.grid(axis="x", linestyle="--", alpha=0.6)
    plt.tight_layout()

    plt.show()


def main() -> None:
    api_key = load_api_key()
    ranking = get_challenger_ranking(api_key)

    if not ranking:
        print("Fail to get rank")
        return

    top_puuids = [p.puuid for p in ranking.entries]
    matches_db = fill_matches_db(top_puuids, api_key)

    if not matches_db:
        print("No match found")
        return

    hero_counter = count_heroes_meta(matches_db)

    """top_n = selects only the 40 most used heroes"""
    show_heroes_chart_in_ram(hero_counter, top_n=40)


if __name__ == "__main__":
    main()
