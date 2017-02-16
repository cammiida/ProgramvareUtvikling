$(document).ready(function(){
	$("#button1").mouseover(function(){
	    $("#button1").css("opacity", "0.8");
	});
	$("#button1").mouseout(function(){
		$("#button1").css("opacity","0.3");
	});
	$("#button1").click(function(){
		var n = $("#textbox").val();
		if($(this).val() == "Trykk her")
			$(this).val("Ikke trykk her");
		else
			$(this).val("Trykk her") 
		//$("#button1").prop("value","ikke trykk her");
		$("#textbox2").prop("value",n);
	});
});
