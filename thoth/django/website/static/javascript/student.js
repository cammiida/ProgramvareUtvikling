/* 
**************************************************
AT THIS TIME THE ONLY THING THIS DOES IS THE buttons
AND DISPLAYING THEM
**************************************************
*/

 function showfeedback(){
	$('#feedback').show();
 	$('#addquestion').hide();
 	$('#questionlist').hide();
  if($(window).width() < 769)
    $('#liste').hide();
 }
 function showaddquestion(){
	$('#feedback').hide();
	$('#addquestion').show();
	$('#questionlist').hide();
  if($(window).width() < 769)
    $('#liste').hide();
 }
 function showquestionlist(){
	$('#feedback').hide();
	$('#addquestion').hide();
	$('#questionlist').show();
  if($(window).width() < 769)
    $('#liste').hide();
 }

$(document).ready(function(){

	$('#feedback').hide();
	$('#addquestion').hide();
	$('#questionlist').hide();
});
