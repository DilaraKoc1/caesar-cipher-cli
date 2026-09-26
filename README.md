# Caesar Cipher CLI

Encrypt, decrypt and brute-force text with the Caesar cipher.

## Usage

```
python main.py encrypt "Hello World" --key 3
python main.py decrypt "Khoor Zruog" --key 3
python main.py brute "Khoor Zruog"
```

Only letters are shifted. Everything else stays as it is.

## Files

- `caesar.py`: cipher functions
- `main.py`: command-line interface

## Why it is insecure

There are only 26 possible keys. The `brute` mode tries all of them, and you can read the right answer from the output. 
A secure cipher needs a key space too large to test, for example AES-256 with 2^256 keys.