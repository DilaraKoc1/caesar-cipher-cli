"""Vigenère cipher.

Letters are shifted as in Caesar, but each shift comes from the next letter of a
keyword that repeats along the text.
"""

from caesar import shift_char


def keyword_shifts(keyword):
    """Turn a keyword into shifts, A=0 to Z=25. LEMON gives [11, 4, 12, 14, 13]."""
    if not keyword or not all('a' <= char <= 'z' for char in keyword.lower()):
        raise ValueError('the keyword must consist of the letters A to Z')
    return [ord(char) - ord('a') for char in keyword.lower()]

def _shift_text(text, shifts):
    result = ''
    position = 0
    for char in text:
        if char.isalpha():
            result += shift_char(char, shifts[position % len(shifts)])
            position += 1
        else:
            result += char
    return result

def encrypt(text, keyword):
    return _shift_text(text, keyword_shifts(keyword))

def decrypt(text, keyword):
    return _shift_text(text, [-shift for shift in keyword_shifts(keyword)])
