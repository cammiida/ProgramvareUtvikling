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

});
