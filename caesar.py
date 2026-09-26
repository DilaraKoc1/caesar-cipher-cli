import json
import math
from functools import cache
from pathlib import Path

BIGRAMS = Path(__file__).parent / 'bigrams.json'


def shift_char(char, key):
    if char.isupper():
        base = ord('A')
    elif char.islower():
        base = ord('a')
    else:
        return char

    position = ord(char) - base
    new_position = (position + key)%26
    return chr(new_position + base)


def encrypt(text, key):
    result = ''
    for char in text:
        result += shift_char(char, key)
    return result

def decrypt(text, key):
    return encrypt(text, -key)

def letters_only(text):
    """Lowercase and drop everything that is not a-z, spaces included."""
    return ''.join(char for char in text.lower() if 'a' <= char <= 'z')

@cache
def log_probabilities():
    """Log probability of every letter pair, with +1 smoothing so unseen pairs are not impossible."""
    counts = json.loads(BIGRAMS.read_text(encoding='utf-8'))
    total = sum(counts.values()) + len(counts)
    return {pair: math.log((count + 1) / total) for pair, count in counts.items()}

def score(text):
    """How English-like text is. Higher is better."""
    letters = letters_only(text)
    table = log_probabilities()
    return sum(table[letters[i:i + 2]] for i in range(len(letters) - 1))

def brute_force(text):
    """Try all 26 keys and return (key, plaintext) pairs, best guess first."""
    candidates = [(key, decrypt(text, key)) for key in range(26)]
    return sorted(candidates, key=lambda candidate: score(candidate[1]), reverse=True)
