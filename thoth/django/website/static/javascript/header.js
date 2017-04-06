$(document).ready(function(){
	$("#dropDownBtn").click(function(){
		$("#liste").toggle();
	});


	$('#toggleaddtask').click(function(){
		$('#addtask').slideToggle();
		console.log('clicks');
	});

});
