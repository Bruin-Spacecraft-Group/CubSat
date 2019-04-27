import serial
import serial.tools.list_ports
from time import sleep
from threading import Thread, Event
from gpiozero import LED
from appThread import AppThread
from random import random
from sensors import Sensors

from numberGen import RandomThread
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from threading import Thread


class Main(Thread):
	def __init__(self):

		## Try to open serial port
		comlist = serial.tools.list_ports.comports()
		for x in comlist:
			try:
				print("Opening Serial Port {}".format(x))
				#initiate serial port to read data from
				ser = serial.Serial(
				    port=x,
				    baudrate=115200,
				    timeout=3, #give up reading after 3 seconds
				    parity=serial.PARITY_ODD,
				    stopbits=serial.STOPBITS_TWO,
				    bytesize=serial.SEVENBITS
				)
				print("connected to port {}".format(x))
				break
			except:
				print("Error connecting to {}".format(x))
			#exit()

		## initialize sensors
		self.sensorThread = Sensors()
		self.sensorThread.start()
		#self.numberGen = RandomThread()
		super(Main, self).__init__()
		self.daemon = True
		print("initialized")

	def run(self):
		while True:
			print("loop")
			## poll sensors
			data = self.sensorThread.data
			#data = self.numberGen.generateData()
			# data = {
			# 	'accel': [0,0,0],
			# 	'gyro': [0,0,0],
			# 	'mag': [0,0,0],
			# 	'imu_temp': 0,
			# 	'temp': 0,
			# 	'pressure': 0,
			# 	'alt': 0,
			# 	'voltage': 0,
			# 	'current': 0,
			# 	'dt': 0
			# }

			## send to radio
			if flask:
				print("sending")
				pushData(data)

			sleep(1)
    
flask = True
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)

@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    print('Client connected')

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


def pushData(data):
    socketio.emit('telemetry', data, namespace='/test')

if __name__ == '__main__':
	main = Main()
	main.start()
	socketio.run(app, host='0.0.0.0')
