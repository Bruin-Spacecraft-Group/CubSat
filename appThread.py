
# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)

class AppThread(Thread):
    def __init__(self):
        print("init app thread")
        super(AppThread, self).__init__()

    @app.route('/')
    def index():
        #only by sending this page first will the client be connected to the socketio instance
        return render_template('index.html')

    @socketio.on('connect', namespace='/test')
    def test_connect():
        print('Client connected')

    @socketio.on('disconnect', namespace='/test')
    def test_disconnect():
        print('Client disconnected')
    

    def pushData(self, data):
        socketio.emit('newnumber', data, namespace='/test')

    def run(self):
    	socketio.run(self.app, host='0.0.0.0')
