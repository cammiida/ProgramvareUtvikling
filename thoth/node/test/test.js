var io = require('socket.io-client')
, expect = require("chai").expect;
var server = require('../server');
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
	beforeEach(function(){
		teacher = io.connect(socketUrl, options);
		student = io.connect(socketUrl, options);
	})
	afterEach(function(){
		student.disconnect();
		teacher.disconnect();
	})
	
	
	
	it('should connect as a teacher and a new lecture should be created', function(done){
		
		teacher.on('connect', function(){
			teacher.emit('usertype', 'teacher', 1);
		});
		teacher.on('update',function(array){
			expect(array['students']).to.equal(0)
			done();
		});
	});
	
	it('should connect as a student on an existing lecture', function(done){
		teacher.on('connect', function(){
			teacher.emit('usertype', 'teacher', 1);
		});
		student.on('connect', function(){
			student.emit('usertype', 'student', 1);
		});
		teacher.once('update', function(array){
			expect(array['students']).to.equal(0)
			teacher.once('update', function(array){
				expect(array['students']).to.equal(1);
				done();
			});
		});
	});
	
	it('Should update slower-array when student push the slower button', function(done){
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
	
	it('Should update slower-array when student push the faster button', function(done){
			teacher.on('connect', function(){
				teacher.emit('usertype', 'teacher', 2);
			});
			student.on('connect', function(){
				student.emit('usertype', 'student', 2);
				student.emit('faster');
			});
			teacher.once('update', function(){
				teacher.once('update', function(){
					teacher.on('update', function(array){
						expect(array['faster']).to.equal(1);
						done();
					});
				});
			});
	});	
	
	it('should update when student log out', function(done){
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
	
	it('should be possible for a teacher to end a lecture', function(done){
		teacher.on('connect', function(){
			teacher.emit('usertype', 'teacher', 4);
		})
		student.on('connect', function(){
			student.emit('usertype', 'student', 4);
		})
		teacher.emit('endlecture', 4);
		student.on('endlecture', function(){
			done();
		})
		
	})
	it('should be possible for a teacher to start a task', function(done){
		this.timeout(4000)
		teacher.on('connect', function(){
			teacher.emit('usertype', 'teacher', 1)
		})
		student.on('connect', function(){
			student.emit('usertype', 'student', 1)
		})
		teacher.emit('starttask', 1, 1)
		student.on('starttask', function(task){
			student.emit('studentanswer', true, 1)
		})
		teacher.on('sendtasksummay', function(taskid,correct,wrong, loggedon){
			expect(correct).to.equal(1)
			done();
		})	
	})
});
