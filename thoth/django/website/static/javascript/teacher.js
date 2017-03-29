var socket;

function endlecture(url,lectureid){
	socket.emit('endlecture',lectureid);
	location.href=url;
}

$(document).ready(function(){

	// Starts up socket.io. Creates connection.
	console.log('node er på.');
  	socket = io.connect('http://localhost:3000');





	var lectureid = $('#lectureid').html();

  socket.emit('usertype','teacher',lectureid);
  // Create a listener for signals from the server.
  socket.on('update',function(data){
    console.log(data);
    if (data.students > 0){
      $('#up').html(Math.round(100*data.faster/data.students) + '%');
      $('#down').html(Math.round(100*data.slower/data.students) + '%');
			$('#studentsconnected').html(data.students);
    }
    else{
      $('#up').html(' 0%');
      $('#down').html(' 0%');
			$('#studentsconnected').html(0);
    }
  });

  //Logic for when lecturespeed is to high/slow
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
