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
 function showquestionlist(){
	$('#feedback').hide();
	$('#addquestion').show();
	$('#questionlist').show();
  if($(window).width() < 769)
    $('#liste').hide();
 }

 function vote(type,url,questionid){
   data = {};
   data[type] = 'true';
   console.log(data);
   $.post(url,data);

   if(type == 'up_button'){
     $('#questionvalue_'+questionid).html(parseInt($('#questionvalue_'+questionid).html())+1);
   }
   else{
     $('#questionvalue_'+questionid).html(parseInt($('#questionvalue_'+questionid).html())-1);
   }

 }

  // DJANGOSTUFFS - SAFETY THINGS COPIED FROM THE WEB
 function getCookie(name) {
     var cookieValue = null;
     if (document.cookie && document.cookie != '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
             var cookie = jQuery.trim(cookies[i]);
             // Does this cookie string begin with the name we want?
             if (cookie.substring(0, name.length + 1) == (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
 }

 function csrfSafeMethod(method) {
     // these HTTP methods do not require CSRF protection
     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
 }


$(document).ready(function(){

	$('#feedback').hide();
	$('#addquestion').hide();
	$('#questionlist').hide();
  // This is required due to djangos CSRF protection
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
});
});
