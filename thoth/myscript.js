$(document).ready(function(){
	$("#down").mouseout(function(){
		$("#down").prop("src", "Ressurser/knapp_down.png");
	});
	$("#up").mouseout(function(){
		$("#up").prop("src", "Ressurser/knapp_up.png");
	});
	$("#up").mouseover(function(){
		$("#up").prop("src", "Ressurser/knapp_up(over).png");
	});
	$("#down").mouseover(function(){
		$("#down").prop("src", "Ressurser/knapp_Down(over).png")
	})
	$("#up").mousedown(function(){
		$("#up").prop("src","Ressurser/knapp_up(pressed).png");
	});
	$("#down").mousedown(function(){
		$("#down").prop("src","Ressurser/knapp_down(pressed).png");
	});
	$("#dropDownBtn").click(function(){
		$("#liste").toggle();
	})
	$("li").mouseover(function(){
		$(this).css("background-color", "#404040");
	});
	$("li").mouseout(function(){
		$(this).css("background-color","#808080")
	})
	$("li").mousedown(function(){
		$(this).css("box-shadow", "inset 1px 0px 7px 8px #202020")
	})
	$("li").mouseup(function(){
		$(this).css("box-shadow", "");
	})
	$("#button1").click(function(){
		var n = $("#textbox").val();
		if($(this).val() == "Trykk her")
			$(this).val("Ikke trykk her");
		else
			$(this).val("Trykk her")
		$("#textbox2").prop("value",n);
	});
});