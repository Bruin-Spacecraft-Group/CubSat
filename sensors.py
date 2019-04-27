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
		self.imu = False
		self.baro = False
		self.currentSense = False

		# I2C connection:
		self.i2c = busio.I2C(board.SCL, board.SDA)
		try:
			self.imu = adafruit_lsm9ds1.LSM9DS1_I2C(self.i2c)
		except:
			print("could not connect to LSM9DS1")
		
		try:
			self.currentSense = adafruit_ina219.INA219(self.i2c)
		except:
			print("could not connect to INA219")
		
		try:
			self.baro = adafruit_mpl3115a2.MPL3115A2(self.i2c)
		except:
			print("could not connect to MPL3115A2")

		self.data = {
			'accel': [0,0,0],
			'gyro': [0,0,0],
			'mag': [0,0,0],
			'imu_temp': 0,
			'temp': 0,
			'pressure': 0,
			'alt': 0,
			'bus_voltage': 0,
			'shunt_voltage': 0,
			'current': 0
		}

		# Calibrate altimeter
		self.baro.sealevel_pressure = 102250

		super(Sensors, self).__init__()
	

	# Main loop will read the acceleration, magnetometer, gyroscope, Temperature
	# values every second and print them out.
	def run(self):
		while True:
		    # Read acceleration, magnetometer, gyroscope, temperature.
		    if self.imu:
			    self.data['accel'] = self.imu.acceleration
			    self.data['mag'] = self.imu.magnetic
			    self.data['gyro'] = self.imu.gyro
			    self.data['imu_temp'] = self.imu.temperature
		    
		    if self.baro:
			    # Read barometer data
			    self.data['temp'] = self.baro.temperature
			    self.data['pressure'] = self.baro.pressure
			    self.data['alt'] = self.baro.altitude

		    if self.currentSense:
			    # Read power draw
			    self.data['bus_voltage'] = self.currentSense.bus_voltage
			    self.data['shunt_voltage'] = self.currentSense.shunt_voltage
			    self.data['current'] = self.currentSense.current

		    # Print values.
		    print(self.data)
		    # Delay for a second.
		    time.sleep(1.0)
