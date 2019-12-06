import gpiozero
from threading import Thread

# Simple demo of the LSM9DS1 accelerometer, magnetometer, gyroscope.
# Will print the acceleration, magnetometer, and gyroscope values every second.
import time
import board
import busio
import serial
import adafruit_lsm9ds1
import adafruit_mpl3115a2
import adafruit_ina219
import adafruit_gps

class Sensors(Thread):
	def __init__(self):
		self.imu = False
		self.baro = False
		self.currentSense = False
		self.gps = False

		# I2C connection:
		self.i2c = busio.I2C(board.SCL, board.SDA)
		try:
			self.imu = adafruit_lsm9ds1.LSM9DS1_I2C(self.i2c)
		except:
			print("could not connect to LSM9DS1")

		try:
			self.currentSense = adafruit_ina219.INA219(self.i2c, addr=0x45)
		except:
			print("could not connect to INA219")

		try:
			self.baro = adafruit_mpl3115a2.MPL3115A2(self.i2c)
			# Calibrate altimeter
			self.baro.sealevel_pressure = 102250
		except:
			print("could not connect to MPL3115A2")

		#self.RX = board.D15 #RX
		#self.TX = board.D14 #TX

		# Create a serial connection for the GPS connection using default speed and
		# a slightly higher timeout (GPS modules typically update once a second).
		try:
			#self.uart = busio.UART(self.TX, self.RX, baudrate=9600, timeout=3000)
			self.uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)
			self.gps = adafruit_gps.GPS(self.uart, debug=False)
			# Initialize the GPS module by changing what data it sends and at what rate.
			# These are NMEA extensions for PMTK_314_SET_NMEA_OUTPUT and
			# PMTK_220_SET_NMEA_UPDATERATE but you can send anything from here to adjust
			# the GPS module behavior:
			#   https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf

			# Turn on the basic GGA and RMC info (what you typically want)
			self.gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
			# Turn on just minimum info (RMC only, location):
			#gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
			# Turn off everything:
			#gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
			# Tuen on everything (not all of it is parsed!)
			#gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')

			# Set update rate to once a second (1hz) which is what you typically want.
			self.gps.send_command(b'PMTK220,900')
			# Or decrease to once every two seconds by doubling the millisecond value.
			# Be sure to also increase your UART timeout above!
			#gps.send_command(b'PMTK220,2000')
			# You can also speed up the rate, but don't go too fast or else you can lose
			# data during parsing.  This would be twice a second (2hz, 500ms delay):
			# gps.send_command(b'PMTK220,500')
			print(self.gps)
		except:
			print("could not connect to GPS")



		self.data = {
			'accel': [0,0,0],
			'gyro': [0,0,0],
			'mag': [0,0,0],
			'imu_temp': 0,
			'temp': 0,
			'pressure': 0,
			'alt': 0,
			'gps': 'no_fix',
			'bus_voltage': 0,
			'shunt_voltage': 0,
			'current': 0,
			'dt': 0
		}

		super(Sensors, self).__init__()


	# Main loop reads from initialized sensors
	def run(self):
		#print("HERE")
		while True:
			# Read acceleration, magnetometer, gyroscope, temperature.
			if self.imu:
				accel_x, accel_y, accel_z = self.imu.acceleration
				mag_x, mag_y, mag_z = self.imu.magnetic
				gyro_x, gyro_y, gyro_z = self.imu.gyro
				temp = self.imu.temperature
				self.data['accel'] = [accel_x, accel_y, accel_z]
				self.data['mag'] = [mag_x, mag_y, mag_z]
				self.data['gyro'] = [gyro_x, gyro_y, gyro_z]
				self.data['imu_temp'] = temp

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

			try:
				#print(self.gps.has_fix)
				if self.gps:
					#print("got in gps")
					#self.gps.update()
					if self.gps.has_fix:
						#print("FIX")
						self.data['gps'] = dict()
						# We have a fix! (gps.has_fix is true)
						# Print out details about the fix like location, date, etc.
						self.data['gps']['time'] = [
						    self.gps.timestamp_utc.tm_mon,   # Grab parts of the time from the
						    self.gps.timestamp_utc.tm_mday,  # struct_time object that holds
						    self.gps.timestamp_utc.tm_year,  # the fix time.  Note you might
						    self.gps.timestamp_utc.tm_hour,  # not get all data like year, day,
						    self.gps.timestamp_utc.tm_min,   # month!
						    self.gps.timestamp_utc.tm_sec]
						self.data['gps']['coords'] = [self.gps.latitude, self.gps.longitude]
						self.data['gps']['quality'] = self.gps.fix_quality
						# Some attributes beyond latitude, longitude and timestamp are optional
						# and might not be present.  Check if they're None before trying to use!
						if self.gps.satellites is not None:
						    self.data['gps']['satellites'] = self.gps.satellites
						if self.gps.altitude_m is not None:
						    self.data['gps']['altitude'] = self.gps.altitude_m
						if self.gps.speed_knots is not None:
						    self.data['gps']['speed'] = self.gps.speed_knots
						if self.gps.track_angle_deg is not None:
						    self.data['gps']['track_angle'] = self.gps.track_angle_deg
						if self.gps.horizontal_dilution is not None:
						    self.data['gps']['dilation'] = self.gps.horizontal_dilution
						if self.gps.height_geoid is not None:
						    self.data['gps']['height_geoid'] = self.gps.height_geoid
					else:
						#print("no fix")
						self.data['gps'] = "no_fix"
			except Exception as e:
				print(e)

			#print("FINISHED LOOP")
			# Print values.
			#print(self.data)
			# Delay for a second.
			time.sleep(1.0)
