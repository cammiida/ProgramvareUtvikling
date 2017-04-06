/***************************************************
AT THIS TIME THE ONLY THING THIS DOES IS THE buttons
AND DISPLAYING THEM
***************************************************/


/***************************************************
            SHOWING AND HIDING TABS
***************************************************/
 function showfeedback(){
	$('#feedback').show();
 	$('#addquestion').hide();
 	$('#questionlist').hide();
  $('#loadabout').hide();
  if($(window).width() < 769)
    $('#liste').hide();
 }
 function showquestionlist(){
	$('#feedback').hide();
	$('#addquestion').show();
	$('#questionlist').show();
  $('#loadabout').hide();
  if($(window).width() < 769)
    $('#liste').hide();
 }
 function showabout(){
 $('#feedback').hide();
 $('#addquestion').hide();
 $('#questionlist').hide();
 $('#loadabout').show();
  if($(window).width() < 769)
    $('#liste').hide();
 }

 /***************************************************
              AJAX FUNCTIONS FOR VOTE up/down
 ***************************************************/
 function vote(type,url,questionid){
   data = {};
   data[type] = 'true';
   console.log(data);
   $.post(url,data)

   .done(function(data){
     $('#questionlist').load('/student/question_list/'+$('#lectureid').html()+'/');
   });

 }

 /***************************************************
              FROM THE WEB TO HANDLE COOKIES
 ***************************************************/
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

 /***************************************************
              FROM THE WEB TO HANDLE HTTP STUFF
 ***************************************************/
 function csrfSafeMethod(method) {
     // these HTTP methods do not require CSRF protection
     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
 }


 /***************************************************
              WHEN DOCUMENT IS ACTIVE
 ***************************************************/
$(document).ready(function(){

  /***************************************************
               LOADING AND HIDING LECTURE CONTENT
  ***************************************************/
  $('#questionlist').load('/student/question_list/'+$('#lectureid').html()+'/');
	$('#feedback').hide();
	$('#addquestion').hide();
	$('#questionlist').hide();
  $('#loadabout').hide();


  /***************************************************
          FROM THE WEB TO HANDLE COOKIE
  ***************************************************/
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
    });

    /***************************************************
              TO USE AJAX ON ADD QUESTIONFORM
    ***************************************************/
    $('#addquestionform').submit(function(event){
      //create dictionary
      var formData = {
        'question' : $('#id_question').val(),
      };

      var url = $('#addquestionform').attr('action');
      $.post(url,formData)
      // when this function has posted the question with ajax, we want to
      // reload the question div but not the page. That's why we use ajax.
      .done(function(data){
          $('#questionlist').load('/student/question_list/'+$('#lectureid').html()+'/');
      });
      //Stop the page from normally refreshing and disconnecting our students:
      event.preventDefault();
    });

});
