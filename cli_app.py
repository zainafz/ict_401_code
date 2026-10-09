# Student Name: Zain Ammar Afzal
# Student ID: 202673038

# THE TERMINAL BASED GUSSING GAME
import os
import time # liberrary for time parts
from engine import GameEngine # its importing class from custom engine.py

WORD_FILES = {
    '1': ('Easy', 'easy.txt'),
    '2': ('Medium', 'medium.txt'),
    '3': ('Hard', 'hard.txt'),
}

HISTORY_FILE = 'game_history.txt'


def append_history(record: str):
    try:
        with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
            f.write(record + '\n')
    except Exception as e:
        print('Warning: could not write history:', e)


def choose_difficulty():
    print('Choose difficulty level and check your skills:')
    for k, (name, fname) in WORD_FILES.items():
        print(f'{k}) {name} ({fname})')
    choice = input('Enter 1/2/3: ').strip()
    return choice if choice in WORD_FILES else None


def load_pool_for_choice(choice: str):
    _, fname = WORD_FILES[choice]
    if not os.path.exists(fname):
        raise FileNotFoundError(f'{fname} not found')
    return GameEngine.load_words_from_file(fname)


def main():
    print('Word Guessing Game - CLI Version')
    while True:
        choice = choose_difficulty()
        if not choice:
            print('Invalid choice. Try again.')
            continue
        try:
            pool = load_pool_for_choice(choice)
        except FileNotFoundError:
            print('Word file missing. Please ensure the file exists in this folder.')
            continue
        engine = GameEngine()
        engine.select_word(pool)
        start_time = time.time()
        guesses = 0
        print('\nGame started! guess the word and win the game')
        print('Hint:', engine.hint)
        while True:
            print('\nWord:', engine.get_display())
            print('Guessed:', ', '.join(sorted(engine.guessed_letters)))
            print(f'Remaining lives: {engine.remaining_lives}')
            print(f'Score: {engine.score}')
            s = input('Enter a letter (or QUIT): ').strip()
            if not s:
                print('Please enter a letter.')
                continue
            if s.upper() == 'QUIT':
                print('Exiting current game.')
                break
            result = engine.guess_letter(s)
            if result.get('status') == 'invalid':
                print('Invalid input:', result.get('message'))
                continue
            if result.get('status') == 'repeat':
                print(result.get('message'))
                continue
            guesses += 1
            if result.get('status') == 'ok':
                print(result.get('message'))
                continue
            if result.get('status') == 'win':
                print('\nYou won! Congratulations! Winner winner chicken dinner! The word was:', engine.reveal_word())
                print('Final score:', engine.score)
                duration = int(time.time() - start_time)
                record = f"{time.strftime('%Y-%m-%d %H:%M:%S')},{WORD_FILES[choice][0]},{engine.reveal_word()},WIN,{guesses},{duration},{engine.score}"
                append_history(record)
                break
            if result.get('status') == 'lose':
                print('\nYou lost. but you can do it again! The word was:', engine.reveal_word())
                print('Final score:', engine.score)
                duration = int(time.time() - start_time)
                record = f"{time.strftime('%Y-%m-%d %H:%M:%S')},{WORD_FILES[choice][0]},{engine.reveal_word()},LOSS,{guesses},{duration},{engine.score}"
                append_history(record)
                break
        again = input('\nPlay again? (y/n): ').strip().lower()
        if again != 'y':
            print('Goodbye!')
            break


if __name__ == '__main__':
    main()
