var expect = require("chai").expect
var io = require("socket.io-client");
var should = require("chai").should

var socketUrl = 'http://localhost:3000';

var options = {
	transports:['websocket'],
	'force new connection': true
};

var expected = ["hei"]

var room = 'lobby'

beforeEach(function(done){
	socket = io.connect(socketUrl, options)
	socket.on('connect', function(){
		console.log('worked');
		done();
	});
});

afterEach(function(done){
	if(socket.connected)
})


describe('sockets', function(){
	var client1;
});

it('should connect as student', function (done){  
    // Set up client1 connection

    // Set up event listener.  This is the actual test we're running
    client1.on('usertype', function(type){
      	type.should.equal('student');
		
	    client1.disconnect();
		done();
	  // Disconnect both client connections
	});

	client1.on('connect', function(){
		client1.emit('usertype', 'student');
    });
  });