from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.resolution = (64,64)
camera.framerate = 4
camera.start_preview(alpha=255)
sleep(2)
camera.capture('image.jpg')

camera.stop_preview()
