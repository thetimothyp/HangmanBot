# HangmanBot
Challenge these bots in the classic game of hangman, or write your own bot to see how it measures up! (Don't worry, at least one of them is really dumb).

#### Play the game at: https://hangmanbot-app.herokuapp.com/
---------------------
HangmanBots is a side project intended to provide a sandbox for developing problem-solving heuristics 
for the classic game of hangman. While anyone can play the game, results and cumulative success rates
for various heuristics are displayed for each bot that tries to find the word of any given round of
hangman. 

## Creating a bot
Creating a hangman-solving bot is super easy to do. To write a bot, simply click the `Write a Bot` button and
define your `make_guess` method in the modal that pops up. All you have to do is make sure that the method returns
a single character value as its guess, and the game loop will take care of processing the guess for you.

For example, if we want to implement a bot that guesses a random letter every turn, we simply fill in the modal like so:
```javascript
/*
---------------------
DO NOT UNCOMMENT
---------------------
class CustomSolver extends Solver {
 
// Your make_guess() method should return a single letter guess.
// Feel free to define any helper methods you need to.

// Implement your make_guess method here
  make_guess(guessed, state, word_list) { 
*/
    
    // Implement helper methods if you need to
    function getRandomInt(min, max) {
      min = Math.ceil(min);
      max = Math.floor(max);
      return Math.floor(Math.random() * (max - min)) + min;
    }

    // Example: guess a random letter every time
    return 'abcdefghijklmnopqrstuvxyz'[getRandomInt(0, 26)];

/*
  } end make_guess
*/
```

### Current limitations
* If you look at the class declaration syntax, it's in JavaScript, not Python. This is done intentionally to avoid running user submitted code on the server (your code runs in your browser, so if you're trying to be malicious, the only person you can hurt is yourself). However, as a result, your bot's logic MUST be written in JavaScript for the time being. I'm looking into client-side interpreters for other languages, but execution speed is a definite issue here.
* Currently, you can only implement the make_guess() method of the CustomSolver class. The method has access to all the resources you'd need to develop an effective heuristic (AFAIK), and you can define any helper methods using those resources that you need inside the make_guess() method itself. HOWEVER, I realize that sometimes you'll want to have instance variables for your solver just to make your life easier. I'm working on redoing the code submission so that you can implement the whole CustomSolver class, rather than just a single method.

## Running the game locally
### Setting up your database (in server.py)
The game uses a small MongoDB database to track cumulative success rates for built-in heuristics. If you want to run the
game locally, you'll need to set up your own MongoDB instance to track your results. You can set up a local instance and connect
to that in `server.py`, or set up a cloud instance on a platform like [mLab](https://mlab.com/). You can read more about MongoDB [here](https://docs.mongodb.com/manual/introduction/).

After setting up your database, there are a few easy steps you need to take to prep your game for local play:
* In `static/index.js`, comment out `const socket = io.connect($(location).attr('href'));` and uncomment
`const socket = io.connect('http://127.0.0.1:5000');`. This prepares the client socket to connect with your
local machine.
* In the project root directory, start up your `virtualenv` and run `pip install -r requirements.txt`
* To run the server, run `python server.py`
* Navigate to `127.0.0.1:5000` to play

## Creating a local bot
Creating a hangman-solving bot happens in `hangman/solver.py`. If you want to make a bot,
it's as easy as defining a subclass of `HangmanSolver` and implementing the `make_guess(guessed, state)` method, 
where `guessed` is a list of letters that have already been guessed and `state` is the known domain of the word (e.g if 
"abc" is the target word, then `state == ['_', 'b', '_']` after guessing "b"). You can use this information when designing
your bot; additionally, if you want to process the entire dictionary of words to improve your heuristic, it can be accessed
in `self.word_list`.

For example, if we want to create a simple bot that will guess the letters from A to Z, we would define a class like the following:
```
class AtoZ(HangmanSolver):
  def __init__(self, word_list, word_length):
    super().__init__(word_list, word_length)
    
    # Create iterator from A to Z
    self.guesses = iter(string.ascii_lowercase)
  
  def make_guess(self, guessed, state):
    # Get the next letter from self.guesses
    guess = next(self.guesses)
    return guess
```
And that's it! Not exactly the smartest bot in the world, but it tries.

## Adding your bot to the runnable bots
Once you've made your bot, it's super simple to run it alongside the other
bots. Open `hangman/player.py`, and add your bot to `SOLVERS` constant, which
holds an iterator of all the bots to run. For our simple `AtoZ` bot, that means
we'd add `solver.AtoZ` to the iterator. Save your work, restart your server,
and you'll see the results of your bot alongside all the others when you finish
a round of hangman.
