var http = require('http').createServer(handler); //require http server, and create server with function handler()
var fs = require('fs'); //require filesystem module
//var io = require('socket.io')(http) //require socket.io module and pass the http object (server)

const io = require('socket.io')(http, {
    cors: {
        origin: "http://localhost:8080",
        methods: ["GET", "POST"],
        transports: ['websocket', 'polling'],
        credentials: true
    },
    allowEIO3: true
});

const spawn = require("child_process").spawn;
const pythonProcess = spawn('python',["Python/IRSensor.py"]);

http.listen(8080); //listen to port 8080
console.log("Server Running");

function handler (req, res) { //create server
  fs.readFile(__dirname + '/public/index.html', function(err, data) { //read file index.html in public folder
    if (err) {
      res.writeHead(404, {'Content-Type': 'text/html'}); //display 404 on error
      return res.end("404 Not Found");
    }
    res.writeHead(200, {'Content-Type': 'text/html'}); //write HTML
    res.write(data); //write data from index.html
    return res.end();
  });
}

io.sockets.on('connection', function (socket) {// WebSocket Connection
console.log("Connected!")
  var lightvalue = 0; //static variable for current status
  socket.on('light', function(data) { //get light switch status from client
    lightvalue = data;
    if (lightvalue) {
      console.log(lightvalue); //turn LED on or off, for now we will just show it in console.log
    }
  });
  
  pythonProcess.stdout.on('data', (data) => {
	console.log(data.toString('utf8')); 
  socket.emit("txt", data.toString('utf8'));
// Do something with the data returned from python script
});
});

//pythonProcess.stdout.on('data', (data) => {
	//console.log(data.toString('utf8')); 
// Do something with the data returned from python script
//});
