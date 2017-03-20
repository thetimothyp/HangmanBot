import player, solver


def test_solvers():
    p = player.HangmanPlayer()
    solvers = (
        solver.ProbabilityBruteForceFrequencies,
        solver.BruteForceFrequencies,
        solver.ProbabilityPatternMatching,
        solver.PatternMatching)
    print("{:<8}{:<8}{:<8}".format("Wins", "Losses", "Success"))
    for s in solvers:
        print("{:<8}{:<8}{:0<8}".format(*p.test_solver(s, 500)))


if __name__ == "__main__":
    test_solvers()