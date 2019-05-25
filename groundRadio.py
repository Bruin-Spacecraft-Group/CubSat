import board
import busio
import digitalio
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.RFM9X_CS)
reset = digitalio.DigitalInOut(board.RFM9X_RST)
import adafruit_rfm9x
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 433.0)

while True:
	packet = rfm9x.receive()  # Wait for a packet to be received (up to 0.5 seconds)
	if packet is not None:
	    packet_text = str(packet, 'ascii')
	    print('Received: {0}'.format(packet_text))