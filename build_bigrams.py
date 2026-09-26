"""Count letter pairs in an English book and save them as bigrams.json.

Run once: python build_bigrams.py
"""
import json
from pathlib import Path

from caesar import letters_only

CORPUS = Path(__file__).parent / 'corpus' / 'pride_and_prejudice.txt'
OUTPUT = Path(__file__).parent / 'bigrams.json'


def book_text(raw):
    """Cut off the Project Gutenberg header and footer."""
    start = raw.index('*** START OF')
    start = raw.index('\n', start) + 1    # skip the rest of the marker line
    end = raw.index('*** END OF')
    return raw[start:end]


def count_bigrams(letters):
    counts = {}
    for first in 'abcdefghijklmnopqrstuvwxyz':
        for second in 'abcdefghijklmnopqrstuvwxyz':
            counts[first + second] = 0

    for i in range(len(letters) - 1):
        counts[letters[i:i + 2]] += 1
    return counts


def main():
    raw = CORPUS.read_text(encoding='utf-8')
    letters = letters_only(book_text(raw))
    counts = count_bigrams(letters)
    OUTPUT.write_text(json.dumps(counts, indent=1), encoding='utf-8')
    print(f'{len(letters)} letters, {sum(counts.values())} bigrams -> {OUTPUT.name}')


if __name__ == '__main__':
    main()
