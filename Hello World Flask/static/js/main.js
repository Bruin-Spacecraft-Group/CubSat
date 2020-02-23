var socket;
var accels = [];
var times = [];
var start_time = new Date();

$(document).ready(function(){
    console.log("Running")
    //connect to the socket server.
    socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    console.log("got here")
    //receive data from server
    socket.on('telemetry', function(msg) {
      console.log(msg)
      console.log("got here")
      accels.push(msg[2])
      let now = new Date()
      times.push((now - start_time)/1000)
      let data = {
	x: times,
	y: accels,
	type: 'scatter'
      }
      console.log(data)
      Plotly.newPlot('plot', [data])
      $(randomNumber).text(msg)
    });

});
