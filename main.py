import argparse
import sys

import caesar
import vigenere

CIPHERS = {'c': 'caesar', 'v': 'vigenere'}
MODES = {'e': 'encrypt', 'd': 'decrypt', 'b': 'brute'}
# Breaking Vigenère comes later, so brute is not offered for it yet.
VIGENERE_MODES = {'e': 'encrypt', 'd': 'decrypt'}


def prepare(text):
    """Keep only the letters A to Z, in capitals, so the ciphertext shows no word lengths."""
    return caesar.letters_only(text).upper()

def ask_choice(question, choices):
    """Ask until the answer is one of the choices, as a first letter or the full name."""
    letters = list(choices)
    hint = ', '.join(letters[:-1]) + ' or ' + letters[-1]
    while True:
        answer = input(question).strip().lower()
        if answer in choices:
            return choices[answer]
        if answer in choices.values():
            return answer
        print(f'Please enter {hint}.')

def ask_text():
    while True:
        text = input('Text: ')
        if text:
            return text
        print('Please enter some text.')

def ask_key():
    while True:
        answer = input('Key: ')
        try:
            return int(answer)
        except ValueError:
            print('Please enter a whole number, for example 3.')

def ask_keyword():
    while True:
        answer = input('Keyword: ').strip()
        try:
            vigenere.keyword_shifts(answer)
            return answer
        except ValueError:
            print('Please enter a keyword made of the letters A to Z.')

def ask_yes_no(question):
    while True:
        answer = input(question).strip().lower()
        if answer in ('y', 'n'):
            return answer == 'y'
        print('Please enter y or n.')

def print_candidates(candidates):
    for key, plaintext in candidates:
        print(key, plaintext)

def interactive():
    cipher = ask_choice('Cipher? [c]aesar, [v]igenere: ', CIPHERS)
    if cipher == 'caesar':
        mode = ask_choice('Mode? [e]ncrypt, [d]ecrypt, [b]rute: ', MODES)
    else:
        mode = ask_choice('Mode? [e]ncrypt, [d]ecrypt: ', VIGENERE_MODES)
    text = ask_text()

    if mode == 'brute':
        candidates = caesar.brute_force(text)
        key, plaintext = candidates[0]
        print(f'key {key}: {plaintext}')
        if ask_yes_no('Show all 26 candidates? [y/n]: '):
            print_candidates(candidates)
        return

    if mode == 'encrypt':
        text = prepare(text)
        if not text:
            print('Nothing to encrypt: the text has no letters A to Z.')
            return

    if cipher == 'caesar':
        module, key = caesar, ask_key()
    else:
        module, key = vigenere, ask_keyword()
    function = module.encrypt if mode == 'encrypt' else module.decrypt
    print(function(text, key))


def main():
    if len(sys.argv) == 1:
        try:
            interactive()
        except (KeyboardInterrupt, EOFError):
            print()
        return

    parser = argparse.ArgumentParser(description='Encrypt, decrypt or break classical ciphers.')
    parser.add_argument('mode', choices=['encrypt', 'decrypt', 'brute'])
    parser.add_argument('text', help='text to encrypt, decrypt or break')
    parser.add_argument('--cipher', choices=['caesar', 'vigenere'], default='caesar')
    parser.add_argument('--key', help='Caesar: a whole number. Vigenere: a keyword')
    parser.add_argument('--all', action='store_true', help='brute: show all 26 candidates, best first')
    args = parser.parse_args()

    if args.mode == 'brute':
        if args.cipher == 'vigenere':
            parser.error('brute is not available for the Vigenere cipher yet')
        candidates = caesar.brute_force(args.text)
        if args.all:
            print_candidates(candidates)
        else:
            key, plaintext = candidates[0]
            print(f'key {key}: {plaintext}')
        return

    if args.key is None:
        parser.error('key is required for encryption/decryption')
    if args.cipher == 'caesar':
        try:
            key = int(args.key)
        except ValueError:
            parser.error('for the Caesar cipher the key must be a whole number')
        module = caesar
    else:
        try:
            vigenere.keyword_shifts(args.key)
        except ValueError as error:
            parser.error(str(error))
        module, key = vigenere, args.key

    text = args.text
    if args.mode == 'encrypt':
        text = prepare(text)
        if not text:
            parser.error('nothing to encrypt: the text has no letters A to Z')
    function = module.encrypt if args.mode == 'encrypt' else module.decrypt
    print(function(text, key))

if __name__ == '__main__':
    main()
