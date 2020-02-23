import board
import busio
import digitalio
import adafruit_rfm9x
import json
import math
from threading import Thread
from dataMap import dataMap

class GroundRadio(Thread):
	def __init__(self):
		spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
		cs = digitalio.DigitalInOut(board.D25) #can be any GPIO
		reset = digitalio.DigitalInOut(board.D8) #can be any GPIO
		self.rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)
		self.dataSize = 252 - 2 - 12 #number of bytes we can send in packet, minus check bytes
		super(GroundRadio, self).__init__()

	def read(self):
		packet = self.rfm9x.receive()  # Wait for a packet to be received (up to 0.5 seconds)
		if packet is not None:
			packet_text = str(packet, 'ascii')
			print('Received: {}'.format(packet_text))
			try:
				data = packet_text.split(",")
				dataDict = {
					'accel': [data(dataMap['accel_x']),data(dataMap['accel_y']),data(dataMap['accel_z'])],
					'gyro': [data(dataMap['gyro_x']),data(dataMap['gyro_y']),data(dataMap['gyro_z'])],
					'mag': [data(dataMap['mag_x']),data(dataMap['mag_y']),data(dataMap['mag_z'])],
					'imu_temp': data(dataMap['imu_temp']),
					'temp': data(dataMap['temp']),
					'pressure': data(dataMap['pressure']),
					'alt': data(dataMap['alt']),
					'gps': {
						'time': data(dataMap['gps_time']),
						'coords': [data(dataMap['gps_lat']), data(dataMap['gps_lon'])],
						'altitude': data(dataMap['gps_alt'])
					},
					'bus_voltage': data(dataMap['bus_voltage']),
					'shunt_voltage': data(dataMap['shunt_voltage']),
					'current': data(dataMap['current'])
				}
				return dataDict
			except:
				return
