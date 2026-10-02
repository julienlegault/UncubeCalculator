# UncubeCalculator

Calculate letter frequencies and the total number of words across Magic card
names using Scryfall's Oracle Cards bulk data.

Run the calculator with Python 3:

```sh
python3 uncube_calculator.py
```

The script downloads the current Scryfall bulk data and prints case-insensitive
letter frequencies followed by the total word count. Run the focused tests with:

```sh
python3 -m unittest
```
