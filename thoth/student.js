$(document).ready(function(){
	/*Speed up and down buttons with animation*/
	var toSlow = 0;
	var toFast = 0;
	$("#down").mouseout(function(){
		$("#down").prop("src", "Ressurser/downbutton.png");
	});
	$("#up").mouseout(function(){
		$("#up").prop("src", "Ressurser/upbutton.png");
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
		$("#down").prop("src","Ressurser/downbutton.png");
	})
	$("#up").mouseup(function(){
		$("#up").prop("src","Ressurser/upbutton.png");
	})
/*Fade functionality and feedback from buttons.*/
	$("#down").click(function(){
		toFast += 1;
		$("#message").text("You pressed the too fast button")
		$("#toFast").text(toFast);
		$("#message").fadeIn("slow");
		setTimeout(function(){
			$("#message").fadeOut("slow");
		}
		,2000);
	});
	$("#up").click(function(){
		toSlow += 1;
		$("#message").text("You pressed the too slow button");
		$("#toSlow").text(toSlow);
		$("#message").fadeIn("slow");
		setTimeout(function(){
			$("#message").fadeOut("slow");
		},2000)
	});

});
