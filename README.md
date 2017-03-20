# HangmanBot
Challenge these bots in the classic game of hangman! (Don't worry, at least one of them is really dumb).

#### Play the game at: https://hangmanbot-app.herokuapp.com/
---------------------
HangmanBots is a side project intended to provide a sandbox for developing problem-solving heuristics 
for the classic game of hangman. While anyone can play the game, results and cumulative success rates
for various heuristics are displayed for each bot that tries to find the word of any given round of
hangman. 

## Running the game locally
In order to run the game locally, there are a couple easy steps you need to take:
* In `static/index.js`, comment out `const socket = io.connect($(location).attr('href'));` and uncomment
`const socket = io.connect('http://127.0.0.1:5000');`. This prepares the client socket to connect with your
local machine.
* In the project root directory, start up your `virtualenv` and run `pip install -r requirements.txt`
* To run the server, run `python server.py`
* Navigate to `127.0.0.1:5000` to play

## Creating a bot
Creating a hangman-solving bot happens in `hangman/solver.py`. If you want to make a bot,
it's as easy as defining a subclass of `HangmanSolver` and implementing the `make_guess()` method.
Every solver instance has a game attached to it, so you'll need to have the game process your guess
at the end of your `make_guess()` implementation. 

For example, if we want to create a simple bot that will guess the letters from A to Z, we would define a class like the following:
```
class AtoZ(HangmanSolver):
  def __init__(self, word_list, game):
    super().__init__(word_list, game)
    self.guesses = iter(string.ascii_lowercase)
  
  def make_guess(self):
    # Get the next letter from self.guesses
    guess = next(self.guesses)
    
    # Tell our game to process this guess
    self.game.process_letter_guess(guess)
```
And that's it! Not exactly the smartest bot in the world, but it tries.

## Adding your bot to the runnable bots
Once you've made your bot, it's super simple to run it alongside the other
bots. Open `hangman/player.py`, and add your bot to `SOLVERS` constant, which
holds an iterator of all the bots to run. For our simple `AtoZ` bot, that means
we'd add `solver.AtoZ` to the iterator. Save your work, restart your server,
and you'll see the results of your bot alongside all the others when you finish
a round of hangman.
