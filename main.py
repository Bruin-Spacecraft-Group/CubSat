from time import sleep
import time
from threading import Thread, Event
from gpiozero import LED
from appThread import AppThread
from random import random
from sensors import Sensors
from radio import Radio
from camera import Camera

from numberGen import RandomThread
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from threading import Thread


class Main(Thread):
	def __init__(self):
		## initialize sensors
		self.sensorThread = False
		self.radioThread = False
		self.cameraThread = False
		try:
			self.sensorThread = Sensors()
		except:
			print("error initing sensor thread")
		try:
			self.cameraThread = Camera()
		except:
			print("error initializing camera thread")
		try:
			self.radioThread = Radio()
		except:
			print("error initing radio thread")
		#self.numberGen = RandomThread()
		super(Main, self).__init__()
		self.daemon = True
		print("initialized")

	def run(self):
		print("main loop running")
		if self.sensorThread:
			self.sensorThread.start()
		if self.radioThread:
			self.radioThread.start()
		if self.cameraThread:
			self.cameraThread.start()

		startTime = time.time()
		while True:
			# data = self.numberGen.generateData()
			data = {
				'accel': [0,0,0],
				'gyro': [0,0,0],
				'mag': [0,0,0],
				'imu_temp': 0,
				'temp': 0,
				'pressure': 0,
				'alt': 0,
				'voltage': 0,
				'current': 0,
				'dt': 0
			}
			## poll sensors
			if self.sensorThread:
				data = self.sensorThread.data
			if self.cameraThread:
				self.cameraThread.image()
			## send to radio
			endTime = time.time()
			data['dt'] = endTime - startTime
			startTime = endTime
			if flask:
				#print('sending')
				#print("sending {}".format(data))
				pushData(data)
			if self.radioThread:
				#print("sending over radio")
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
