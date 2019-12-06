import board
import busio
import digitalio
import adafruit_rfm9x
import json
import math
from threading import Thread

class Radio(Thread):
	def __init__(self, parent):
		spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
		cs = digitalio.DigitalInOut(board.D25) #can be any GPIO
		reset = digitalio.DigitalInOut(board.D8) #can be any GPIO
		self.rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)
		self.dataSize = 252 - 2 - 12 #number of bytes we can send in packet, minus check bytes
		self.parent = parent
		print(self.parent)
		super(Radio, self).__init__()

	def sendData(self, data):
		# max packet size is 252 bytes, if I want to send more than that, must be broken up
		# TODO not sure if the 252 includes the preamble and header or not!
		# need a way to mark packets -- numerator and denominator, 1 byte for each
		print("sending over radio")
		#print(data)
		#stringifiedData = json.dumps(data)

		dataString = str(round(data['accel'][0],3)) + ',' + str(round(data['accel'][1], 3)) + ',' + str(round(data['accel'][2], 3))
		dataString += ',' + str(round(data['gyro'][0],3)) + ',' + str(round(data['gyro'][1],3)) + ',' + str(round(data['gyro'][2],3))
		dataString += ',' + str(round(data['mag'][0],2)) + ',' + str(round(data['mag'][1],2)) + ',' + str(round(data['mag'][2],2))
		dataString += ',' + str(round(data['imu_temp'], 2))
		dataString += ',' + str(round(data['temp'],3))
		dataString += ',' + str(round(data['pressure'],3))
		dataString += ',' + str(round(data['alt'],3))
		dataString += ',' + str(round(data['bus_voltage'],3))
		dataString += ',' + str(round(data['shunt_voltage'],3))
		dataString += ',' + str(round(data['current'],3))
		dataString += ',' + str(round(data['dt'],3))
		try:
			dataString += ',' + str(data['gps']['time']) + ',' + str(data['gps']['coords'][0]) + ',' + str(data['gps']['coords'][1]) + ',' + str(data['gps']['quality'])
		except:
			pass
		try:
			dataString += ',' + str(round(data['gps']['satellites'],3))
			dataString += ',' + str(round(data['gps']['altitude'],3))
			dataString += ',' + str(round(data['gps']['speed'],3))
			dataString += ',' + str(round(data['gps']['track_angle'],3))
			dataString += ',' + str(round(data['gps']['dilation'],3))
			dataString += ',' + str(round(data['gps']['height_geoid'],3))
		except:
			pass

		numPackets = math.ceil(len(dataString) / (self.dataSize))
		#print(numPackets)
		for i in range(numPackets):
			packet = dataString[i*self.dataSize : (i+1)*self.dataSize]
			packet = packet + str(i+1) + str(numPackets)
			#print("packet {}/{}: {}".format(i+1, numPackets, packet))
			print("packet {}/{}".format(i+1, numPackets))
			try:
				self.rfm9x.send(bytes(packet, 'utf-8'))
			except:
				print("error sending packet")

	def captureAndSendImage(self):
		print("captureAndSendImage")
		try:
			print(self.parent)
			print(self.parent.cameraThread)
			fileLoc = self.parent.cameraThread.image()
			print("took image, file at: " + fileLoc)
			myfile = open(fileLoc, 'rb')
			mybytes = str(myfile.read())
			size = len(mybytes)
			print(mybytes)
			print(size)
			numPackets = math.ceil(size / (self.dataSize))
			#print(numPackets)
			for i in range(numPackets):
				packet = mybytes[i*self.dataSize : (i+1)*self.dataSize]
				packet = packet + str(i+1) + str(numPackets)
				#print("packet {}/{}: {}".format(i+1, numPackets, packet))
				print("packet {}/{}".format(i+1, numPackets))
				try:
					self.rfm9x.send(bytes(packet, 'utf-8'))
				except Exception as e:
					print("error sending packet")
					print(e)
		except:
			print("error taking picture")

	def run(self):
		print("radioThread running")
		while True:
			try:
				packet = self.rfm9x.receive(timeout=0.5)  # Wait for a packet to be received (up to 0.5 seconds)
				if packet is not None:
					packet_text = str(packet, 'ascii')
					rssi = self.rfm9x.rssi
					print('Received: {}, {}'.format(packet_text, rssi))
					if packet_text == "picture":
						self.captureAndSendImage()

			except Exception as e:
				print(e)
