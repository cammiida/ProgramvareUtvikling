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
			var util = require('util');

describe('sockets', function(){
	afterEach(function(){
		student.disconnect();
		teacher.disconnect();
	})
	
	
	
	it('should connect as a teacher, to connect as student and update connected students', function(done){
		teacher = io.connect(socketUrl, options);
		teacher.on('connect', function(){
			teacher.emit('usertype', 'teacher', 1);
		});
		student = io.connect(socketUrl, options);
		student.on('connect', function(){
			student.emit('usertype', 'student', 1);
		});
		teacher.once('update', function(array){
			teacher.on('update', function(array){
				expect(array['students']).to.equal(1);	
				done();
			});
		});
	});
	
	it('Should know update slower if student pushed slower', function(done){
		teacher = io.connect(socketUrl, options);
		student = io.connect(socketUrl, options);
		teacher.on('connect', function(){
			teacher.emit('usertype', 'teacher', 2);
		});
		student.on('connect', function(){
			student.emit('usertype', 'student', 2);
			student.emit('slower');
		});
		teacher.once('update', function(){
			teacher.once('update', function(){
				teacher.on('update', function(array){
					expect(array['slower']).to.equal(1);
					done();
				});
			});
		});
	});
	
	it('should update when student log out', function(done){
		teacher = io.connect(socketUrl, options);
		student = io.connect(socketUrl, options);
		teacher.on('connect', function(){
			teacher.emit('usertype', 'teacher', 3);
		});
		student.on('connect', function(){
			student.emit('usertype', 'student', 3);
		});
		teacher.once('update', function(array){
			teacher.once('update', function(array){
				expect(array['students']).to.equal(1);
				student.disconnect();
				teacher.on('update', function(array){
					expect(array['students']).to.equal(0);
					done();
				});
			});
		});
	});
	
	it('should be able to start up existing lecture', function(done){
		teacher = io.connect(socketUrl, options);
		teacher.on('connect', function(){
			teacher.emit('usertype', 'teacher', 1);
		});
		teacher.on('update', function(array){
			console.log(util.inspect(array))
			expect(array['students']).to.equal(0);
			done();
		});
	});
});
