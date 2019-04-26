console.log("Dummy")
var gauges = [];
var state = {
    'accel': [0,0,0],
    'velocity': [0,0,0],
    'gyro': [0,0,0],
    'angle': [0,0,0],
    'mag': [0,0,0],
    'temp': 0,
    'pressure': 0,
    'alt': 0,
    'voltage': 0,
    'current': 0,
    'dt': 0
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
        minorTicks: 5
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

function initialize()
{
    createGauges();
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
    
    for(i in state['gyro']){
        state['angle'][i] = state['angle'][i] + state['gyro'][i]*state['dt']
    }
}

$(document).ready(function(){
    console.log("Running")
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    initialize()
    //receive details from server
    socket.on('telemetry', function(msg) {
        console.log("Received message " + msg);
        processTelemetry(msg)
        updateGauges()
        console.log(JSON.stringify(state))
    });

});