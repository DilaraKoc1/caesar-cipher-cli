"""Tests for main.py.

Run: python -m unittest -v
"""
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main


def run(argv, answers=()):
    """Run main() with the given command line and typed answers, return what it printed."""
    output = io.StringIO()
    with patch('sys.argv', argv), patch('builtins.input', side_effect=answers), redirect_stdout(output):
        main.main()
    return output.getvalue()


class InteractiveTest(unittest.TestCase):
    def test_encrypt(self):
        self.assertIn('Khoor Zruog', run(['main.py'], ['e', 'Hello World', '3']))

    def test_decrypt(self):
        self.assertIn('Hello World', run(['main.py'], ['d', 'Khoor Zruog', '3']))

    def test_brute_shows_best_guess(self):
        self.assertIn('key 3: Hello World', run(['main.py'], ['b', 'Khoor Zruog', 'n']))

    def test_brute_can_show_all_candidates(self):
        output = run(['main.py'], ['b', 'Khoor Zruog', 'y'])
        self.assertIn('14 Wtaad Ldgas', output)

    def test_asks_again_after_invalid_answers(self):
        output = run(['main.py'], ['x', 'e', '', 'Hello', 'three', '3'])
        self.assertIn('Please enter e, d or b.', output)
        self.assertIn('Please enter some text.', output)
        self.assertIn('Please enter a whole number', output)
        self.assertIn('Khoor', output)

    def test_ctrl_c_exits_quietly(self):
        # Raising means the test fails, so no assertion is needed beyond running it.
        run(['main.py'], KeyboardInterrupt())


class ArgumentModeTest(unittest.TestCase):
    def test_arguments_still_work(self):
        self.assertIn('key 3: Hello World', run(['main.py', 'brute', 'Khoor Zruog']))


if __name__ == '__main__':
    unittest.main()
