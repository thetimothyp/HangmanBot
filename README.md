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
