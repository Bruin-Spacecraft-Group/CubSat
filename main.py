import serial
from time import sleep
from threading import Thread, Event
from gpiozero import LED
from appThread import AppThread
from sensors import Sensors


class Main():
	def __init__(self):

		## Try to open serial port
		try:
			print("Opening Serial Port...")
			#initiate serial port to read data from
			SERIAL_PORT = 'COM4'
			ser = serial.Serial(
			    port=SERIAL_PORT,
			    baudrate=115200,
			    timeout=3, #give up reading after 3 seconds
			    parity=serial.PARITY_ODD,
			    stopbits=serial.STOPBITS_TWO,
			    bytesize=serial.SEVENBITS
			)
			print("connected to port " + SERIAL_PORT)
		except:
			print("<==Error connecting to " + SERIAL_PORT + "==>")
			#exit()

		## initialize sensors
		self.sensorThread = Sensors(self)

		flask = True
		if flask == True:
			self.appThread = AppThread()


while True:
	## poll sensors
	data = self.sensorThread.data
	## send to radio
	socketio.emit('telemetry', data, namespace='/test')
    
