$(document).ready(function(){
  var socket = io();
  socket.emit('usertype','teacher');

  // Create a listener for signals from the server.
  socket.on('update',function(data){
    console.log(data);
    if (data.students > 0){
      $('#up').html(Math.round(100*data.faster/data.students) + '%');
      $('#down').html(Math.round(100*data.slower/data.students) + '%');
    }
    else{
      $('#up').html(' 0%');
      $('#down').html(' 0%');
    }

  });


});
