var io = require('socket.io').listen(3000);
//var connectedstudents = {'students': []};
console.log("listening on 3000")
const util = require('util');
var connectedstudents = [];
var teacherid;

io.on('connection', function(socket){
	socket.on('usertype', function(type){
		if(type == 'student')
		{
			io.emit('usertype', 'student');
			console.log('student has logged on');
			socket.slower = false;
			socket.faster = false;
			connectedstudents.push(socket);
			io.to(teacherid).emit('update',feedbackcalculator());
			
	
			socket.once('array', function(){
				var connectedStudent = {'students': []};
				connectedStudent['students'].push('socket');
				console.log('Skal sende array');
				io.emit('array', connectedStudent);
			});

			//io.to(teacherid).emit('update', feedbackcalcualtor());
		}
	    else{
	     	console.log('Teacher has logged on');
	     	// detects the socket id from the teacher connection and sets it.
	      	teacherid = socket.id;
			socket.emit('teacherid',{'teacherId': teacherid});
	    }
	})
	io.emit('echo', 'Hello World');
})

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
