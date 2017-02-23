var express = require('express');
var app = require('express')();
var http = require('http').Server(app);

app.get('/', function(req, res){
  res.sendFile(__dirname + '/student.html');
});

app.use('/', express.static(__dirname + '/'));

http.listen(3000, function(){
  console.log('listening on *:3000');
});
