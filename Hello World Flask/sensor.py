import board
import busio
import adafruit_lsm9ds1
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
from time import sleep


def poll():
	accel_x, accel_y, accel_z = sensor.acceleration
	print('Acceleration: {0:0.3f},{1:0.3f},{2:0.3f}'.format(accel_x, accel_y, accel_z))
	return [accel_x, accel_y, accel_z]
