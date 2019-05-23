$(document).ready(function() {
	$("#btn1").on('submit', function() {

		$.ajax({
			data : {
				name : $("#nameInput").val(),
			},
			type: 'POST',
			url: '/database',
			success: function (data) {

				if (data.error) {
					$('#errorAlert').text(data.error).show();
					$('#successAlert').hide();
				} else {
					$("#nameInput").attr("value", data.news)
				}

			},

		});
	});

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				name : $("#nameInput").val(),
			},
			type : 'POST',
			url : '/process'
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#successAlert').text(data.name).show();
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});

});