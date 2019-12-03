from time import sleep
from threading import Thread, Event
from appThread import AppThread
from random import random

from numberGen import RandomThread
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context


class Main(Thread):
	def __init__(self):
		## initialize sensors
		self.sensorThread = False
		self.radioThread = False
		self.groundRadioThread = False
		try:
			self.sensorThread = Sensors()
		except:
			print("error initing sensor thread")
		try:
			#self.radioThread = Radio()
			self.groundRadioThread = GroundRadio()
		except:
			print("error initing radio thread")
		self.numberGen = RandomThread()
		super(Main, self).__init__()
		self.daemon = True
		print("initialized")

	def run(self):
		print("main loop running")
		if self.sensorThread:
			self.sensorThread.start()
		if self.radioThread:
			self.radioThread.start()
		if self.groundRadioThread:
			self.groundRadioThread.start()
		while True:
			## poll sensors
			#data = self.sensorThread.data
			#data = self.numberGen.generateData()
			data = self.groundRadio.read()
			# data = {
			# 	'accel': [0,0,0],
			# 	'gyro': [0,0,0],
			# 	'mag': [0,0,0],
			# 	'imu_temp': 0,
			# 	'temp': 0,
			# 	'pressure': 0,
			# 	'alt': 0,
			# 	'bus_voltage': 0,
			# 	'shunt_voltage': 0,
			# 	'current': 0,
			# 	'dt': 0
			# }

			## send to radio
			if flask:
				#print('sending')
				#print("sending {}".format(data))
				pushData(data)
				dataString = str(round(data['accel'][0],3)) + ',' + str(round(data['accel'][1], 3)) + ',' + str(round(data['accel'][2], 3))
				dataString += ',' + str(round(data['gyro'][0],3)) + ',' + str(round(data['gyro'][1],3)) + ',' + str(round(data['gyro'][2],3))
				dataString += ',' + str(round(data['mag'][0],2)) + ',' + str(round(data['mag'][1],2)) + ',' + str(round(data['mag'][2],2))
				dataString += ',' + str(round(data['imu_temp'], 2))
				dataString += ',' + str(round(data['temp'],3))
				dataString += ',' + str(round(data['pressure'],3))
				dataString += ',' + str(round(data['alt'],3))
				dataString += ',' + str(round(data['alt'],3))
				dataString += ',' + str(round(data['bus_voltage'],3))
				dataString += ',' + str(round(data['shunt_voltage'],3))
				dataString += ',' + str(round(data['current'],3))
				dataString += ',' + str(round(data['dt'],3))
				try:
					dataString += ',' + str(data['gps']['time']) + ',' + str(data['gps']['coords'][0]) + ',' + str(data['gps']['coords'][1])
				except:
					pass
				try:
					dataString += ',' + str(data['gps']['quality'])
					dataString += ',' + str(round(data['gps']['satellites'],3))
					dataString += ',' + str(round(data['gps']['altitude'],3))
					dataString += ',' + str(round(data['gps']['speed'],3))
					dataString += ',' + str(round(data['gps']['track_angle'],3))
					dataString += ',' + str(round(data['gps']['dilation'],3))
					dataString += ',' + str(round(data['gps']['height_geoid'],3))
				except:
					pass

				print(dataString)
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

@socketio.on('command', namespace='/test')
def got_command(cmd):
    print('GOT MESSAGE')
    print(cmd)
    socketio.emit('response', "received: " + cmd, namespace='/test')

def pushData(data):
    socketio.emit('telemetry', data, namespace='/test')

if __name__ == '__main__':
	main = Main()
	main.start()
	socketio.run(app, host='0.0.0.0')
