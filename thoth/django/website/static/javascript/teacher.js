$(document).ready(function(){

	// Starts up socket.io. Creates connection.
	console.log('node er på.');
  	var socket = io.connect('http://localhost:3000');
	var title = "Dette er en test";
	var options = 	{
						body: "testen går som følgende",
 	   					image: "/static/images/logo.png",
						silent: true
					}
	
  

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
    if (data.students < 10){
      $('#fast_slow').html('too few students online');
    }
    else{
      if (data.slower/data.students >= 0.4){
        $('#fast_slow').html('the lecture speed is to slow');}
      else if (data.faster/data.students >= 0.4){
        $('#fast_slow').html('the lecture speed is to fast');}
      else{
        $('#fast_slow').html('the lecture speed is fine');}
      }
  });

  socket.on('show', function(){
	var notification = new Notification(title, options);
		notification.onshow = function(){
			  console.log("dette er en test")
			  setTimeout(function(){
			  	notification.close();
			  },2000)
		  }
  });

});
