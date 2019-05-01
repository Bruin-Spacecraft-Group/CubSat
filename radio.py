import board
import busio
import digitalio
import adafruit_rfm9x
import json
import math
from threading import Thread

class Radio(Thread):
	def __init__(self):
		spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
		cs = digitalio.DigitalInOut(board.D5) #can be any GPIO
		reset = digitalio.DigitalInOut(board.D6) #can be any GPIO
		self.rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)
		self.dataSize = 252 - 2 #number of bytes we can send in packet, minus check bytes
		super(Radio, self).__init__()
		
	def sendData(self, data):
		# max packet size is 252 bytes, if I want to send more than that, must be broken up
		# TODO not sure if the 252 includes the preamble and header or not!
		# need a way to mark packets -- numerator and denominator, 1 byte for each
		
		print(data)
		stringifiedData = json.dumps(data) 
		
		numPackets = math.ceil(len(stringifiedData) / (self.dataSize))
		print(numPackets)
		for i in range(numPackets):
			packet = stringifiedData[i*self.dataSize : (i+1)*self.dataSize]
			packet = packet + str(i+1) + str(numPackets)
			print(packet)
			self.rfm9x.send(packet)

	def run(self):
		while True:
			packet = self.rfm9x.receive()  # Wait for a packet to be received (up to 0.5 seconds)
			if packet is not None:
				packet_text = str(packet, 'ascii')
				rssi = self.rfm9x.rssi
				print('Received: {}, {}'.format(packet_text, rssi))
