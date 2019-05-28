var activePage = "Main"
var gauges = [];
var lines = [];
var map;
var flightPlanCoordinates = [];
var state = {
    'accel': [0,0,0],
    'velocity': [0,0,0],
    'position': [0,0,0],
    'gyro': [0,0,0],
    'angle': [0,0,0],
    'mag': [0,0,0],
    'temp': 0,
    'pressure': 0,
    'alt': 0,
    'gps': 'no_fix',
    'bus_voltage': 0,
    'shunt_voltage': 0,
    'current': 0,
    'dt': 0,
    'runtime': 0
}  

function createGauge(name, label, min, max)
{
    console.log(name)
    var config = 
    {
        size: 180,
        label: label,
        min: undefined != min ? min : 0,
        max: undefined != max ? max : 100,
        minorTicks: 5,
        greenColor: "#109618",
        yellowColor: "#ffff74",
        redColor: "#ff1744",
    }
    
    var range = config.max - config.min;
    config.yellowZones = [{ from: config.min + range*0.75, to: config.min + range*0.9 }];
    config.redZones = [{ from: config.min + range*0.9, to: config.max }];
    
    gauges[name] = new Gauge(name + "GaugeContainer", config);
    gauges[name].render();
}

function createGauges()
{
    createGauge("velocity_x", "Velocity X");
    createGauge("velocity_y", "Velocity Y");
    createGauge("velocity_z", "Velocity Z");
    createGauge("angular_x", "Angular X");
    createGauge("angular_y", "Angular Y");
    createGauge("angular_z", "Angular Z");
}

function updateGauges()
{
    gauges['velocity_x'].redraw(Math.abs(state['velocity'][0]));
    gauges['velocity_y'].redraw(Math.abs(state['velocity'][1]));
    gauges['velocity_z'].redraw(Math.abs(state['velocity'][2]));
    gauges['angular_x'].redraw(Math.abs(state['gyro'][0]));
    gauges['angular_y'].redraw(Math.abs(state['gyro'][1]));
    gauges['angular_z'].redraw(Math.abs(state['gyro'][2]));
}

function createLineGraph(name)
{
    lines[name] = new LineGraph(name + "LineGraphContainer");
    lines[name].makeLine();
}
function createLineGraphs()
{
    createLineGraph('accel_x')
}
function updateLineGraphs()
{
    lines['accel_x'].addPoint(state['accel'][0],state['runtime']);
}

function initMap() {
    var element = document.createElement("script")
    element.src = `https://maps.googleapis.com/maps/api/js?key=${googleAPIkey}`
    element.onload = function(){
            map = new google.maps.Map(document.getElementById('map'), {
              zoom: 16,
              center: {lat: 0, lng: -180},
              mapTypeId: 'terrain'
            });
            console.log('map inited')
        }
    document.body.appendChild(element)
}

function updateMap() {
    if (state['gps'] == 'no_fix') {
        return
    }

    flightPlanCoordinates.push({lat: state['gps']['coords'][0], lng: state['gps']['coords'][1]})

    var flightPath = new google.maps.Polyline({
      path: flightPlanCoordinates,
      geodesic: true,
      strokeColor: '#FF0000',
      strokeOpacity: 1.0,
      strokeWeight: 2
    });

    flightPath.setMap(map);
    map.setCenter({lat: state['gps']['coords'][0], lng: state['gps']['coords'][1]})
}

function updateConsole() {
    $('#acceleration').text(`${state['accel'][0].toFixed(2)}, ${state['accel'][1].toFixed(2)}, ${state['accel'][2].toFixed(2)}`)
    $('#velocity').text(`${state['velocity'][0].toFixed(2)}, ${state['velocity'][1].toFixed(2)}, ${state['velocity'][2].toFixed(2)}`)
    $('#angVelocity').text(`${state['gyro'][0].toFixed(2)}, ${state['gyro'][1].toFixed(2)}, ${state['gyro'][2].toFixed(2)}`)
    $('#pressure').text(`${state['pressure'].toFixed(2)}`)
    $('#temperature').text(`${state['temp'].toFixed(2)}`)
    $('#bus_voltage').text(`${state['bus_voltage'].toFixed(2)}`)
    $('#shunt_voltage').text(`${state['shunt_voltage'].toFixed(2)}`)
    $('#current').text(`${state['current'].toFixed(2)}`)
    $('#power').text(`${(state['bus_voltage']*state['current'].toFixed(2)).toFixed(2)}`)
    $('#altitude').text(`${state['alt'].toFixed(2)}`)
    $('#position').text(`${state['position'][0].toFixed(2)}, ${state['position'][1].toFixed(2)}, ${state['position'][2].toFixed(2)}`)
    if (state['gps'] == 'no_fix'){
        $('#coordinates').text('no fix')
    }
    else {        
        $('#coordinates').text(`${state['gps']['coords'][0].toFixed(2)}, ${state['gps']['coords'][1].toFixed(2)}`)
    }
}

function updateVideo() {

}

function initialize()
{
    createGauges();
    createLineGraphs();
    initMap()
    console.log("initialized")
}

function processTelemetry(data)
{
    for(key in data){
        state[key] = data[key]
    }
    
    for(i in state['velocity']){
        state['velocity'][i] = state['velocity'][i] + state['accel'][i]*state['dt']
    }

    for(i in state['position']){
        state['position'][i] = state['position'][i] + state['velocity'][i]*state['dt']
    }
    
    for(i in state['gyro']){
        state['angle'][i] = state['angle'][i] + state['gyro'][i]*state['dt']
    }
    state['runtime'] += state['dt']
    console.log(state['gps'])
}

$(document).ready(function(){
    console.log("Running")
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    initialize()
    //receive details from server
    socket.on('telemetry', function(msg) {
        //console.log("Received message " + msg);
        processTelemetry(msg)
        switch(activePage){
            case "Main":
                updateGauges()
                updateLineGraphs()
                updateMap()
                break;
            case "Console":
                updateConsole()
                break;
            case "Video":
                updateVideo()
                break;
        }

        //console.log(JSON.stringify(state))
    });

});

function switchPage(object) {
    $(".vizPage").each(function(){
        $(this).hide()
    })
    activePage = object.id.slice(6,object.id.length)
    $("#"+activePage).show()

}