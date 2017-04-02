/*
**************************************************
ALL THE REAL-TIME AND SOCKET/NODE-PARTS USED BY
THE STUDENTS. MOVED OUT OF STUDENT.JS TO SEPARATE
REALTIME FROM INACTIVE STUFFS
**************************************************
*/



/******************************************************
                      ALIDATE TASK
******************************************************/
function submittaskanswer(correctanswer,taskid){
  if($('#textanswer_'+taskid).val().toLowerCase() == correctanswer.toLowerCase()){
    alert('YOU ANSWERED CORRECTLY. WP.');

  }
  else{
    alert('Failed.');
  }
  $('#studenttask_'+taskid).hide();
}

function correctoption(correctoption,taskid){
  if(correctoption == 'True'){
    alert('YOU ANSWERED CORRECTLY. WP.');
  }
  else{
    alert('Failed.');
  }
    $('#studenttask_'+taskid).hide();
}

$(document).ready(function(){
 // Starts up socket.io. Creates connection.

/******************************************************
                CONNECTS THE STUDENTS
******************************************************/

 var socket = io.connect('http://localhost:3000');
 var lectureid = $('#lectureid').html();
 console.log('asd'+lectureid);
 socket.emit('usertype','student', lectureid);


 /******************************************************
                       START TASK
 ******************************************************/
 socket.on('starttask',function(taskid){
   console.log('TASK IS STARTING. ');
   alert("Task starting :"+taskid);
   $('#studenttask_'+taskid).show();
 });

 /******************************************************
                       END LECTURE
 ******************************************************/
 socket.on('endlecture',function(){
   console.log('the world is nigh, call buffy. ');
   alert("This class has ended, you can no longer vote on the speed");
   location.reload();
 });

 /******************************************************
                      UP AND DOWN BUTTONS
 ******************************************************/
 /*Speed up and down buttons with animation*/
 var toSlow = 0;
 var toFast = 0;
 $("#down").mouseout(function(){
   $("#down").css("background-color","#d1c0c0");
 });
 $("#up").mouseout(function(){
   $("#up").css("background-color","#c0d1be");
 });

 $("#up").mouseover(function(){
   $("#up").css("background-color","grey");
 });
 $("#down").mouseover(function(){
   $("#down").css("background-color","grey");
 });

 $("#up").mousedown(function(){
   $("#up").css("background-color","lightgrey");
 });
 $("#down").mousedown(function(){
   $("#down").css("background-color","lightgrey");
 });

 $("#down").mouseup(function(){
   $("#down").css("background-color","#d1c0c0");
 })
 $("#up").mouseup(function(){
   $("#up").css("background-color","#c0d1be");
 })

  /******************************************************
                FEEDBACK FROM BUTTONS
  ******************************************************/
/*Fade functionality and feedback from buttons.*/
 $("#down").click(function(){
   toFast += 1;
   // Counter on page
   $("#message").text("You pressed the too fast button")
   $("#toFast").text(toFast);
   $("#message").fadeIn("slow");
   setTimeout(function(){
     $("#message").fadeOut("slow");
   }
   ,2000);
   // sending message to the server:
   socket.emit('slower');
 });

 $("#up").click(function(){
   toSlow += 1;
   // Counter on page
   $("#message").text("You pressed the too slow button");
   $("#toSlow").text(toSlow);
   $("#message").fadeIn("slow");
   setTimeout(function(){
     $("#message").fadeOut("slow");
   },2000);
   // sending message to the server:
   socket.emit('faster');
 });

}); // END DOCUMENT READY
