"""
A hangman puzzle generator. Reads in a list of words from
a file and generates hangman games by picking a random word
from the list.
"""
import random
from hangman import game


class HangmanGenerator:
    def __init__(self, filename):
        self.words = self.get_word_list(filename)

    def get_games(self, max_guesses=8):
        while True:
            yield game.HangmanGame(self.pick_random_word(), max_guesses)

    @staticmethod
    def get_word_list(filename):
        with open(filename) as file:
            words = file.readlines()
        return [word.strip() for word in words if len(word.strip()) > 3 and word.strip().isalpha()]

    def pick_random_word(self):
        return self.words[random.randrange(len(self.words))]