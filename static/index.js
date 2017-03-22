$(function(){
	const socket = io.connect('http://127.0.0.1:5000');
	// const socket = io.connect($(location).attr('href'));

	let userBot;

	const display_word = (word) => {
		$("#play-field").text(word.split('').join(' '))
	}

	const update_guesses_remaining = (remaining) => {
		$("#guesses-remaining").text(remaining)
	}

	const update_guesses = (guesses) => {
		$("#guesses").text(guesses)
	}

	const prettyprint = (results) => {
		return results.join('<br/><br/>') + '<br/><br/>' + userBot;
	}

	const fade_loader = (dir) => {
		if (dir == 'in') {
			$(".loading").css({"border-color":"rgba(0, 0, 0, 0.2)", "border-top-color":"black"});
		} else {
			$(".loading").css({"border-color":"rgba(0, 0, 0, 0)", "border-top-color":"white"});
		}	
	}

	socket.on('message', (message) => {
		console.log(message);
	});

	socket.on('game_state', (state) => {
		state = JSON.parse(state)
		display_word(state['state'])
		update_guesses_remaining(state['remaining'])
		update_guesses(state['guessed'])
	})

	socket.on('win_status', (status) => {
		$("#win-status").text(status)
		$("#guess").prop("disabled", true)
	})

	socket.on('solver_results', (results) => {
		$("#solver-results").html(prettyprint(results))
	})

	socket.on('processed', (flag) => {
		fade_loader('out')
		$("#guess").prop("disabled", false)
	})

	socket.on('new_game', (data) => {
		data = JSON.parse(data);
		g = new Game(data['word'], data['max_guesses']);
		s = new CustomSolver(data['word_length'], data['word_list']);
		userBot = g.run_with_solver(s);
	})

	$("#play").on('click', () => {
		socket.emit('play_game', 'hi')
		$("#guess").prop("disabled", false)
	})

	$("#guess").on('click', () => {
		let letter_val = $("#letter").val().toLowerCase()
		$("#letter").val('')
		socket.emit('letter_guess', letter_val)
		fade_loader('in')
		$("#guess").prop("disabled", true)
	})

	$("#modal-btn").on('click', () => {
		$("#myModal").css('display', 'block');
	})

	$(".close").on('click', () => {
		$("#myModal").css('display', 'none');
	})

})