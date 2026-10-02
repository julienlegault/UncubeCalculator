import unittest
from collections import Counter
from io import BytesIO
import gzip
import json
from unittest.mock import patch

from uncube_calculator import calculate_statistics, load_card_names


class CalculateStatisticsTests(unittest.TestCase):
    def test_counts_letters_case_insensitively_and_words(self):
        letters, words = calculate_statistics(["The Gathering", "THE"])

        self.assertEqual(letters, {"a": 1, "e": 3, "g": 2, "h": 3, "i": 1, "n": 1, "r": 1, "t": 3})
        self.assertEqual(words, 3)

    def test_ignores_face_separator_and_counts_unicode_letters(self):
        letters, words = calculate_statistics(["Æther // Ice"])

        self.assertEqual(letters, {"æ": 1, "c": 1, "e": 2, "h": 1, "i": 1, "r": 1, "t": 1})
        self.assertEqual(words, 2)

    def test_counts_casefolded_unicode_expansions(self):
        letters, words = calculate_statistics(["Straße"])

        self.assertEqual(letters, {"a": 1, "e": 1, "r": 1, "s": 3, "t": 1})
        self.assertEqual(words, 1)

    def test_counts_accented_letters_as_their_base_letters(self):
        letters, words = calculate_statistics(["Café", "Cafe\u0301"])

        self.assertEqual(letters, {"a": 2, "c": 2, "e": 2, "f": 2})
        self.assertEqual(words, 2)

    def test_empty_names(self):
        self.assertEqual(calculate_statistics([]), (Counter(), 0))

    @patch("uncube_calculator.urlopen")
    def test_loads_names_from_oracle_cards_bulk_data(self, urlopen):
        urlopen.side_effect = [
            BytesIO(
                b'{"data":[{"type":"default_cards","download_uri":"unused"},'
                b'{"type":"oracle_cards","download_uri":"https://example.test/cards"}]}'
            ),
            BytesIO(
                gzip.compress(
                    b'{"name":"Black Lotus"}\n{"name":"Ancestral Recall"}\n'
                )
            ),
        ]

        self.assertEqual(
            list(load_card_names()),
            ["Black Lotus", "Ancestral Recall"],
        )
        self.assertEqual(urlopen.call_count, 2)


if __name__ == "__main__":
    unittest.main()
