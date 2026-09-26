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

def brute_force(text):
    for key in range(26):
        print(key, decrypt(text, key))
