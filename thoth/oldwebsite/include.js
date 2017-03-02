$(function () {
  $("#includedHeader").load("header.html", function() {
	  	$("#dropDownBtn").click(function(){
	  		$("#liste").toggle();
			});
			$("li").mouseover(function(){
				$(this).css("background-color", "#c4c4c4");
			});
			$("li").mouseout(function(){
				$(this).css("background-color","#e4e4e4");
			});
			$("li").mousedown(function(){
				$(this).css("box-shadow", "inset 1px 0px 7px 8px #8c8c8c");
			});
			$("li").mouseup(function(){
				$(this).css("box-shadow", "");
			});
	});
	var toSlow = 0;
	var toFast = 0;
	$("#up").click(function(){
		toSlow += 1;
		$("#slow_value").text(toSlow);
	});
	$("#down").click(function(){
		toFast += 1;
		$("#fast_value").text(toFast);
	});
});
