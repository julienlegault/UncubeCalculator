#!/usr/bin/env python3
"""Calculate letter and word totals across Scryfall card names."""

from collections import Counter
import gzip
import json
import re
import unicodedata
from urllib.request import Request, urlopen


BULK_DATA_URL = "https://api.scryfall.com/bulk-data"
USER_AGENT = "UncubeCalculator/1.0"
WORD_PATTERN = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*", re.UNICODE)


def calculate_statistics(names):
    """Return case-insensitive letter frequencies and the total word count."""
    letters = Counter()
    word_count = 0

    for name in names:
        letters.update(
            folded
            for character in name
            for folded in unicodedata.normalize("NFD", character.casefold())
            if folded.isalpha()
        )
        word_count += len(WORD_PATTERN.findall(name))

    return letters, word_count


def load_card_names():
    """Stream names from Scryfall's gzipped Oracle Cards JSONL bulk dataset."""
    request = Request(
        BULK_DATA_URL,
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
    )
    with urlopen(request, timeout=60) as response:
        bulk_data = json.load(response)

    oracle_cards = next(
        (entry for entry in bulk_data["data"] if entry["type"] == "oracle_cards"),
        None,
    )
    if oracle_cards is None:
        raise RuntimeError("Scryfall did not provide an oracle_cards bulk dataset")

    request = Request(
        oracle_cards["jsonl_download_uri"],
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
    )
    with urlopen(request, timeout=120) as response:
        with gzip.GzipFile(fileobj=response) as archive:
            for line in archive:
                if line.strip():
                    yield json.loads(line)["name"]


def main():
    letters, word_count = calculate_statistics(load_card_names())
    print("Letter frequencies:")
    for letter in sorted(letters):
        print(f"{letter}: {letters[letter]}")
    print(f"Total words: {word_count}")


if __name__ == "__main__":
    main()
