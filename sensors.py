import gpiozero
from threading import Thread

# Simple demo of the LSM9DS1 accelerometer, magnetometer, gyroscope.
# Will print the acceleration, magnetometer, and gyroscope values every second.
import time
import board
import busio
import adafruit_lsm9ds1

class Sensors(Thread, parent):
	def __init__(self):
		# I2C connection:
		self.i2c = busio.I2C(board.SCL, board.SDA)
		self.imu = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

		self.data = {
			'accel': [0,0,0],
			'gyro': [0,0,0],
			'mag': [0,0,0],
			'imu_temp': 0,
			'temp': 0,
			'pressure': 0,
			'alt': 0,
			'voltage': 0,
			'current': 0
		}

		super(Sensors, self).__init__()
	
	# Main loop will read the acceleration, magnetometer, gyroscope, Temperature
	# values every second and print them out.
	while True:
	    # Read acceleration, magnetometer, gyroscope, temperature.
	    self.data['accel'] = self.imu.acceleration
	    self.data['mag'] = self.imu.magnetic
	    self.data['gyro'] = self.imu.gyro
	    self.data['imu_temp'] = self.imu.temperature
	    
	    # Print values.
	    print(self.data)
	    # Delay for a second.
	    time.sleep(1.0)
