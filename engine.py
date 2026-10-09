# Student Name: Zain Ammar Afzal
# Student ID: 202673038


#Main game engine which hundle all game logic and state management.

import random   # for random works selection

from typing import List, Tuple, Optional # for type hinting

# CLASS WHICH IS GAME MIND  
class GameEngine:

    # constructor for initialize the game engine with default values for secret word, hint, guessed letters, remaining lives, and display state.
    def __init__(self):
        self.secret_word: Optional[str] = None
        self.hint: Optional[str] = None
        self.guessed_letters: set[str] = set()
        self.remaining_lives: int = 6
        self._display: List[str] = []
        self.max_lives: int = 6
        self.score: int = 0

    @staticmethod
    def load_words_from_file(path: str) -> List[Tuple[str, str]]:
        words = []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or '|' not in line:
                        continue
                    word, hint = line.split('|', 1)
                    word = word.strip()
                    hint = hint.strip()
                    if word:
                        words.append((word.upper(), hint))
        except FileNotFoundError:
            raise
        return words

    # select a word from the given pool and start a new game.
    def select_word(self, word_pool: List[Tuple[str, str]]):
        if not word_pool:
            raise ValueError('Empty word pool')
        word, hint = random.choice(word_pool)
        self.start_new_game(word, hint)
    # start a new game with the given word, hint, and number of lives.
    def start_new_game(self, word: str, hint: str, lives: int = 6):

        self.secret_word = word.upper()
        self.hint = hint
        self.guessed_letters = set()
        self.remaining_lives = lives
        
        self.max_lives = lives
        self.score = 0
        self._display = [c if not c.isalpha() else '_' for c in self.secret_word]

    def get_display(self) -> str:
        return ' '.join(self._display)

    def is_won(self) -> bool:
        return self.secret_word is not None and all(
            (self._display[i] == self.secret_word[i]) or not self.secret_word[i].isalpha()
            for i in range(len(self.secret_word))
        )

    def is_lost(self) -> bool:
        return self.remaining_lives <= 0 and not self.is_won()

    def reveal_word(self) -> str:
        return self.secret_word or ''

    def validate_input(self, letter: str) -> Tuple[bool, str]:

        if not letter or len(letter) != 1:
            return False, 'Enter a single letter.'
        if not letter.isalpha():
            return False, 'Only letters are allowed.'
        return True, ''

    def guess_letter(self, letter: str) -> dict:
        if self.secret_word is None:
            return {'status': 'invalid', 'message': 'No active game.'}

        letter = letter.upper()
        valid, msg = self.validate_input(letter)
        if not valid:
            return {'status': 'invalid', 'message': msg}

        if letter in self.guessed_letters:
            return {'status': 'repeat', 'message': f'You already guessed {letter}.', 'display': self.get_display(), 'remaining_lives': self.remaining_lives}

        self.guessed_letters.add(letter)

        if letter in self.secret_word:
            matches = 0
            for i, ch in enumerate(self.secret_word):
                if ch == letter:
                    self._display[i] = letter
                    matches += 1
            self.score += matches * 10
            if self.is_won():
                return {'status': 'win', 'message': 'You won!', 'display': self.get_display(), 'remaining_lives': self.remaining_lives}
            return {'status': 'ok', 'message': 'Correct', 'display': self.get_display(), 'remaining_lives': self.remaining_lives}
        else:
            self.remaining_lives -= 1
            self.score = max(0, self.score - 5)
            if self.is_lost():
                return {'status': 'lose', 'message': 'No lives left', 'display': self.get_display(), 'remaining_lives': self.remaining_lives}
            return {'status': 'ok', 'message': 'Incorrect', 'display': self.get_display(), 'remaining_lives': self.remaining_lives}

    def get_state(self) -> dict:
        return {
            'display': self.get_display(),
            'hint': self.hint,
            'guessed': sorted(list(self.guessed_letters)),
            'remaining_lives': self.remaining_lives,
            'max_lives': self.max_lives,
            'score': self.score,
            'secret_word': self.secret_word,
        }
