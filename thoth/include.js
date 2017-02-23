$(function () {
  $("#includedHeader").load("header.html", function() {
	  	$("#dropDownBtn").click(function(){
	  		$("#liste").toggle();
	  	});
	});
});
