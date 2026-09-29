"""Tests for main.py.

Run: python -m unittest -v
"""
import ast
import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

import main


def run(argv, answers=()):
    """Run main() with the given command line and typed answers, return what it printed."""
    output = io.StringIO()
    with patch('sys.argv', argv), patch('builtins.input', side_effect=answers), \
            redirect_stdout(output), redirect_stderr(io.StringIO()):
        main.main()
    return output.getvalue()


class PrepareTest(unittest.TestCase):
    def test_keeps_only_capital_letters(self):
        self.assertEqual(main.prepare('Attack at dawn, 5 a.m.!'), 'ATTACKATDAWNAM')


class InteractiveTest(unittest.TestCase):
    def test_encrypt(self):
        self.assertIn('KHOORZRUOG', run(['main.py'], ['c', 'e', 'Hello World', '3']))

    def test_decrypt(self):
        self.assertIn('Hello World', run(['main.py'], ['c', 'd', 'Khoor Zruog', '3']))

    def test_brute_shows_best_guess(self):
        self.assertIn('key 3: Hello World', run(['main.py'], ['c', 'b', 'Khoor Zruog', 'n']))

    def test_brute_can_show_all_candidates(self):
        output = run(['main.py'], ['c', 'b', 'Khoor Zruog', 'y'])
        self.assertIn('14 Wtaad Ldgas', output)

    def test_asks_again_after_invalid_answers(self):
        output = run(['main.py'], ['x', 'c', 'x', 'e', '', 'Hello', 'three', '3'])
        self.assertIn('Please enter c or v.', output)
        self.assertIn('Please enter e, d or b.', output)
        self.assertIn('Please enter some text.', output)
        self.assertIn('Please enter a whole number', output)
        self.assertIn('KHOOR', output)

    def test_encrypt_without_letters(self):
        self.assertIn('Nothing to encrypt', run(['main.py'], ['c', 'e', '123 !?', '3']))

    def test_vigenere_encrypt(self):
        output = run(['main.py'], ['v', 'e', 'Attack at dawn!', 'LEMON'])
        self.assertIn('LXFOPVEFRNHR', output)
        # The prepared plaintext is only used internally and must not be shown.
        self.assertNotIn('ATTACKATDAWN', output)

    def test_decrypt_keeps_the_format_it_gets(self):
        self.assertIn('ATTAC KATDA WN', run(['main.py'], ['v', 'd', 'LXFOP VEFRN HR', 'LEMON']))

    def test_vigenere_asks_again_for_invalid_keyword(self):
        output = run(['main.py'], ['v', 'e', 'Attack at dawn!', 'lem0n', 'LEMON'])
        self.assertIn('Please enter a keyword made of the letters A to Z.', output)
        self.assertIn('LXFOPVEFRNHR', output)

    def test_vigenere_does_not_offer_brute_yet(self):
        output = run(['main.py'], ['v', 'b', 'd', 'LXFOPVEFRNHR', 'LEMON'])
        self.assertIn('Please enter e or d.', output)
        self.assertIn('ATTACKATDAWN', output)

    def test_ctrl_c_exits_quietly(self):
        # Raising means the test fails, so no assertion is needed beyond running it.
        run(['main.py'], KeyboardInterrupt())


class ArgumentModeTest(unittest.TestCase):
    def test_arguments_still_work(self):
        self.assertIn('key 3: Hello World', run(['main.py', 'brute', 'Khoor Zruog']))

    def test_vigenere_arguments(self):
        output = run(['main.py', 'encrypt', 'Attack at dawn!', '--cipher', 'vigenere', '--key', 'LEMON'])
        self.assertIn('LXFOPVEFRNHR', output)

    def test_caesar_key_must_be_a_number(self):
        with self.assertRaises(SystemExit):
            run(['main.py', 'encrypt', 'Hello', '--key', 'LEMON'])

    def test_brute_is_not_available_for_vigenere_yet(self):
        with self.assertRaises(SystemExit):
            run(['main.py', 'brute', 'LXFOPVEFRNHR', '--cipher', 'vigenere'])


class OutputTextTest(unittest.TestCase):
    def test_strings_are_ascii(self):
        # Windows terminals can show characters such as the è in Vigenère wrongly, so every
        # string main.py can print must be plain ASCII. Docstrings are never printed.
        tree = ast.parse(Path(main.__file__).read_text(encoding='utf-8'))
        docstrings = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.FunctionDef)) and ast.get_docstring(node):
                docstrings.add(id(node.body[0].value))
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstrings:
                with self.subTest(text=node.value):
                    self.assertTrue(node.value.isascii())


if __name__ == '__main__':
    unittest.main()
