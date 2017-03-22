class Solver {
	constructor(word_length, word_list) {
		this.word_length = word_length;
		this.word_list = this.prune_word_list(word_list);
	}

	prune_word_list(word_list) {
		return word_list.filter((word) => word.length == this.word_length);
	}

	make_guess(guessed, state, word_list) {
		/* Implement in subclass */
	}
}

class CustomSolver extends Solver {
	/* 
		Your make_guess() method should return a single letter guess.
		Feel free to define any helper methods you need to.
	 */
	constructor(word_length, word_list) {
		super(word_length, word_list);
	}

	make_guess(guessed, state, word_list) {
		/* Implement your make_guess method here */
		return '_';
	}
}