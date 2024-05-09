localStorage.clear("score");

const $scoreValue = $("#score-value");
const $guessForm = $("#guess-form");
const $guessInput = $("#guess-input");
const $serverResponse = $(".server-response");
const $timeLeft = $("#time-left");

let totalScore = 0;
let timeLeft = 60;
let timerStarted = false;
let timer;

function startTimer() {
	timer = setInterval(() => {
		timerStarted = true;
		timeLeft--;
		$timeLeft.text(timeLeft);
		if (timeLeft === 0) {
			clearInterval(timer);
			sendScoreToServer(totalScore);
			window.location.href = "/game-over";
		}
	}, 1000);
}

// Display the initial score and time left
$scoreValue.text(totalScore);
$timeLeft.text(timeLeft);

$guessForm.submit(function (e) {
	e.preventDefault();
	let formData = { guess: $guessInput.val() };

	axios
		.post("/submit_guess", formData)
		.then(function (response) {
			const result = response.data.result;
			const newScore = parseInt(response.data.score);
			console.log(newScore);
			$serverResponse.text(result);
			totalScore = newScore;
			$scoreValue.text(totalScore);
			$guessInput.val("");
			// update score in localStorage
			localStorage.setItem("score", totalScore);
			console.log(response.data);

			if (!timerStarted && result === "ok") {
				startTimer();
			}
		})
		.catch(function (error) {
			console.error("Error:", error);
		});
});

function sendScoreToServer(score) {
	console.log(totalScore);

	axios
		.post(
			"/game-over",
			{ score: score },
			{
				headers: {
					"Content-Type": "application/json",
				},
			}
		)
		.then(function (response) {
			window.location.href = "/game-over";
		})
		.catch(function (error) {
			console.error("Error:", error);
		});
}
