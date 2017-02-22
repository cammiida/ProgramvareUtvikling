var express = require('express');
  app = express();
  http = require('http');
  fs = require('fs');



fs.readFile('./index_page.html', function (err, html) {
    if (err) {
        throw err;
    }
    http.createServer(function(request, response) {
        response.writeHeader(200, {"Content-Type": "text/html"});
        response.write(html);
        response.end();
    }).listen(8000);
});

console.log('Server running on port 8000.');

function redirectToStudentPage(){
  app.get('/student', function(req, res){
    res.send('You were redirected to the student page');
  });
}

function redirectToTeacherPage(){
  app.get('/teacher', function(req, res){
    res.send('You were redirected to the teacher page');
  });
}
