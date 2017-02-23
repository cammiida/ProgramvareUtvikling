$(document).ready(function(){
	/*Speed up and down buttons with animation*/
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
	$("#down").mouseup(function(){
		$("#down").prop("src","Ressurser/knapp_down.png");
	})
	$("#up").mouseup(function(){
		$("#up").prop("src","Ressurser/knapp_up.png");
	})
	/*Drop Down Menu functionality with button animation*/
	$("#dropDownBtn").click(function(){
		$("#liste").toggle();
	})
	$("li").mouseover(function(){
		$(this).css("background-color", "#c4c4c4");
	});
	$("li").mouseout(function(){
		$(this).css("background-color","#e4e4e4")
	})
	$("li").mousedown(function(){
		$(this).css("box-shadow", "inset 1px 0px 7px 8px #8c8c8c")
	})
	$("li").mouseup(function(){
		$(this).css("box-shadow", "");
	})
/*Fade functionality and feedback from buttons.*/
	$("#down").click(function(){
		$("#message").text("You pressed the to fast button")
		$("#message").fadeIn("slow");
		setTimeout(function(){
			$("#message").fadeOut("slow");
		}
		,2000);
	});
	$("#up").click(function(){
		$("#message").text("You pressed the to slow button");
		$("#message").fadeIn("slow");
		setTimeout(function(){
			$("#message").fadeOut("slow");
		},2000)
	});
	
});