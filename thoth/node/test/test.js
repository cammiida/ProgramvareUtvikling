
var io = require('socket.io-client')
, expect = require("chai").expect;
	//,io_server = require('socket.io').listen(3001);

var socketUrl = 'http://localhost:3000';

var options = {
            'reconnection delay' : 0
            , 'reopen delay' : 0
            , 'force new connection' : true
       	 	};

			var socket;


		


describe('sockets', function(){
	
	beforeEach(function(done){
		socket = io.connect(socketUrl, options);
		socket.on('connect', function(){
			socket.emit('usertype', 'student');
			console.log('worked');
			done();
		});
	    socket.on('disconnect', function() {
	        console.log('disconnected...');
	    })
	});

	afterEach(function(done){
				if(socket.connected) {
		            console.log('disconnecting...');
		            socket.disconnect();
		        } 
				else {
		            // There will not be a connection unless you have done() in beforeEach, socket.on('connect'...)
		            console.log('no connection to break...');
		     	 }
		done();
	});
	
	it('should know if a student log in', function(done){
		var connectedStudents = [];
		socket.emit('array', 'student');
		socket.on('array', function(connectedstudents){
			connectedStudents = connectedstudents.games;
			expect(connectedstudents['students']).to.have.length(1);
			expect(connectedstudents['students'][0]).to.equal('socket');
			done();
		});
	});

	it('should communicate', function (done){  	
		socket.once('echo', function(message){
			expect(message).to.equal('Hello World');
			done();
		});
	});
	
	it('should recognize student user', function(done){
		socket.on('usertype', function(type){
			expect(type).to.equal('student');
			done();
		});
	});
	
	it('should connect as a teacher', function(done){
		socket = io.connect(socketUrl, options);
		socket.on('connect', function(){
			socket.emit('usertype', 'teacher');
		});
		socket.on('teacherid', function(array){
			expect(array['teacherId']).equal(socket.id);
		});
		socket2 = io.connect(socketUrl, options);
		socket2.on('connect', function(){
			socket.emit('usertype', 'student');
		})
		socket.on('update', function(feedbackcalculator){
			expect(feedbackcalculator['students']).to.be.above(3);
			done();
		});
	});
});