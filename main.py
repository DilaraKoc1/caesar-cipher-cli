import argparse
import sys

from caesar import encrypt, decrypt, brute_force

MODES = {'e': 'encrypt', 'd': 'decrypt', 'b': 'brute'}


def ask_mode():
    while True:
        answer = input('Mode? [e]ncrypt, [d]ecrypt, [b]rute: ').strip().lower()
        if answer in MODES:
            return MODES[answer]
        if answer in MODES.values():
            return answer
        print('Please enter e, d or b.')

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
    mode = ask_mode()
    text = ask_text()
    if mode == 'encrypt':
        print(encrypt(text, ask_key()))
    elif mode == 'decrypt':
        print(decrypt(text, ask_key()))
    else:
        candidates = brute_force(text)
        key, plaintext = candidates[0]
        print(f'key {key}: {plaintext}')
        if ask_yes_no('Show all 26 candidates? [y/n]: '):
            print_candidates(candidates)


def main():
    if len(sys.argv) == 1:
        try:
            interactive()
        except (KeyboardInterrupt, EOFError):
            print()
        return

    parser = argparse.ArgumentParser(description='Encrypt/Decrypt text or brute force the secret message.')
    parser.add_argument('mode', choices=['encrypt', 'decrypt', 'brute'])
    parser.add_argument('text', help='text to encrypt/decrypt')
    parser.add_argument('--key',type=int, help='key for encryption/decryption')
    parser.add_argument('--all', action='store_true', help='brute: show all 26 candidates, best first')
    args = parser.parse_args()

    if args.mode in ['encrypt', 'decrypt'] and args.key is None:
        parser.error('key is required for encryption/decryption')

    if args.mode == 'encrypt':
        print(encrypt(args.text, args.key))
    elif args.mode == 'decrypt':
        print(decrypt(args.text, args.key))
    elif args.mode == 'brute':
        candidates = brute_force(args.text)
        if args.all:
            print_candidates(candidates)
        else:
            key, plaintext = candidates[0]
            print(f'key {key}: {plaintext}')

if __name__ == '__main__':
    main()
