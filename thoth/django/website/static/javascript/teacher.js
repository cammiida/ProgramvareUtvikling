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


/******************************************************
                  DOCUMENT IS RUNNING
******************************************************/
$(document).ready(function(){
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

	// Starts up socket.io. Creates connection.
	console.log('node er på.');
	//socket = io.connect('http://thothnode.helemork.com');
	socket = io.connect('localhost:3000');

	var lectureid = $('#lectureid').html();

	/******************************************************
	                      LOGS ON TEACHER
	******************************************************/
  socket.emit('usertype','teacher',lectureid);

	/******************************************************
	                     RECEIVE TASK SUMMARY
	******************************************************/
	socket.on('sendtasksummay',function(taskid,correct,wrong, loggedon){
		var timedoutnr = (loggedon-correct-wrong);
		var correctpercentage = (correct/loggedon)*100;
		var wrongpercentage = (wrong/loggedon)*100;
		var timedoutpercentage = (timedoutnr/loggedon)*100;
		// Want to do an ajax post to save the history into the database
		// for later use.
		$.post('/savetaskhistory/',{
			taskid:taskid,
			correct:correct,
			wrong:wrong,
			timedoutnr:timedoutnr,
		});
		alert(correct+' out of '+loggedon+' students answered correctly to task '+taskid+' while '+wrong+' answered wrongly.')
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
  //if you can recieve push notifications
  var canCall = true;

  socket.on('update', function(data){
    if (data.students < 1){
      $('#fast_slow').html('too few students online');
    }
    else{
    console.log("cancall = " + canCall)
      slowerPercent = data.slower/data.students;
      fasterPercent = data.faster/data.students;

      if (slowerPercent >= 0.4){	//chosen threshold for when pushnotification can be shown
        if (canCall){
          showNotification("too slow " + slowerPercent*100 + "% means this", "/static/images/thoth.png");
					// Want to do an ajax post to save the history into the database
					// for later use.
					$.post('/savefeedback/',{
						lectureid:lectureid,
						up:data.slower,
						down:data.faster,
						none:(data.students-data.slower-data.faster),
					});
		  canCall = false;
		  //timer for how often push notifications can be shown, in ms
          setTimeout(function() {canCall = true;}, 10000);}
        $('#fast_slow').html('the lecture speed is too slow');}
      else if (fasterPercent >= 0.4){
        if (canCall){
          showNotification("too fast " + fasterPercent*100 + "% means this", "/static/images/thoth.png");
					// Want to do an ajax post to save the history into the database
					// for later use.
					$.post('/savefeedback/',{
						lectureid:lectureid,
						up:data.slower,
						down:data.faster,
						none:(data.students-data.slower-data.faster),
					});
          canCall = false;
          //timer for how often push notifications can be shown, in ms
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
    var title = "Adjust your lecture speed";
	var options = 	{
						body: message,
						icon: icon,
						image: icon
						}
	var notification = new Notification(title, options);
		notification.onshow = function(){
			  setTimeout(function(){
			  	notification.close();
			  }, 2000)
		  }
  };

});
