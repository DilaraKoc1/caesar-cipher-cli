import argparse
from caesar import encrypt, decrypt, brute_force



def main():
    parser = argparse.ArgumentParser(description='Encrypt/Decrypt text or brute force the secret message.')
    parser.add_argument('mode', choices=['encrypt', 'decrypt', 'brute'])
    parser.add_argument('text', help='text to encrypt/decrypt')
    parser.add_argument('--key',type=int, help='key for encryption/decryption')
    args = parser.parse_args()

    if args.mode in ['encrypt', 'decrypt'] and args.key is None:
        parser.error('key is required for encryption/decryption')

    if args.mode == 'encrypt':
        print(encrypt(args.text, args.key))
    elif args.mode == 'decrypt':
        print(decrypt(args.text, args.key))
    elif args.mode == 'brute':
        brute_force(args.text)

if __name__ == '__main__':
    main()