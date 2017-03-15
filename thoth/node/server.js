// Importing libraries
var express = require('express');
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

// Big security hole, but makes all files availiable from the outside.
// Quickfix for us.
// We will fix this hole later. But it works for the first demo.
app.use('/', express.static(__dirname + '/'));


var teacherid;
var connectedstudents = [];


// Now we will connect the users to socket.io.
// Socket io is a library that maintains and keeps track of connected users.
// We added things to student.html and student.js to make it work.

// This creates a connection to the
io.on('connection',function(socket){

  // Creates events for the existing connection

  socket.on('usertype',function(type){
    // Checks if the type of person connected is using the javascript from the
    // student page or the teacher page, and decides further actions based on
    // this.
    if (type == 'student'){
      console.log('Student has logged on');
      socket.slower = false;
      socket.faster = false;
      connectedstudents.push(socket);
      io.to(teacherid).emit('update',feedbackcalculator());

      // Creates a listener for a signal with a name that MAY contain data.
      // Basically an eventlistener across pages.
      socket.on('slower',function(){
        console.log('Student pressed slower button');
        // send message to teacher:
        socket.slower = true;
        socket.faster = false;
        io.to(teacherid).emit('update',feedbackcalculator());
      });
      socket.on('faster',function(){
        console.log('Student pressed faster button');
        socket.faster = true;
        socket.slower = false;
        io.to(teacherid).emit('update',feedbackcalculator());
      });
      socket.on('disconnect',function(){
          for (var i = 0; i<connectedstudents.length;i++){
            if ( connectedstudents[i].id == socket.id){
              connectedstudents.splice(i,1);
            }
          };
          io.to(teacherid).emit('update',feedbackcalculator());
      });
    }
    else{
      console.log('Teacher has logged on');
      // detects the socket id from the teacher connection and sets it.
      teacherid = socket.id;
    }
  });
});

function feedbackcalculator(){
  var slower = 0;
  var faster = 0;
  for (var i = 0; i<connectedstudents.length;i++){
    var student = connectedstudents[i];
    if (student.slower == true){
      slower += 1;
    };
    if (student.faster == true){
      faster += 1;
    };
  };

  return {
    slower:slower,
    faster:faster,
    students:connectedstudents.length,
  }
};



// Starts the server on port 3000.
http.listen(3000, function(){
  console.log('listening on *:3000');
});
