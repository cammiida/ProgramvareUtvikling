

function showhistory(url){


	$('#taskhistory').load(url,function(){
		// Collects the total number of students of each type
		var corran = $('#corran').text();
		var worngan = $('#worngan').text(); //typo, but afraid to not find everything to change
		var timeoan = $('#timeoan').text();
		// Turns strings into numbers
		corran = parseInt(corran);
		worngan = parseInt(worngan);
		timeoan = parseInt(timeoan);
		// Total number of students
		var totalnr = (corran+worngan+timeoan);
		// Calculates percentages
		var tcorpros = (corran/totalnr)*100;
		var twropros = (worngan/totalnr)*100;
		var tiompros = (timeoan/totalnr)*100;
		// Logs to see it works
		console.log('corr answers '+corran);
		console.log('wrong answers  '+worngan);
		console.log('timed out  answers '+timeoan);
		console.log('tot '+totalnr);
		console.log('% '+tcorpros);
		console.log('% '+twropros);
		console.log('% '+tiompros);

		// Creates the graph:
		$('#correctanswers').css('height',tcorpros);
		$('#wronganswers').css('height',twropros);
		$('#timedoutanswers').css('height',tiompros);
	});
};


$(document).ready(function(){

	$('#detailsbutton').click(function(){
		$('#detailsbox').toggle();
	});


	$('#taskhistory').click(function(){
		$('#taskhistory').hide();
	})

	$('.addquestion').click(function(){
		$('#taskhistory').show();
	})


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
