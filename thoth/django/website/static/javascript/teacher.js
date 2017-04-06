var socket;

/******************************************************
                    END LECTURE
******************************************************/
function endlecture(url,lectureid){
	socket.emit('endlecture',lectureid);
	location.href=url;
}

/******************************************************
                      START TASK
******************************************************/
function starttask(taskid,timeout){
	console.log(taskid);
	socket.emit('starttask',taskid,timeout);
}

/******************************************************
                  DOCUMENT IS RUNNING
******************************************************/
$(document).ready(function(){


	// Starts up socket.io. Creates connection.
	console.log('node er på.');
  	socket = io.connect('http://localhost:3000');


	var lectureid = $('#lectureid').html();

	/******************************************************
	                      LOGS ON TEACHER
	******************************************************/
  socket.emit('usertype','teacher',lectureid);

	/******************************************************
	                     RECEIVE TASK SUMMARY
	******************************************************/
	socket.on('sendtasksummay',function(taskid,correct,wrong, loggedon){
		alert(correct+' out of '+loggedon+' students answered correctly to task '+taskid+' while '+wrong+' answered wrongly.')
		var correctpercentage = (correct/loggedon)*100;
		var wrongpercentage = (wrong/loggedon)*100;
		var timedoutnr = (loggedon-correct-wrong);
		var timedoutpercentage = (timedoutnr/loggedon)*100;
		$('#correctanswers').html(Math.round(correctpercentage) + '%');
		$('#wronganswers').html(Math.round(wrongpercentage) + '%');
		$('#timedoutanswers').html(Math.round(timedoutpercentage) + '%');
		$('#correctanswers').css('height',Math.round(correctpercentage)*3+'px');
		$('#wronganswers').css('height',Math.round(wrongpercentage)*3+'px');
		$('#timedoutanswers').css('height',Math.round(timedoutpercentage)*3+'px');
	});

	/******************************************************
	                     UPDATE SPEED
	******************************************************/


	socket.on('update',function(data){
		console.log(data);
		if (data.students > 0){
			$('#speedup').html(Math.round(100*data.faster/data.students) + '%');
			$('#slowdown').html(Math.round(100*data.slower/data.students) + '%');
			$('#speedup').css('height',Math.round(100*data.faster/data.students)*3+'px');
			$('#slowdown').css('height',Math.round(100*data.slower/data.students)*3+'px');
			$('#studentsconnected').html('Students online: </br>'+data.students);
		}
		else{
			$('#speedup').html(' 0%');
			$('#slowdown').html(' 0%');
			$('#studentsconnected').html(0);
		}
	});


	/******************************************************
	                     LECTURE SPEED LOGIC
	******************************************************/
  var canCall = true;
  socket.on('update', function(data){
    console.log(data);
    if (data.students < 1){
      $('#fast_slow').html('too few students online');
    }
    else{
    console.log("cancall = " + canCall)
      slowerPercent = data.slower/data.students;
      fasterPercent = data.faster/data.students;
      if (slowerPercent >= 0.4){
        if (canCall){
          showNotification("too slow " + slowerPercent*100 + "% means this", "/static/images/thoth.png");
          canCall = false;
          setTimeout(function() {canCall = true;}, 10000);}
        $('#fast_slow').html('the lecture speed is too slow');}
      else if (fasterPercent >= 0.4){
        if (canCall){
          showNotification("too fast " + fasterPercent*100 + "% means this", "/static/images/thoth.png");
          canCall = false;
          setTimeout(function() {canCall = true;}, 10000);}
        $('#fast_slow').html('the lecture speed is too fast');}
      else{
        $('#fast_slow').html('the lecture speed is fine');}
      }
  });


/******************************************************
	                   SHOW NOTOFICATION
******************************************************/
function showNotification(message, icon){
    var title = "Dette er en test";
    console.log("kjører denne?")
	var options = 	{
						body: message,
						icon: icon,
						image: icon
						}
	var notification = new Notification(title, options);
		notification.onshow = function(){
			  console.log("dette er en test")
			  setTimeout(function(){
			  	notification.close();
			  }, 2000)
		  }
  };

});
