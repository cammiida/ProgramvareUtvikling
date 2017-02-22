var express = require('express');
var http = require('http');
var fs = require('fs');

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
