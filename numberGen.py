#Random Number Generator Thread
from threading import Thread, Event
from random import random
thread = Thread()
thread_stop_event = Event()
class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()
    def generateData(self):
        data = {
          'accel': [0,0,0],
          'gyro': [0,0,0],
          'mag': [0,0,0],
          'imu_temp': 0,
          'temp': 0,
          'pressure': 0,
          'alt': 0,
          'voltage': 0,
          'current': 0,
          'dt': 0
        }
        for key in data:
            try:
                for i in range(3):
                    data[key][i] = random()*10
            except:
                data[key] = random()*10
        for i in range(3):
            if random() > 0.5:
                data['accel'][i] = -1*data['accel'][i]
            if random() > 0.5:
                data['gyro'][i] = -1*data['gyro'][i]
        data['dt'] = random()*1.5
        return data

    def run(self):
        pass