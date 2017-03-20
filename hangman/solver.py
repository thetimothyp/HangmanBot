import collections, re, random, bisect
from hangman import generator


class HangmanSolver:
    def __init__(self, word_list, game):
        self.word_length = len(game.word)
        self.word_list = self.prune_word_list(word_list)
        self.game = game

    def prune_word_list(self, word_list):
        return [word for word in word_list if len(word) == self.word_length]

    def make_guess(self):
        raise NotImplementedError("This method is not implemented")


class ProbabilityBruteForceFrequencies(HangmanSolver):
    """
    Tries the k most frequent characters for
    words of length n.
    """
    def __init__(self, word_list, game):
        super().__init__(word_list, game)
        self.freq = self.get_frequencies()

    def make_guess(self):
        guess = self.weighted_choice(self.freq)
        while guess in self.game.state['guessed']:
            guess = self.weighted_choice(self.freq)
        self.game.process_letter_guess(guess)

    def get_frequencies(self):
        freq = collections.defaultdict(int)
        for word in self.word_list:
            for c in set(word):
                freq[c] += 1
        return freq.items()

    def weighted_choice(self, choices):
        values, weights = zip(*choices)
        total = 0
        cum_weights = []
        for w in weights:
            total += w
            cum_weights.append(total)
        x = random.random() * total
        i = bisect.bisect(cum_weights, x)
        return values[i]


class BruteForceFrequencies(HangmanSolver):
    """
    Tries the most probable letters for
    a word of length n, weighted by frequency
    """
    def __init__(self, word_list, game):
        super().__init__(word_list, game)
        self.freq = self.get_frequencies()

    def make_guess(self):
        guess = self.get_max()
        while guess in self.game.state['guessed']:
            guess = self.get_max()
        self.game.process_letter_guess(guess)

    def get_frequencies(self):
        freq = collections.defaultdict(int)
        for word in self.word_list:
            for c in set(word):
                freq[c] += 1
        return (c for c, cnt in sorted(freq.items(), key=lambda x: x[1], reverse=True))

    def get_max(self):
        return next(self.freq)


class ProbabilityPatternMatching(HangmanSolver):
    """
    Tries the most probable characters for
    words that match current pattern, weighted
    by frequency. E.g if current word is "__AT_",
    we try the k most frequent characters out of
    the words that match r'..AT.'
    """
    def __init__(self, word_list, game):
        super().__init__(word_list, game)
        self.freq = self.get_frequencies()

    def make_guess(self):
        self.update_frequencies()
        guess = self.weighted_choice(self.freq)
        while guess in self.game.state['guessed']:
            guess = self.weighted_choice(self.freq)
        self.game.process_letter_guess(guess)

    def update_frequencies(self):
        cur = ''.join(self.game.state['state'])
        pattern = ''.join([c if c.isalpha() else '.' for c in cur])
        self.word_list = [word for word in self.word_list if re.match(pattern, word)]
        self.freq = self.get_frequencies()

    def get_frequencies(self):
        freq = collections.defaultdict(int)
        for word in self.word_list:
            for c in set(word):
                freq[c] += 1
        return freq.items()

    def weighted_choice(self, choices):
        values, weights = zip(*choices)
        total = 0
        cum_weights = []
        for w in weights:
            total += w
            cum_weights.append(total)
        x = random.random() * total
        i = bisect.bisect(cum_weights, x)
        return values[i]


class PatternMatching(HangmanSolver):
    """
    Tries k most frequent characters for
    words that match current pattern. E.g
    if current word is "__AT_", we try
    the k most frequent characters out of
    the words that match r'..AT.'
    """
    def __init__(self, word_list, game):
        super().__init__(word_list, game)
        self.freq = self.get_frequencies()

    def make_guess(self):
        self.update_frequencies()
        guess = self.get_max()
        while guess in self.game.state['guessed']:
            guess = self.get_max()
        self.game.process_letter_guess(guess)

    def update_frequencies(self):
        cur = ''.join(self.game.state['state'])
        pattern = ''.join([c if c.isalpha() else '.' for c in cur])
        self.word_list = [word for word in self.word_list if re.match(pattern, word)]
        self.freq = self.get_frequencies()

    def get_frequencies(self):
        freq = collections.defaultdict(int)
        for word in self.word_list:
            for c in set(word):
                freq[c] += 1
        return (c for c, cnt in sorted(freq.items(), key=lambda x: x[1], reverse=True))

    def get_max(self):
        return next(self.freq)


