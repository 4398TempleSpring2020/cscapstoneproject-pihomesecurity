#!usr/bin/python3
from sensor_manager import Sensor_Manager
from microphone import Microphone
from camera import Camera

if __name__ == '__main__':
    sm = Sensor_Manager()
    sm.add_sensor(Microphone(duration=10, frequency=44100))
    sm.add_sensor(Camera(duration=5, frequency=1))
    sm.connect_all()
    sm.initiate_all()
