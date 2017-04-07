
function showhistory(url){
	$('#taskhistory').load(url);
};



$(document).ready(function(){
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
