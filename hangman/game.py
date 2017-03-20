"""
Class for hangman games the the generator generates. Tracks
current word state, current letters guessed, target word, and
remaining guesses.
"""


class HangmanGame:
    def __init__(self, word, guesses):
        self.word = word
        self.guesses = guesses
        self.state = self.init_game_state()

    def init_game_state(self):
        return {'state': ['_'] * len(self.word), 'wrong': 0, 'guessed': set()}

    def reset_game_state(self):
        self.state = self.init_game_state()

    def process_letter_guess(self, letter):
        self.state['guessed'].add(letter)
        occurrences = [i for i, char in enumerate(self.word) if char == letter]
        for i in occurrences:
            self.state['state'][i] = letter
        self.state['wrong'] += 1 if len(occurrences) == 0 else 0

    def is_win(self):
        return ''.join(self.state['state']) == self.word and self.state['wrong'] < self.guesses

    def is_loss(self):
        return self.state['wrong'] >= self.guesses

    def game_over(self):
        return self.is_win() or self.is_loss()

    def check_for_win_status(self):
        if self.is_win():
            return ('You solved "{}" with {} guesses remaining.'.format(
                self.word,
                self.guesses - self.state['wrong']
            ))
        if self.is_loss():
            return ('You failed "{}" with {}.'.format(
                self.word,
                self.state['state']
            ))

    def print_game_state(self):
        print('--------------------------')
        print('Current state: {}'.format(self.state['state']))
        print('Guesses: {}'.format(', '.join(self.state['guessed'])))
        print('Guesses left: {}'.format(self.guesses - self.state['wrong']))
        print('--------------------------')

    def get_state(self):
        return {
            'state': ''.join(self.state['state']),
            'remaining': self.guesses - self.state['wrong'],
            'guessed': ', '.join(self.state['guessed']),
            'win': self.is_win()
        }

