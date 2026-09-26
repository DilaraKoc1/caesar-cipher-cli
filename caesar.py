# Relative letter frequencies in English text, in percent (A-Z)
ENGLISH_FREQUENCIES = [
    8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.15, 0.77, 4.0, 2.4,
    6.7, 7.5, 1.9, 0.095, 6.0, 6.3, 9.1, 2.8, 0.98, 2.4, 0.15, 2.0, 0.074,
]


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

def score(text):
    """Chi-squared distance between the letter counts of text and English.
    Lower means more English-like."""
    counts = [0] * 26
    for char in text.lower():
        if 'a' <= char <= 'z':
            counts[ord(char) - ord('a')] += 1

    total = sum(counts)
    if total == 0:
        return 0.0

    chi_squared = 0.0
    for observed, frequency in zip(counts, ENGLISH_FREQUENCIES):
        expected = total * frequency / 100
        chi_squared += (observed - expected) ** 2 / expected
    return chi_squared

def brute_force(text):
    """Try all 26 keys and return (key, plaintext) pairs, best guess first."""
    candidates = [(key, decrypt(text, key)) for key in range(26)]
    return sorted(candidates, key=lambda candidate: score(candidate[1]))
