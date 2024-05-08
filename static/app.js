$(document).ready(function () {
	$("#guess-form").submit(function (e) {
		e.preventDefault();
		const formData = { guess: $("#guess-input").val() };
		axios
			.post("/submit_guess", formData)
			.then(function (response) {
				const result = response.data.result;
				$(".server-response").text(result);
				console.log(response.data);
			})
			.catch(function (error) {
				console.error("Error:", error);
			});
	});
});
