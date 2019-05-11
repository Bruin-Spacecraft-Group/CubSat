from picamera import PiCamera
from time import sleep
from threading import Thread
import os
from datetime import datetime

class Camera(Thread):
	def __init__(self, resolution):
		super(Camera, self).__init__()
		self.camera = PiCamera()
		if resolution == "High":
			self.camera.resolution = (2592,1944)
			self.camera.framerate = 15
		elif resolution == "Medium":
			self.camera.resolution = (1296,972)
			self.camera.framerate = 8
		elif resolution == "Mini":
			self.camera.resolution = (64,64)
			self.camera.framerate = 4
		self.ready = False
		self.fileLocation = str(os.getcwd()) + '/images/'
		print(self.fileLocation)
		self.whiteBalance()
		print("camera ready")

	def whiteBalance(self):
		self.camera.start_preview()
		sleep(2)
		self.camera.stop_preview()
		self.ready = True

	def image(self):
		print("taking picture")
		if self.ready:
			self.camera.start_preview()
			print("preview started")
			name = self.fileLocation +  str(datetime.now().replace(microsecond=0))
			name = name.replace(":", "-")
			self.camera.capture(name + ".jpg")
			self.camera.stop_preview()
			print("preview ended")
		else:
			self.whiteBalance()
			name = self.fileLocation +  str(datetime.now())
			self.camera.capture(name)
	def run(self):
		while True:
			self.camera.start_preview()
			sleep(2)
			self.camera.capture('image.jpg')
			self.camera.stop_preview()

if __name__ == "__main__":
	mycamera = Camera("Mini")
	mycamera.image()
