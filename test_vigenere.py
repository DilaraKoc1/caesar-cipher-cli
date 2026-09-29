"""Tests for vigenere.py.

Run: python -m unittest -v
"""
import unittest

import caesar
from vigenere import decrypt, encrypt, keyword_shifts


class VigenereTest(unittest.TestCase):
    def test_known_example(self):
        self.assertEqual(encrypt('ATTACKATDAWN', 'LEMON'), 'LXFOPVEFRNHR')

    def test_keyword_only_advances_on_letters(self):
        self.assertEqual(encrypt('Attack at dawn!', 'LEMON'), 'Lxfopv ef rnhr!')

    def test_keyword_case_does_not_matter(self):
        self.assertEqual(encrypt('Hello', 'lemon'), encrypt('Hello', 'LEMON'))

    def test_decrypt_reverses_encrypt(self):
        text = 'The quick brown fox jumps over the lazy dog!'
        for keyword in ['A', 'KEY', 'LEMON', 'CRYPTOGRAPHY']:
            with self.subTest(keyword=keyword):
                self.assertEqual(decrypt(encrypt(text, keyword), keyword), text)

    def test_one_letter_keyword_is_caesar(self):
        # D is a shift of 3, so this is the Caesar cipher with key 3.
        self.assertEqual(encrypt('Hello World', 'D'), caesar.encrypt('Hello World', 3))

    def test_rejects_invalid_keywords(self):
        for keyword in ['', 'lem0n', 'le mon']:
            with self.subTest(keyword=keyword):
                with self.assertRaises(ValueError):
                    keyword_shifts(keyword)


if __name__ == '__main__':
    unittest.main()
