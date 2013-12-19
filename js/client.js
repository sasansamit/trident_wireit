var WebSocket = require('ws');
var os = require('os');
var ws = new WebSocket('ws://localhost:12345/');

function s4() {
  return Math.floor((1 + Math.random()) * 0x10000)
             .toString(16)
             .substring(1);
};

function guid() {
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
         s4() + '-' + s4() + s4() + s4();
};
var clientId = "345";

ws.on('open', function() {

  var curMemToSend = 10;

  var id = setInterval(function() {
	if (curMemToSend == 10) {
		console.log("sending anomaly memory = 2500");
		curMemToSend = 2500;
	}
	else {
		console.log("sending normal memory = 10");
		curMemToSend = 10;
	}
  }, 40*1000);


  var id = setInterval(function() {
	var data = {};
	//data["heapUsed"] = process.memoryUsage().heapUsed;
	data["deviceid"] = clientId;
	data["timestamp"] = Date.now();
	//var memory = ((os.totalmem() - os.freemem())/(1024*1024));
	data["memory"] = curMemToSend;//.toString();
	console.log('data being sent %s', JSON.stringify(data));
    ws.send(JSON.stringify(data));
  }, 1000);
});
ws.on('message', function(data, flags) {
	console.log('recieved server data %s',data);
    // flags.binary will be set if a binary data is received
    // flags.masked will be set if the data was masked
});
