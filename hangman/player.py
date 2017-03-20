from hangman import generator, solver
import collections


SOLVERS = (
    solver.ProbabilityBruteForceFrequencies,
    solver.BruteForceFrequencies,
    solver.ProbabilityPatternMatching,
    solver.PatternMatching,
)


class HangmanPlayer:
    def __init__(self):
        self.g = generator.HangmanGenerator("words.txt")
        self.game_generator = self.g.get_games()
        self.game = next(self.game_generator)

    def run(self):
        self.reset_game()
        while not self.game.game_over():
            self.game.print_game_state()
            guess = input('Guess a letter: ')
            self.game.process_letter_guess(guess)
        return self.game.check_for_win_status()

    def run_solvers(self, solvers=SOLVERS):
        return [self.run_with_solver(s) for s in solvers]

    def run_with_solver(self, solver_class):
        s = solver_class(self.g.words, len(self.game.word))
        self.reset_game()
        while not self.game.game_over():
            guessed = self.game.state['guessed']
            state = self.game.state['state']
            guess = s.make_guess(guessed, state)
            self.game.process_letter_guess(guess)
        return solver_class, self.game.get_state()

    def report_solver_results(self, solver_class, result):
        if result['win']:
            return('Solver ({}) solved "{}" with {} guesses remaining.'.format(
                solver_class.__name__,
                self.game.word,
                result['remaining']
            ))
        else:
            return('Solver ({}) failed "{}" with "{}".'.format(
                solver_class.__name__,
                self.game.word,
                result['state']
            ))

    def test_solver(self, solver_class, n=10):
        wins = losses = 0
        for _ in range(n):
            self.start_new_game()
            s = solver_class(self.g.words, self.game)
            while not self.game.game_over():
                s.make_guess()
            if self.game.is_win():
                wins += 1
            else:
                losses += 1
        return (wins, losses, wins / (wins + losses))

    def start_new_game(self):
        self.game = next(self.game_generator)

    def reset_game(self):
        self.game.reset_game_state()


if __name__ == "__main__":
    player = HangmanPlayer()
    player.run()
    results = player.run_solvers()
    for s, r in results:
        print(player.report_solver_results(s, r))
