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

`brute` tries all 26 keys and prints the one that reads most like English. It scores each candidate
by how common its letter pairs (bigrams) are in English. The counts come from *Pride and Prejudice*.
With `--all` it prints all 26 candidates with the best first.

To rebuild the counts, save https://www.gutenberg.org/cache/epub/1342/pg1342.txt as
`corpus/pride_and_prejudice.txt` and run `python build_bigrams.py`.

## Files

- `caesar.py`: cipher functions and bigram scoring
- `main.py`: command-line interface
- `build_bigrams.py`: counts the letter pairs in the book
- `bigrams.json`: the counts

## Why it is insecure

There are only 26 possible keys. The `brute` mode tries all of them and even picks the right one automatically,
because shifting every letter by the same amount does not hide which letter pairs are common.
A secure cipher needs a key space too large to test, for example AES-256 with 2^256 keys.