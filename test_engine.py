# Student Name: Zain Ammar Afzal
# Student ID: 202673038
# Unit tests for engine.py. Run with: python -m unittest -v test_engine

import os
import tempfile
import unittest

from engine import GameEngine


class TestGameEngine(unittest.TestCase):

    def setUp(self):
        self.engine = GameEngine()
        self.engine.start_new_game('apple', 'A fruit')

    def test_word_is_uppercased_and_hidden(self):
        self.assertEqual(self.engine.secret_word, 'APPLE')
        self.assertEqual(self.engine.get_display(), '_ _ _ _ _')

    def test_correct_guess_reveals_every_match_and_scores(self):
        result = self.engine.guess_letter('p')
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(self.engine.get_display(), '_ P P _ _')
        self.assertEqual(self.engine.score, 20)

    def test_wrong_guess_costs_a_life_and_points(self):
        self.engine.guess_letter('p')
        result = self.engine.guess_letter('z')
        self.assertEqual(result['message'], 'Incorrect')
        self.assertEqual(self.engine.remaining_lives, 5)
        self.assertEqual(self.engine.score, 15)

    def test_score_never_goes_below_zero(self):
        self.engine.guess_letter('z')
        self.assertEqual(self.engine.score, 0)

    def test_repeat_guess_changes_nothing(self):
        self.engine.guess_letter('z')
        result = self.engine.guess_letter('Z')
        self.assertEqual(result['status'], 'repeat')
        self.assertEqual(self.engine.remaining_lives, 5)

    def test_invalid_input_is_rejected(self):
        for bad in ['', '12', '5', '!', 'ab']:
            self.assertEqual(self.engine.guess_letter(bad)['status'], 'invalid')
        self.assertEqual(self.engine.remaining_lives, 6)

    def test_win_when_all_letters_found(self):
        result = None
        for ch in 'APLE':
            result = self.engine.guess_letter(ch)
        self.assertEqual(result['status'], 'win')
        self.assertTrue(self.engine.is_won())

    def test_loss_after_six_wrong_guesses(self):
        result = None
        for ch in 'ZXQWJK':
            result = self.engine.guess_letter(ch)
        self.assertEqual(result['status'], 'lose')
        self.assertTrue(self.engine.is_lost())

    def test_guess_without_active_game(self):
        self.assertEqual(GameEngine().guess_letter('a')['status'], 'invalid')

    def test_select_word_uses_the_pool(self):
        self.engine.select_word([('dog', 'Pet')])
        self.assertEqual(self.engine.secret_word, 'DOG')

    def test_empty_pool_raises(self):
        with self.assertRaises(ValueError):
            self.engine.select_word([])

    def test_load_words_skips_bad_lines(self):
        with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write('cat|A pet\n\nno delimiter here\nsun | A star\n')
            path = f.name
        try:
            self.assertEqual(GameEngine.load_words_from_file(path),
                             [('CAT', 'A pet'), ('SUN', 'A star')])
        finally:
            os.remove(path)

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            GameEngine.load_words_from_file('does_not_exist.txt')


if __name__ == '__main__':
    unittest.main()
