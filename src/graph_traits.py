import matplotlib

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from collections import Counter

from main import count_traits_meta, fill_matches_db, get_challenger_ranking, load_api_key


def show_traits_chart_in_ram(trait_counter: Counter, top_n: int = 10) -> None:
    if not trait_counter:
        print("No traits found.")
        return

    top_traits = trait_counter.most_common(top_n)

    names = [trait for trait, _ in top_traits]
    counts = [count for _, count in top_traits]

    names.reverse()
    counts.reverse()

    plt.figure(figsize=(10, 6))
    bars = plt.barh(names, counts, color="#3498db")

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

    # Títulos e Estilo
    plt.title(f"Top {top_n} Traits / (Top 4)", fontsize=14, fontweight="bold")
    plt.xlabel("Most Picked", fontsize=12)
    plt.ylabel("Traits", fontsize=12)
    plt.grid(axis="x", linestyle="--", alpha=0.6)
    plt.tight_layout()

    plt.show()


def main() -> None:
    api_key = load_api_key()
    ranking = get_challenger_ranking(api_key)

    if not ranking:
        print("Fail to get rank.")
        return

    top_puuids = [p.puuid for p in ranking.entries]
    matches_db = fill_matches_db(top_puuids, api_key)

    if not matches_db:
        print("No matches found.")
        return

    trait_counter = count_traits_meta(matches_db)

    show_traits_chart_in_ram(trait_counter, top_n=40)


if __name__ == "__main__":
    main()
