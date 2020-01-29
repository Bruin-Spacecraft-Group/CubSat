var socket;
$(document).ready(function(){
    console.log("Running")
    //connect to the socket server.
    socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    console.log("got here")
    //receive data from server
    socket.on('telemetry', function(msg) {
      console.log(msg)
      console.log("got here")
      
      $(randomNumber).text(msg)
    });

});
