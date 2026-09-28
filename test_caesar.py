"""Tests for caesar.py.

Run: python -m unittest -v
"""
import unittest

from caesar import brute_force, decrypt, encrypt, letters_only, log_probabilities, shift_char


class ShiftTest(unittest.TestCase):
    def test_shifts_upper_and_lower_case(self):
        self.assertEqual(shift_char('A', 3), 'D')
        self.assertEqual(shift_char('a', 3), 'd')

    def test_wraps_around_the_alphabet(self):
        self.assertEqual(shift_char('x', 3), 'a')
        self.assertEqual(shift_char('Z', 1), 'A')

    def test_leaves_non_letters_alone(self):
        for char in ' 1!?.':
            self.assertEqual(shift_char(char, 3), char)


class EncryptDecryptTest(unittest.TestCase):
    def test_known_example(self):
        self.assertEqual(encrypt('Hello World', 3), 'Khoor Zruog')

    def test_decrypt_reverses_encrypt_for_every_key(self):
        text = 'The quick brown fox jumps over the lazy dog!'
        for key in range(26):
            with self.subTest(key=key):
                self.assertEqual(decrypt(encrypt(text, key), key), text)

    def test_keys_repeat_every_26(self):
        self.assertEqual(encrypt('Hello', 29), encrypt('Hello', 3))


class BruteForceTest(unittest.TestCase):
    def test_finds_plaintext(self):
        # The cases from the README and the blog post. Words of two or three letters are left
        # out on purpose: bigram scoring gets most of them wrong, which is a known limit.
        cases = [
            ('Hello World', 3),
            ('The quick brown fox jumps over the lazy dog', 11),
            ('ATTACKATDAWN', 7),
            ('secret', 20),
        ]
        for plaintext, key in cases:
            with self.subTest(plaintext=plaintext):
                best = brute_force(encrypt(plaintext, key))[0]
                self.assertEqual(best, (key, plaintext))

    def test_returns_every_key_once(self):
        keys = [key for key, plaintext in brute_force('Khoor Zruog')]
        self.assertEqual(sorted(keys), list(range(26)))

    def test_text_without_letters_does_not_crash(self):
        # Without letters all 26 candidates are identical, so which key comes first does not matter.
        best_key, best_text = brute_force('123 !?')[0]
        self.assertEqual(best_text, '123 !?')


class BigramTableTest(unittest.TestCase):
    def test_has_every_letter_pair(self):
        # score() looks up every pair in this table. A missing pair would raise a KeyError.
        self.assertEqual(len(log_probabilities()), 26 * 26)

    def test_letters_only_drops_everything_else(self):
        self.assertEqual(letters_only('Hello, World 42!'), 'helloworld')


if __name__ == '__main__':
    unittest.main()