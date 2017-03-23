class Game {
	constructor(word, max_guesses) {
		this.word = word;
		this.max_guesses = max_guesses;
		this.state = this.init_game_state();
	}

	init_game_state() {
		return {
			word_state: Array(this.word.length).fill('_'),
			remaining: this.max_guesses,
			guessed: new Set(),
			status: null
		}
	}

	guess(letter) {
		this.state.guessed.add(letter);
		this.state.word_state = this.word.split('')
			.map((x, i) => x == letter || this.state.word_state[i] != '_' ? x : '_');
		this.state.remaining -= this.word.includes(letter) ? 0 : 1;
	}

	is_win() {
		return this.word == this.state.word_state.join('') && this.state.remaining > 0;
	}

	is_loss() {
		return this.state.remaining <= 0;
	}

	game_over() {
		if (this.is_win()) { this.state.status = 'win' }
		if (this.is_loss()) { this.state.status = 'loss' }
		return this.is_win() || this.is_loss();
	}

	run_with_solver(s, word_list) {
		while (!this.game_over()) {
			this.guess(s.make_guess(this.state.guessed, this.state));
		}
		return this.results;
	}

	get results() {
		if (this.state.status == 'win') {
			return 'Your bot solved "' + this.word + '" with ' 
				+ this.state.remaining + ' guesses remaining.';
		} else {
			return 'Your bot failed "' + this.word + '" with "' 
				+ this.state.word_state.join('') + '".';
		}
	}
}