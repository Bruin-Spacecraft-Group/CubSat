from time import sleep
from threading import Thread, Event
from random import random
import sensor

from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context


class Main(Thread):
	def __init__(self):
		## initialize sensors
		super(Main, self).__init__()
		self.daemon = True
		print("initialized")

	def run(self):
		print("main loop running")
		while True:
			data = sensor.poll()
			pushData(data)
			sleep(1)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)

@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('helloWorldFlask.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    print('Client connected')

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

def pushData(data):
    print(data)
    socketio.emit('telemetry', (data), namespace='/test')

if __name__ == '__main__':
	main = Main()
	main.start()
	socketio.run(app, host='0.0.0.0')
