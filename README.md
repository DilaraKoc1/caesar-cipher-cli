# Caesar Cipher CLI

Encrypt, decrypt and brute-force text with the Caesar cipher.

## Usage

```
python main.py encrypt "Hello World" --key 3
python main.py decrypt "Khoor Zruog" --key 3
python main.py brute "Khoor Zruog"
python main.py brute "Khoor Zruog" --all
```

Only letters are shifted. Everything else stays as it is.

`brute` tries all 26 keys and prints the one whose letter frequencies are closest to English
(chi-squared test). With `--all` it prints all 26 candidates with the best first. On very short texts
the best guess can be wrong, so check the list in that case.

## Files

- `caesar.py`: cipher functions
- `main.py`: command-line interface

## Why it is insecure

There are only 26 possible keys. The `brute` mode tries all of them and even picks the right one automatically,
because shifting letters does not hide how often each letter occurs.
A secure cipher needs a key space too large to test, for example AES-256 with 2^256 keys.