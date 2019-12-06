import board
import busio
import digitalio
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D25)
reset = digitalio.DigitalInOut(board.D8)
import adafruit_rfm9x
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)

#print("sending")
print("receiving")
while True:
	#rfm9x.send(b'Hello world!')
	data = rfm9x.receive()
	print(data)
