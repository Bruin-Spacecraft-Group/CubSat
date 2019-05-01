from time import sleep
from threading import Thread, Event
from gpiozero import LED
from appThread import AppThread
from random import random
from sensors import Sensors
from radio import Radio

from numberGen import RandomThread
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from threading import Thread


class Main(Thread):
	def __init__(self):
		## initialize sensors
		self.sensorThread = Sensors()
		self.radioThread = Radio()
		#self.numberGen = RandomThread()
		super(Main, self).__init__()
		self.daemon = True
		print("initialized")

	def run(self):
		self.sensorThread.start()
		self.radioThread.start()
		while True:
			## poll sensors
			data = self.sensorThread.data
			# data = self.numberGen.generateData()
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
				print('sending')
				#print("sending {}".format(data))
				pushData(data)
				self.radioThread.sendData(data)

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
