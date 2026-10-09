# Student Name: Zain Ammar Afzal
# Student ID: 202673038


#gui part of game which is same as cli part but using tkinter for making it visually easy

import tkinter as tk #its used for making gui
from tkinter import messagebox #liberary for showing message box
import os  # liberary for os access like files 
from engine import GameEngine # its importing engine.py class which i defined for game logic and functionality

"files which have words for game and its deficulties "

WORD_FILES = {
    'Easy': 'easy.txt',
    'Medium': 'medium.txt',
    'Hard': 'hard.txt',
}

HISTORY_FILE = 'game_history.txt' # file to store game history

# this function  used to append game history to a file
def append_history(record: str):
    try:
        with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
            f.write(record + '\n')
    except Exception:
        pass

#  class is used for game gui
class WordGameGUI(tk.Tk):
    # this is constructor of class which is used to initialize the game gui and its components
    def __init__(self):
        super().__init__()
        self.title('Word Guessing Game, Guess the Word and win the game')
        self.geometry('600x400')
        self.engine = GameEngine()
        self.difficulty_var = tk.StringVar(value='Easy')
        self.create_widgets()

    # function is used to create game widgets ,buttons and labels for game gui
    def create_widgets(self):
        top = tk.Frame(self)
        top.pack(pady=8)
        tk.Label(top, text='Difficulty:').pack(side='left')
        tk.OptionMenu(top, self.difficulty_var, *WORD_FILES.keys()).pack(side='left')
        tk.Button(top, text='New Game', command=self.new_game).pack(side='left', padx=8)

        self.hint_label = tk.Label(self, text='Hint: -', font=('Arial', 12))
        self.hint_label.pack(pady=6)

        self.word_label = tk.Label(self, text='', font=('Consolas', 24))
        self.word_label.pack(pady=6)

        self.lives_label = tk.Label(self, text='Lives: 0', font=('Arial', 12))
        self.lives_label.pack(pady=4)

        self.score_label = tk.Label(self, text='Score: 0', font=('Arial', 12))
        self.score_label.pack(pady=4)

        self.keyboard_frame = tk.Frame(self)
        self.keyboard_frame.pack(pady=6)
        self.letter_buttons = {}

        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i, ch in enumerate(letters):
            btn = tk.Button(self.keyboard_frame, text=ch, width=4, command=lambda c=ch: self.on_letter(c))
            btn.grid(row=i//9, column=i%9, padx=2, pady=2)
            self.letter_buttons[ch] = btn

        self.new_game()
    #for start new game or reset game
    def new_game(self):
        diff = self.difficulty_var.get()
        fname = WORD_FILES.get(diff)
        if not fname or not os.path.exists(fname):
            messagebox.showerror('File missing', f'{fname} not found in folder')
            return
        pool = GameEngine.load_words_from_file(fname)
        self.engine.select_word(pool)
        for btn in self.letter_buttons.values():
            btn.config(state='normal')
        self.update_ui()

    # update game current state
    def update_ui(self):
        state = self.engine.get_state()
        self.word_label.config(text=state['display'])
        self.hint_label.config(text=f"Hint: {state['hint']}")
        self.lives_label.config(text=f"Lives: {state['remaining_lives']}/{state['max_lives']}")
        self.score_label.config(text=f"Score: {state['score']}")

    def on_letter(self, ch: str):
        btn = self.letter_buttons.get(ch)
        if btn:
            btn.config(state='disabled')
        result = self.engine.guess_letter(ch)
        if result.get('status') == 'invalid' or result.get('status') == 'repeat':
            # ignore
            pass
        self.update_ui()
        if result.get('status') == 'win':
            messagebox.showinfo('You won', f"You won congratulations!, Winner winner chicken dinner! The word was {self.engine.reveal_word()}. Score: {self.engine.score}")
            record = f"{self._timestamp()},{self.difficulty_var.get()},{self.engine.reveal_word()},WIN,0,0,{self.engine.score}"
            append_history(record)
            self.new_game()
        elif result.get('status') == 'lose':
            messagebox.showinfo('You lost', f"You lost better luck next time and try again. The word was {self.engine.reveal_word()}. Score: {self.engine.score}")
            record = f"{self._timestamp()},{self.difficulty_var.get()},{self.engine.reveal_word()},LOSS,0,0,{self.engine.score}"
            append_history(record)
            self.new_game()

    def _timestamp(self):
        import time
        return time.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    app = WordGameGUI()
    app.mainloop()
