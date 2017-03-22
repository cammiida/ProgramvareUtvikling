$(document).ready(function(){

	// Starts up socket.io. Creates connection.
	console.log('node er på.');
  	var socket = io.connect('http://localhost:3000');


	
  

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
  socket.on('update', function(data){
    console.log(data);
    if (data.students < 1){
      $('#fast_slow').html('too few students online');
    }
    else{
      if (data.slower/data.students >= 0.4){
        showNotification("too slow");
        $('#fast_slow').html('the lecture speed is too slow');}
      else if (data.faster/data.students >= 0.4){
        showNotification("too fast");
        $('#fast_slow').html('the lecture speed is too fast');}
      else{
        $('#fast_slow').html('the lecture speed is fine');}
      }
  });

function showNotification(message){
    var title = "Dette er en test";
    console.log("kjører denne?")
	var options = 	{
						body: message,
 	   					image: "/static/images/logo.png",
						silent: true
						}
	var notification = new Notification(title, options);
		notification.onshow = function(){
			  console.log("dette er en test")
			  setTimeout(function(){
			  	notification.close();
			  },2000)
		  }
  };

});
