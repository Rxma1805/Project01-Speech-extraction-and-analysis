$(document).ready(function() {



	$('#btn2').click(function() {
		var input_message = $("#nameInput").val();

		$.post("/process",{"name": input_message}, function (data, status) {
			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#successAlert').text(data.name).show();
				$('#errorAlert').hide();
			}
			});
	});

	$('#btn3').click(function() {
		var input_message = $("#nameInput").val();

		$.post("/process2",{"name": input_message}, function (data, status) {
			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#successAlert').text(data.name).show();
				$('#errorAlert').hide();
			}
			});
	});


});