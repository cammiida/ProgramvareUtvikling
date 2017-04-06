$(document).ready(function(){
	$("#dropDownBtn").click(function(){
		$("#liste").toggle();
	});

	$('#optionsfield').hide();
	$('#textanswerfield').hide();

	$('#toggleaddtask').click(function(){
		$('#addtask').slideToggle();
		console.log('clicks');
	});

	$('#addtextanswer').click(function(){
		$('#textanswerfield').slideToggle();
		$('#optionsfield').hide();
		console.log('clicks');
	});

	$('#addoptions').click(function(){
		$('#optionsfield').slideToggle();
		$('#textanswerfield').hide();
		console.log('clicks');
	});



});
