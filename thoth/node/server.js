// Importing libraries
var express = require('express');
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

var lectures = {};

// Now we will connect the users to socket.io.
// Socket io is a library that maintains and keeps track of connected users.
// We added things to student.html and student.js to make it work.

// This creates a connection to the
io.on('connection',function(socket){

  // Creates events for the existing connection

  socket.on('usertype',function(type,lectureid){
    // Checks if the type of person connected is using the javascript from the
    // student page or the teacher page, and decides further actions based on
    // this.

    /******************************************************
                          STUDENT
    ******************************************************/
    if (type == 'student'){
      console.log('Student has logged on to lecture ' + lectureid);
      socket.slower = false;
      socket.faster = false;
      lectures[lectureid]['students'].push(socket);
      io.to(lectures[lectureid].teacherid).emit('update',feedbackcalculator(lectureid));

      // Creates a listener for a signal with a name that MAY contain data.
      // Basically an eventlistener across pages.

      /******************************************************
                            PRESSED BUTTON
      ******************************************************/
      socket.on('slower',function(){
        console.log('Student pressed slower button');
        // send message to teacher:
        socket.slower = true;
        socket.faster = false;
        io.to(lectures[lectureid].teacherid).emit('update',feedbackcalculator(lectureid));
        // ADDED CODE
        setTimeout(function() {
          resetTimer(lectureid, socket);}, 3000);
      });
      socket.on('faster',function(){
        console.log('Student pressed faster button');
        socket.faster = true;
        socket.slower = false;
        io.to(lectures[lectureid].teacherid).emit('update',feedbackcalculator(lectureid));
        //ADDED CODE
        setTimeout(function() {
          resetTimer(lectureid, socket);}, 300000);
      });
      /******************************************************
                            DISCONNECT
      ******************************************************/
      socket.on('disconnect',function(){
        console.log('student disconnect');
        var connectedstudents = lectures[lectureid].students;
          for (var i = 0; i<connectedstudents.length;i++){
            if ( connectedstudents[i].id == socket.id){
              connectedstudents.splice(i,1);
            }
          };
        io.to(lectures[lectureid].teacherid).emit('update',feedbackcalculator(lectureid));
      });
    }
    else{

      /******************************************************
                            TEACHER
      ******************************************************/
      console.log('Teacher has logged on with lecture ' + lectureid);
      // detects the socket id from the teacher connection and sets it.


      if (lectureid in lectures){
        lectures[lectureid].teacherid = socket.id;
        console.log('lecture existed');
        io.to(lectures[lectureid].teacherid).emit('update',feedbackcalculator(lectureid));
      }
      else{
        lectures[lectureid] = {
          teacherid:socket.id,
          students:[],
        };
        console.log('lecture created');
		io.to(lectures[lectureid].teacherid).emit('update',feedbackcalculator(lectureid));
      }
      /******************************************************
                            START TASK
      ******************************************************/
      socket.on('starttask',function(taskid){
        console.log('TASK STARTING NOW: '+taskid);
        // SEND ENDMESSAGELECTURE TO OUR STUDENTS
        var connectedstudents = lectures[lectureid].students;
        for (var i = 0; i<connectedstudents.length;i++){
          var student = connectedstudents[i];
            io.to(student.id).emit('starttask',taskid);
          }
      })
      /******************************************************
                            END LECTURE
      ******************************************************/
      socket.on('endlecture',function(lectureid){
        console.log('Lecture has ended '+lectureid);
        // SEND ENDMESSAGELECTURE TO OUR STUDENTS
        var connectedstudents = lectures[lectureid].students;
        for (var i = 0; i<connectedstudents.length;i++){
          var student = connectedstudents[i];
            io.to(student.id).emit('endlecture');
          }
      })
      /******************************************************
                            DISCONNECT
      ******************************************************/
      socket.on('disconnect',function(){
        console.log('teacher disconnect');
        // her må vi først lagre dataene våre sånn at de ikke forsvinner.
        // dvs stuffe inn i db før delete.
        //delete lectures[lectureid];
      });
    }
  });
});

/******************************************************
                      FEEDBACK CALCULATOR
******************************************************/
function resetTimer(lectureid, socket){
  socket.slower = false;
  socket.faster = false;
  io.to(lectures[lectureid].teacherid).emit('update',feedbackcalculator(lectureid));
  }

function feedbackcalculator(lectureid){
  var connectedstudents = lectures[lectureid].students;
  var slower   = 0;
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


/******************************************************
                      STARTS SERVER
******************************************************/
// Starts the server on port 3000.
http.listen(3000, function(){
  console.log('listening on *:3000');
});
