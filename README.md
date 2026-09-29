# Cipher Breaker

Encrypt, decrypt and break classical ciphers. It currently supports the Caesar and Vigenere ciphers.

## Usage

```
python main.py encrypt "Hello World" --key 3
python main.py decrypt "Khoor Zruog" --key 3
python main.py brute "Khoor Zruog"
python main.py brute "Khoor Zruog" --all
python main.py encrypt "Attack at dawn!" --cipher vigenere --key LEMON
python main.py decrypt "LXFOPVEFRNHR" --cipher vigenere --key LEMON
python main.py
```

Without arguments, `main.py` asks for the cipher, the mode, the text and, for encrypt and
decrypt, the key or keyword.

When encrypting, everything except the letters A to Z is removed and the rest is put in
capitals, so the ciphertext does not show word lengths. Decrypting gives the letters back
without spaces. Breaking Vigenere is not available yet.

`brute` tries all 26 keys and prints the one that reads most like English. It scores each candidate
by how common its letter pairs (bigrams) are in English. The counts come from *Pride and Prejudice*.
With `--all` it prints all 26 candidates with the best first.

To rebuild the counts, save https://www.gutenberg.org/cache/epub/1342/pg1342.txt as
`corpus/pride_and_prejudice.txt` and run `python build_bigrams.py`.

## Tests

```
python -m unittest -v
```

The tests cover shifting, encrypting and decrypting with every key, and brute force on
known examples, including a text without spaces and a single word. `test_main.py` covers
the interactive mode and checks that passing arguments still works. Only the standard
library is needed.

## Files

- `caesar.py`: cipher functions and bigram scoring
- `vigenere.py`: Vigenere cipher
- `main.py`: command-line interface
- `build_bigrams.py`: counts the letter pairs in the book
- `bigrams.json`: the counts
- `test_caesar.py`: tests for `caesar.py`
- `test_vigenere.py`: tests for `vigenere.py`
- `test_main.py`: tests for the command-line interface

## Why the Caesar cipher is insecure

There are only 26 possible keys. The `brute` mode tries all of them and even picks the right one automatically,
because shifting every letter by the same amount does not hide which letter pairs are common.
A secure cipher needs a key space too large to test, for example AES-256 with 2^256 keys.